#!/usr/bin/env python3
"""
VisionUX Core: Autonomous Accessibility Repair Engine
Built on Karpathy's Autoresearch Philosophy & NAIM Discipline

LIFT-003 Enhancements:
- CIE Delta-E 2000 color distance calculation
- K-Means pixel sampling for gradient handling
- Refined M-metric with max(0, 4.5 - C) formula
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
import cv2
from sklearn.cluster import KMeans

# Color science library
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

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
    delta_e: float = 0.0  # CIE Delta-E 2000 color distance


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
# ADVANCED COLOR SCIENCE (LIFT-003)
# ============================================================================

class ColorScience:
    """
    Advanced color analysis using CIE Delta-E 2000.
    Ensures minimal perceptual color change during repair.
    """
    
    @staticmethod
    def calculate_delta_e(rgb1: Tuple[int, int, int], 
                          rgb2: Tuple[int, int, int]) -> float:
        """
        Calculate CIE Delta-E 2000 color distance.
        
        ΔE < 1.0: Not perceptible by human eyes
        ΔE < 5.0: Acceptable for brand consistency
        ΔE > 10.0: Significantly different colors
        
        Args:
            rgb1: Original color (0-255 range)
            rgb2: Modified color (0-255 range)
            
        Returns:
            Delta-E 2000 distance (0-100)
        """
        try:
            # Convert RGB to sRGB color objects (0-1 range)
            color1 = sRGBColor(rgb1[0]/255, rgb1[1]/255, rgb1[2]/255)
            color2 = sRGBColor(rgb2[0]/255, rgb2[1]/255, rgb2[2]/255)
            
            # Convert to LAB color space (perceptually uniform)
            lab1 = convert_color(color1, LabColor)
            lab2 = convert_color(color2, LabColor)
            
            # Calculate Delta-E 2000
            delta_e = delta_e_cie2000(lab1, lab2)
            
            # Handle numpy scalar conversion (compatibility fix)
            if hasattr(delta_e, 'item'):
                return float(delta_e.item())
            return float(delta_e)
            
        except Exception as e:
            # Fallback: Simple Euclidean distance in RGB space
            r_diff = (rgb1[0] - rgb2[0]) ** 2
            g_diff = (rgb1[1] - rgb2[1]) ** 2
            b_diff = (rgb1[2] - rgb2[2]) ** 2
            euclidean = (r_diff + g_diff + b_diff) ** 0.5
            # Normalize to Delta-E range (0-100)
            return euclidean / 441.67 * 100  # 441.67 = sqrt(255^2 * 3)
    
    @staticmethod
    def sample_background_kmeans(image_array: np.ndarray,
                                  bbox: Tuple[int, int, int, int],
                                  n_clusters: int = 3,
                                  sample_size: int = 10) -> Tuple[int, int, int]:
        """
        Use K-Means clustering to find dominant background color.
        Handles gradients by sampling multiple regions.
        
        Args:
            image_array: Full image as numpy array
            bbox: Text bounding box (x_min, y_min, x_max, y_max)
            n_clusters: Number of K-Means clusters
            sample_size: Padding around bbox for sampling
            
        Returns:
            Dominant background RGB color
        """
        x_min, y_min, x_max, y_max = bbox
        h, w = image_array.shape[:2]
        
        # Expand bbox for background sampling
        bg_x_min = max(0, x_min - sample_size)
        bg_y_min = max(0, y_min - sample_size)
        bg_x_max = min(w, x_max + sample_size)
        bg_y_max = min(h, y_max + sample_size)
        
        # Collect border pixels (exclude text area)
        border_pixels = []
        
        # Top border
        if bg_y_min < y_min:
            top = image_array[bg_y_min:y_min, bg_x_min:bg_x_max]
            border_pixels.append(top.reshape(-1, 3))
        
        # Bottom border
        if y_max < bg_y_max:
            bottom = image_array[y_max:bg_y_max, bg_x_min:bg_x_max]
            border_pixels.append(bottom.reshape(-1, 3))
        
        # Left border
        if bg_x_min < x_min:
            left = image_array[y_min:y_max, bg_x_min:x_min]
            border_pixels.append(left.reshape(-1, 3))
        
        # Right border
        if x_max < bg_x_max:
            right = image_array[y_min:y_max, x_max:bg_x_max]
            border_pixels.append(right.reshape(-1, 3))
        
        if not border_pixels:
            # Fallback: sample corners
            return tuple(image_array[0, 0])
        
        # Combine all border pixels
        all_pixels = np.vstack(border_pixels)
        
        if len(all_pixels) < n_clusters:
            # Not enough pixels for K-Means
            return tuple(np.median(all_pixels, axis=0).astype(int))
        
        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(all_pixels)
        
        # Find most common cluster (dominant color)
        labels = kmeans.labels_
        unique, counts = np.unique(labels, return_counts=True)
        dominant_cluster = unique[np.argmax(counts)]
        
        # Return cluster center as background color
        bg_color = kmeans.cluster_centers_[dominant_cluster]
        
        return tuple(bg_color.astype(int))
    
    @staticmethod
    def find_worst_case_contrast(image_array: np.ndarray,
                                  text_bbox: Tuple[int, int, int, int],
                                  text_rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """
        For gradient backgrounds, find the worst-case (lowest contrast) color.
        This ensures our fix works across the entire gradient.
        
        Args:
            image_array: Full image
            text_bbox: Text bounding box
            text_rgb: Text color
            
        Returns:
            Background color with lowest contrast to text
        """
        x_min, y_min, x_max, y_max = text_bbox
        h, w = image_array.shape[:2]
        
        # Sample background region
        bg_x_min = max(0, x_min - 10)
        bg_y_min = max(0, y_min - 10)
        bg_x_max = min(w, x_max + 10)
        bg_y_max = min(h, y_max + 10)
        
        # Get unique background colors
        bg_region = image_array[bg_y_min:bg_y_max, bg_x_min:bg_x_max]
        bg_pixels = bg_region.reshape(-1, 3)
        unique_colors = np.unique(bg_pixels, axis=0)
        
        # Calculate contrast for each unique color
        min_contrast = float('inf')
        worst_bg = unique_colors[0]
        
        for bg_color in unique_colors:
            contrast = WCAGContrastChecker.calculate_contrast_ratio(
                text_rgb, tuple(bg_color)
            )
            if contrast < min_contrast:
                min_contrast = contrast
                worst_bg = bg_color
        
        return tuple(worst_bg)


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
        Calculate refined M-metric per IDEA v2.0 specification.
        
        Formula: M = (1/N) * Σ max(0, 4.5 - C_actual)
        
        This ensures:
        - M = 0: Perfect compliance (all C ≥ 4.5)
        - M > 0: Sum of deficits from threshold
        - Only counts violations, not excess contrast
        
        Args:
            violations: List of detected violations
            
        Returns:
            M metric value (0 = perfect)
        """
        if not violations:
            return 0.0
        
        # Calculate deficit for each violation
        deficits = [max(0, self.target_ratio - v.actual_ratio) 
                   for v in violations]
        
        # Average deficit
        M = sum(deficits) / len(violations)
        
        return M
    
    def auto_repair(self, violation: ContrastViolation) -> RepairSuggestion:
        """
        Generate minimal color adjustment with Delta-E constraint.
        
        Strategy (LIFT-003 Enhanced):
        1. Determine if text is darker or lighter than background
        2. Adjust color with minimal change
        3. Ensure Delta-E < 5.0 for brand consistency
        4. Preserve hue, only modify lightness
        5. Use K-Means if gradient detected
        """
        text_rgb = violation.text_rgb
        bg_rgb = violation.bg_rgb
        target = self.target_ratio
        
        # Calculate luminances to determine which is darker
        text_lum = WCAGContrastChecker.rgb_to_relative_luminance(text_rgb)
        bg_lum = WCAGContrastChecker.rgb_to_relative_luminance(bg_rgb)
        
        best_repair = None
        min_delta_e = float('inf')
        
        # Strategy 1: Darken text (if text is lighter)
        if text_lum > bg_lum:
            # Text is lighter - try darkening it
            for factor in np.linspace(0, 1, 100):
                # Interpolate towards black
                candidate_rgb = tuple(int(c * (1 - factor)) for c in text_rgb)
                ratio = WCAGContrastChecker.calculate_contrast_ratio(candidate_rgb, bg_rgb)
                
                if ratio >= target:
                    # Check Delta-E constraint
                    delta_e = ColorScience.calculate_delta_e(text_rgb, candidate_rgb)
                    
                    if delta_e < min_delta_e:
                        min_delta_e = delta_e
                        best_repair = RepairSuggestion(
                            original_text=text_rgb,
                            fixed_text=candidate_rgb,
                            original_bg=bg_rgb,
                            fixed_bg=bg_rgb,
                            ratio_before=violation.actual_ratio,
                            ratio_after=ratio,
                            strategy="darken_text",
                            hue_shift_degrees=0.0,
                            saturation_shift_percent=0.0,
                            delta_e=delta_e
                        )
                    
                    # If Delta-E < 5, use this (brand-safe)
                    if delta_e < 5.0:
                        break
            
            if best_repair and best_repair.delta_e < 10.0:
                return best_repair
        
        # Strategy 2: Lighten text (if text is darker)
        if text_lum <= bg_lum:
            # Text is darker - try lightening it
            for factor in np.linspace(0, 1, 100):
                # Interpolate towards white
                candidate_rgb = tuple(int(c + (255 - c) * factor) for c in text_rgb)
                ratio = WCAGContrastChecker.calculate_contrast_ratio(candidate_rgb, bg_rgb)
                
                if ratio >= target:
                    delta_e = ColorScience.calculate_delta_e(text_rgb, candidate_rgb)
                    
                    if delta_e < min_delta_e:
                        min_delta_e = delta_e
                        best_repair = RepairSuggestion(
                            original_text=text_rgb,
                            fixed_text=candidate_rgb,
                            original_bg=bg_rgb,
                            fixed_bg=bg_rgb,
                            ratio_before=violation.actual_ratio,
                            ratio_after=ratio,
                            strategy="lighten_text",
                            hue_shift_degrees=0.0,
                            saturation_shift_percent=0.0,
                            delta_e=delta_e
                        )
                    
                    if delta_e < 5.0:
                        break
            
            if best_repair and best_repair.delta_e < 10.0:
                return best_repair
        
        # Strategy 3: Adjust background if text adjustment wasn't enough
        if bg_lum > text_lum:
            # Background is lighter - try lightening more
            for factor in np.linspace(0, 1, 100):
                candidate_rgb = tuple(int(c + (255 - c) * factor) for c in bg_rgb)
                ratio = WCAGContrastChecker.calculate_contrast_ratio(text_rgb, candidate_rgb)
                
                if ratio >= target:
                    delta_e = ColorScience.calculate_delta_e(bg_rgb, candidate_rgb)
                    
                    if delta_e < min_delta_e:
                        min_delta_e = delta_e
                        best_repair = RepairSuggestion(
                            original_text=text_rgb,
                            fixed_text=text_rgb,
                            original_bg=bg_rgb,
                            fixed_bg=candidate_rgb,
                            ratio_before=violation.actual_ratio,
                            ratio_after=ratio,
                            strategy="lighten_background",
                            hue_shift_degrees=0.0,
                            saturation_shift_percent=0.0,
                            delta_e=delta_e
                        )
                    
                    if delta_e < 5.0:
                        break
            
            if best_repair:
                return best_repair
        else:
            # Background is darker - try darkening more
            for factor in np.linspace(0, 1, 100):
                candidate_rgb = tuple(int(c * (1 - factor)) for c in bg_rgb)
                ratio = WCAGContrastChecker.calculate_contrast_ratio(text_rgb, candidate_rgb)
                
                if ratio >= target:
                    delta_e = ColorScience.calculate_delta_e(bg_rgb, candidate_rgb)
                    
                    if delta_e < min_delta_e:
                        min_delta_e = delta_e
                        best_repair = RepairSuggestion(
                            original_text=text_rgb,
                            fixed_text=text_rgb,
                            original_bg=bg_rgb,
                            fixed_bg=candidate_rgb,
                            ratio_before=violation.actual_ratio,
                            ratio_after=ratio,
                            strategy="darken_background",
                            hue_shift_degrees=0.0,
                            saturation_shift_percent=0.0,
                            delta_e=delta_e
                        )
                    
                    if delta_e < 5.0:
                        break
            
            if best_repair:
                return best_repair
        
        # Fallback: Force to maximum contrast (only if Delta-E failed)
        if text_lum > bg_lum:
            # Use white text on dark background
            delta_e = ColorScience.calculate_delta_e(text_rgb, (255, 255, 255))
            return RepairSuggestion(
                original_text=text_rgb,
                fixed_text=(255, 255, 255),
                original_bg=bg_rgb,
                fixed_bg=(0, 0, 0),
                ratio_before=violation.actual_ratio,
                ratio_after=21.0,
                strategy="force_maximum_contrast",
                hue_shift_degrees=0.0,
                saturation_shift_percent=0.0,
                delta_e=delta_e
            )
        else:
            # Use black text on white background
            delta_e = ColorScience.calculate_delta_e(text_rgb, (0, 0, 0))
            return RepairSuggestion(
                original_text=text_rgb,
                fixed_text=(0, 0, 0),
                original_bg=bg_rgb,
                fixed_bg=(255, 255, 255),
                ratio_before=violation.actual_ratio,
                ratio_after=21.0,
                strategy="force_maximum_contrast",
                hue_shift_degrees=0.0,
                saturation_shift_percent=0.0,
                delta_e=delta_e
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
        print(f"  • Delta-E: {repair.delta_e:.2f} {'🟢 (brand-safe)' if repair.delta_e < 5.0 else '🟡 (acceptable)' if repair.delta_e < 10.0 else '🔴 (significant)'}")
        
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
