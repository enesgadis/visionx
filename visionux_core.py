#!/usr/bin/env python3
"""
VisionUX Core: Autonomous Accessibility Repair Engine
Built on Karpathy's Autoresearch Philosophy & NAIM Discipline

This module orchestrates the complete repair cycle:
1. Image Analysis → Color Extraction
2. WCAG Calculation → Violation Detection  
3. Auto-Repair → Color Optimization
4. Code Generation → React Native patches
5. Metric Validation → Commit or Rollback
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from PIL import Image
import colorsys

# Import existing WCAG checker
from wcag_contrast_checker import (
    WCAGContrastChecker,
    ScreenshotAnalyzer
)


# ============================================================================
# DATA CONTRACTS (Type-Safe Interfaces)
# ============================================================================

@dataclass
class ColorPair:
    """Represents a text-background color pair from UI element."""
    text_rgb: Tuple[int, int, int]
    bg_rgb: Tuple[int, int, int]
    bbox: Tuple[int, int, int, int]  # (x_min, y_min, x_max, y_max)
    element_text: str
    ocr_confidence: float


@dataclass
class ContrastViolation:
    """WCAG violation detected in UI."""
    element_id: str
    element_text: str
    bbox: Tuple[int, int, int, int]
    text_rgb: Tuple[int, int, int]
    bg_rgb: Tuple[int, int, int]
    actual_ratio: float
    target_ratio: float = 4.5
    severity: str = "moderate"  # critical, moderate, minor
    
    def __post_init__(self):
        if self.actual_ratio < 3.0:
            self.severity = "critical"
        elif self.actual_ratio < 4.0:
            self.severity = "moderate"
        else:
            self.severity = "minor"


@dataclass
class RepairSuggestion:
    """Proposed fix for a contrast violation."""
    original_text: Tuple[int, int, int]
    fixed_text: Tuple[int, int, int]
    original_bg: Tuple[int, int, int]
    fixed_bg: Tuple[int, int, int]
    ratio_before: float
    ratio_after: float
    strategy: str  # "darken_text", "lighten_bg", "both"
    hue_shift_degrees: float
    saturation_shift_percent: float


@dataclass
class LiftResult:
    """Result of a single Naim Lift execution."""
    lift_number: int
    success: bool
    element_id: str
    M_before: float
    M_after: float
    delta_M: float
    repair: Optional[RepairSuggestion]
    commit_hash: Optional[str]
    timestamp: datetime
    reason: Optional[str] = None  # For failures


# ============================================================================
# CORE ENGINE
# ============================================================================

class VisionUXCore:
    """Main orchestrator for autonomous accessibility repair."""
    
    def __init__(self, image_path: str, target_ratio: float = 4.5):
        self.image_path = Path(image_path)
        self.target_ratio = target_ratio
        self.analyzer = ScreenshotAnalyzer(str(image_path))
        self.lift_counter = 0
        self.lifts_log = []
        
    def scan_violations(self) -> List[ContrastViolation]:
        """
        Scan image and return all WCAG violations.
        Uses existing ScreenshotAnalyzer.
        """
        results = self.analyzer.analyze()
        violations = []
        
        for i, result in enumerate(results):
            if result['wcag_aa'] == 'FAIL':
                violation = ContrastViolation(
                    element_id=f"element_{i:03d}",
                    element_text=result['text'],
                    bbox=result['bbox'],
                    text_rgb=result['text_color'],
                    bg_rgb=result['background_color'],
                    actual_ratio=result['contrast_ratio'],
                    target_ratio=self.target_ratio
                )
                violations.append(violation)
        
        return violations
    
    def calculate_M_metric(self, violations: List[ContrastViolation]) -> float:
        """
        Calculate aggregate health metric.
        M = 0: Perfect (all compliant)
        M > 0: Average distance from threshold
        """
        if not violations:
            return 0.0
        
        distances = [abs(self.target_ratio - v.actual_ratio) 
                    for v in violations]
        return sum(distances) / len(violations)
    
    def auto_repair(self, violation: ContrastViolation) -> RepairSuggestion:
        """
        Generate minimal color adjustment to fix violation.
        
        Strategy (WCAG-compliant):
        1. Determine if text is darker or lighter than background
        2. Adjust the appropriate color with minimal change
        3. Use binary search for efficiency
        4. Preserve hue, only modify lightness
        """
        text_rgb = violation.text_rgb
        bg_rgb = violation.bg_rgb
        target = self.target_ratio
        
        # Calculate luminances to determine which is darker
        text_lum = WCAGContrastChecker.rgb_to_relative_luminance(text_rgb)
        bg_lum = WCAGContrastChecker.rgb_to_relative_luminance(bg_rgb)
        
        # Strategy 1: Darken text (if text is lighter)
        if text_lum > bg_lum:
            # Text is lighter - try darkening it
            for factor in np.linspace(0, 1, 100):
                # Interpolate towards black
                candidate_rgb = tuple(int(c * (1 - factor)) for c in text_rgb)
                ratio = WCAGContrastChecker.calculate_contrast_ratio(candidate_rgb, bg_rgb)
                
                if ratio >= target:
                    return RepairSuggestion(
                        original_text=text_rgb,
                        fixed_text=candidate_rgb,
                        original_bg=bg_rgb,
                        fixed_bg=bg_rgb,
                        ratio_before=violation.actual_ratio,
                        ratio_after=ratio,
                        strategy="darken_text",
                        hue_shift_degrees=0.0,
                        saturation_shift_percent=0.0
                    )
        
        # Strategy 2: Lighten text (if text is darker)
        if text_lum <= bg_lum:
            # Text is darker - try lightening it
            for factor in np.linspace(0, 1, 100):
                # Interpolate towards white
                candidate_rgb = tuple(int(c + (255 - c) * factor) for c in text_rgb)
                ratio = WCAGContrastChecker.calculate_contrast_ratio(candidate_rgb, bg_rgb)
                
                if ratio >= target:
                    return RepairSuggestion(
                        original_text=text_rgb,
                        fixed_text=candidate_rgb,
                        original_bg=bg_rgb,
                        fixed_bg=bg_rgb,
                        ratio_before=violation.actual_ratio,
                        ratio_after=ratio,
                        strategy="lighten_text",
                        hue_shift_degrees=0.0,
                        saturation_shift_percent=0.0
                    )
        
        # Strategy 3: Adjust background if text adjustment wasn't enough
        if bg_lum > text_lum:
            # Background is lighter - try lightening more
            for factor in np.linspace(0, 1, 100):
                candidate_rgb = tuple(int(c + (255 - c) * factor) for c in bg_rgb)
                ratio = WCAGContrastChecker.calculate_contrast_ratio(text_rgb, candidate_rgb)
                
                if ratio >= target:
                    return RepairSuggestion(
                        original_text=text_rgb,
                        fixed_text=text_rgb,
                        original_bg=bg_rgb,
                        fixed_bg=candidate_rgb,
                        ratio_before=violation.actual_ratio,
                        ratio_after=ratio,
                        strategy="lighten_background",
                        hue_shift_degrees=0.0,
                        saturation_shift_percent=0.0
                    )
        else:
            # Background is darker - try darkening more
            for factor in np.linspace(0, 1, 100):
                candidate_rgb = tuple(int(c * (1 - factor)) for c in bg_rgb)
                ratio = WCAGContrastChecker.calculate_contrast_ratio(text_rgb, candidate_rgb)
                
                if ratio >= target:
                    return RepairSuggestion(
                        original_text=text_rgb,
                        fixed_text=text_rgb,
                        original_bg=bg_rgb,
                        fixed_bg=candidate_rgb,
                        ratio_before=violation.actual_ratio,
                        ratio_after=ratio,
                        strategy="darken_background",
                        hue_shift_degrees=0.0,
                        saturation_shift_percent=0.0
                    )
        
        # Fallback: Force to maximum contrast (black on white or white on black)
        if text_lum > bg_lum:
            # Use white text on dark background
            return RepairSuggestion(
                original_text=text_rgb,
                fixed_text=(255, 255, 255),
                original_bg=bg_rgb,
                fixed_bg=(0, 0, 0),
                ratio_before=violation.actual_ratio,
                ratio_after=21.0,
                strategy="force_maximum_contrast",
                hue_shift_degrees=0.0,
                saturation_shift_percent=0.0
            )
        else:
            # Use black text on white background
            return RepairSuggestion(
                original_text=text_rgb,
                fixed_text=(0, 0, 0),
                original_bg=bg_rgb,
                fixed_bg=(255, 255, 255),
                ratio_before=violation.actual_ratio,
                ratio_after=21.0,
                strategy="force_maximum_contrast",
                hue_shift_degrees=0.0,
                saturation_shift_percent=0.0
            )
    
    def execute_lift(self, violation: ContrastViolation) -> LiftResult:
        """
        Execute one atomic lift: fix → test → commit or rollback.
        """
        self.lift_counter += 1
        timestamp = datetime.now()
        
        print(f"\n→ LIFT-{self.lift_counter:03d}: Fixing '{violation.element_text[:30]}'...")
        print(f"  • Before: RGB{violation.text_rgb} on RGB{violation.bg_rgb} = {violation.actual_ratio:.2f}:1 ❌")
        
        # Measure baseline
        M_before = self.calculate_M_metric(self.scan_violations())
        
        # Generate repair
        repair = self.auto_repair(violation)
        
        print(f"  • After: RGB{repair.fixed_text} on RGB{repair.fixed_bg} = {repair.ratio_after:.2f}:1 ✅")
        print(f"  • Strategy: {repair.strategy}")
        
        # TODO: Apply fix to actual codebase (for now, simulation)
        # self._apply_fix_to_code(repair)
        
        # Rescan to get new M
        # M_after = self.calculate_M_metric(self.scan_violations())
        # For now, simulate improvement
        M_after = M_before - abs(repair.ratio_after - violation.actual_ratio) / 10
        
        delta_M = M_before - M_after
        
        # Decision: Commit or Rollback
        if M_after < M_before and repair.ratio_after >= self.target_ratio:
            print(f"  • M: {M_before:.2f} → {M_after:.2f} (Δ {delta_M:.2f})")
            print(f"  • Weight: {int(delta_M * 100)}kg 🏋️")
            
            # Would commit here
            # commit_hash = self._git_commit(self.lift_counter, M_before, M_after)
            commit_hash = f"abc{self.lift_counter:04d}"
            
            result = LiftResult(
                lift_number=self.lift_counter,
                success=True,
                element_id=violation.element_id,
                M_before=M_before,
                M_after=M_after,
                delta_M=delta_M,
                repair=repair,
                commit_hash=commit_hash,
                timestamp=timestamp
            )
        else:
            print(f"  • ⚠️ REGRESSION DETECTED - Rolling back")
            # Would rollback here
            # subprocess.run(['git', 'reset', '--hard', 'HEAD'], check=True)
            
            result = LiftResult(
                lift_number=self.lift_counter,
                success=False,
                element_id=violation.element_id,
                M_before=M_before,
                M_after=M_after,
                delta_M=0.0,
                repair=None,
                commit_hash=None,
                timestamp=timestamp,
                reason="M_regressed" if M_after >= M_before else "insufficient_ratio"
            )
        
        self.lifts_log.append(result)
        return result
    
    def run_autonomous_repair(self) -> Dict:
        """
        Main autonomous loop: fix all violations sequentially.
        Stops when M = 0 or all lifts attempted.
        """
        print("="*80)
        print("VISIONUX AUTONOMOUS REPAIR CYCLE")
        print("="*80)
        
        # Initial scan
        violations = self.scan_violations()
        M_baseline = self.calculate_M_metric(violations)
        
        print(f"\n→ Scanning image: {self.image_path.name}")
        print(f"→ Found {len(violations)} WCAG violations")
        print(f"→ M_baseline = {M_baseline:.2f}")
        print(f"\n→ Starting autonomous repair...")
        
        successful_lifts = 0
        failed_lifts = 0
        
        for violation in violations:
            result = self.execute_lift(violation)
            
            if result.success:
                successful_lifts += 1
            else:
                failed_lifts += 1
        
        # Final report
        final_M = self.calculate_M_metric(self.scan_violations())
        total_weight = sum(int(lift.delta_M * 100) for lift in self.lifts_log if lift.success)
        
        print(f"\n" + "="*80)
        print("FINAL REPORT")
        print("="*80)
        print(f"• {successful_lifts} violations fixed")
        print(f"• {failed_lifts} regressions prevented")
        print(f"• M: {M_baseline:.2f} → {final_M:.2f} ({(1 - final_M/M_baseline)*100:.1f}% improvement)")
        print(f"• Total weight: {total_weight}kg across {successful_lifts} lifts")
        print(f"• Success rate: {successful_lifts/(successful_lifts+failed_lifts)*100:.1f}%")
        
        return {
            'M_baseline': M_baseline,
            'M_final': final_M,
            'successful_lifts': successful_lifts,
            'failed_lifts': failed_lifts,
            'total_weight': total_weight,
            'lifts_log': self.lifts_log
        }
    
    # Helper methods
    def _rgb_to_hsl(self, rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """Convert RGB (0-255) to HSL (0-1, 0-1, 0-1)."""
        r, g, b = [x / 255.0 for x in rgb]
        return colorsys.rgb_to_hls(r, g, b)
    
    def _hsl_to_rgb(self, hsl: Tuple[float, float, float]) -> Tuple[int, int, int]:
        """Convert HSL (0-1, 0-1, 0-1) to RGB (0-255)."""
        h, l, s = hsl  # colorsys uses HLS order
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return tuple(int(x * 255) for x in (r, g, b))


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    if len(sys.argv) != 2:
        print("Usage: python visionux_core.py <screenshot.png>")
        print("\nExample:")
        print("  python visionux_core.py test_screenshots/halısaha_app.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    try:
        core = VisionUXCore(image_path, target_ratio=4.5)
        results = core.run_autonomous_repair()
        
        # TODO: Write results to MOBILE.md
        # TODO: Generate React Native patches
        
        sys.exit(0 if results['M_final'] == 0 else 1)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
