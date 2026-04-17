# VisionUX Technical Specification
**Project:** Autonomous Mobile UI Accessibility Repair System  
**Standard:** WCAG 2.1 AA (Contrast Minimum 4.5:1)  
**Philosophy:** Karpathy Autoresearch + NAIM Discipline  
**Updated:** 2026-03-18

---

## 1. PROJECT SCOPE & OBJECTIVES

### 1.1 Primary Mission
Build an autonomous system that:
- Accepts mobile UI screenshots or React Native code
- Detects WCAG 2.1 AA violations (contrast < 4.5:1)
- Generates minimal color adjustments to achieve compliance
- Auto-commits successful fixes without human intervention

### 1.2 Success Criteria
- **M Metric:** Reduce M = (1/N) * Σ |4.5 - C_actual| to 0.0
- **Zero Regression:** Every commit improves or maintains metrics
- **Brand Preservation:** Hue shifts < 15° in HSL space
- **Automation:** 100% autonomous operation (no human approvals)

---

## 2. SYSTEM ARCHITECTURE

### 2.1 Core Modules

```
visionux/
├── visionux_core.py           # Main orchestrator
│   ├── ImageAnalyzer          # OCR + color extraction
│   ├── ContrastCalculator     # WCAG math engine
│   ├── ViolationDetector      # Threshold checking
│   └── AutoRepairEngine       # Color optimization
│
├── wcag_contrast_checker.py   # Existing scanner (v0.2)
│
├── react_native_generator.py  # StyleSheet code gen
│
├── metrics/
│   ├── m_calculator.py        # M metric computation
│   └── lift_logger.py         # MOBILE.md writer
│
└── tests/
    ├── test_contrast.py       # Unit tests
    └── test_lifts.py          # Integration tests
```

### 2.2 Data Flow

```
Input (Screenshot/Code)
    ↓
[ImageAnalyzer] → Extract (text_rgb, bg_rgb, bbox)
    ↓
[ContrastCalculator] → Compute ratios
    ↓
[ViolationDetector] → Filter violations
    ↓
[AutoRepairEngine] → Generate fixes
    ↓
[ReactNativeGenerator] → Output StyleSheet
    ↓
[TestRunner] → Validate fix
    ↓
[MetricCalculator] → Compute new M
    ↓
Decision: M improved? → Commit : Rollback
    ↓
[LiftLogger] → Log to MOBILE.md
```

---

## 3. TECHNICAL SPECIFICATIONS

### 3.1 WCAG 2.1 Contrast Formula

```python
def relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """
    Convert RGB to relative luminance.
    
    Per WCAG 2.1:
    1. Normalize RGB to [0, 1]
    2. Apply gamma correction:
       - If c ≤ 0.03928: c_linear = c / 12.92
       - Else: c_linear = ((c + 0.055) / 1.055) ^ 2.4
    3. Calculate: L = 0.2126*R + 0.7152*G + 0.0722*B
    """
    r, g, b = [x / 255.0 for x in rgb]
    
    def linearize(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    R, G, B = map(linearize, [r, g, b])
    return 0.2126 * R + 0.7152 * G + 0.0722 * B

def contrast_ratio(color1: Tuple[int, int, int], 
                   color2: Tuple[int, int, int]) -> float:
    """
    WCAG 2.1 contrast ratio.
    Returns value in range [1.0, 21.0]
    """
    L1 = relative_luminance(color1)
    L2 = relative_luminance(color2)
    
    lighter = max(L1, L2)
    darker = min(L1, L2)
    
    return (lighter + 0.05) / (darker + 0.05)
```

### 3.2 Auto-Repair Algorithm

```python
def auto_repair(text_rgb: Tuple[int, int, int],
                bg_rgb: Tuple[int, int, int],
                target_ratio: float = 4.5) -> RepairSuggestion:
    """
    Find minimal color adjustment to achieve target contrast.
    
    Strategy:
    1. Convert to HSL color space
    2. Preserve Hue (H) and Saturation (S)
    3. Adjust only Lightness (L) of foreground
    4. If insufficient, adjust background Lightness
    5. Binary search for minimal L change
    
    Constraints:
    - Max hue shift: ±15°
    - Prefer darkening text over lightening background
    - Stay within perceptually similar colors
    """
    # Convert to HSL
    text_hsl = rgb_to_hsl(text_rgb)
    bg_hsl = rgb_to_hsl(bg_rgb)
    
    # Try adjusting text lightness first
    for lightness in np.linspace(0, 1, 100):
        candidate_rgb = hsl_to_rgb((text_hsl[0], text_hsl[1], lightness))
        ratio = contrast_ratio(candidate_rgb, bg_rgb)
        
        if ratio >= target_ratio:
            return RepairSuggestion(
                original_text=text_rgb,
                fixed_text=candidate_rgb,
                original_bg=bg_rgb,
                fixed_bg=bg_rgb,
                ratio_before=contrast_ratio(text_rgb, bg_rgb),
                ratio_after=ratio,
                strategy="darken_text"
            )
    
    # If text adjustment insufficient, adjust background
    for lightness in np.linspace(0, 1, 100):
        candidate_rgb = hsl_to_rgb((bg_hsl[0], bg_hsl[1], lightness))
        ratio = contrast_ratio(text_rgb, candidate_rgb)
        
        if ratio >= target_ratio:
            return RepairSuggestion(
                original_text=text_rgb,
                fixed_text=text_rgb,
                original_bg=bg_rgb,
                fixed_bg=candidate_rgb,
                ratio_before=contrast_ratio(text_rgb, bg_rgb),
                ratio_after=ratio,
                strategy="adjust_background"
            )
    
    # Last resort: adjust both
    # ... (similar binary search on both colors)
```

### 3.3 M Metric Implementation

```python
def calculate_M_metric(violations: List[ContrastViolation]) -> float:
    """
    Aggregate metric for system health.
    
    M = 0: Perfect compliance
    M > 0: Average distance from threshold
    
    Each Naim Lift must reduce M monotonically.
    """
    if not violations:
        return 0.0
    
    distances = [abs(4.5 - v.actual_ratio) for v in violations 
                 if v.actual_ratio < 4.5]
    
    return sum(distances) / len(violations) if distances else 0.0
```

---

## 4. NAIM LIFT DISCIPLINE

### 4.1 Lift Execution Protocol

Each lift is a 15-minute atomic operation:

```python
def execute_lift(violation: ContrastViolation) -> LiftResult:
    """
    One violation, one fix, one commit.
    """
    # 1. Measure baseline
    M_before = calculate_M_metric(scan_all_violations())
    
    # 2. Generate fix
    repair = auto_repair(violation.text_rgb, violation.bg_rgb)
    
    # 3. Apply fix
    apply_fix_to_codebase(repair)
    
    # 4. Validate
    M_after = calculate_M_metric(scan_all_violations())
    
    # 5. Decision
    if M_after < M_before:
        # Success - commit
        git_commit(f"LIFT-{lift_number}: {violation.id} {M_before:.2f}→{M_after:.2f}")
        log_lift(lift_number, M_before, M_after, repair)
        return LiftResult(success=True, delta_M=M_before - M_after)
    else:
        # Regression - rollback
        git_reset_hard()
        return LiftResult(success=False, reason="M_regressed")
```

### 4.2 MOBILE.md Format

```markdown
# VisionUX Naim Lift Log

## Project Metrics
- **Baseline M:** 1.82 (22 violations)
- **Current M:** 0.0 (0 violations)
- **Total Lifts:** 22
- **Total Weight:** 182kg
- **Success Rate:** 100%

---

## Lift History

### LIFT-001 @ 2026-03-18 21:45:32
- **Element:** `headerTitle` (Ana Sayfa)
- **Location:** (19, 59, 141, 95)
- **Violation:** Already compliant (16.48:1)
- **Action:** SKIP
- **M:** 1.82 → 1.82 (Δ 0.0)
- **Weight:** 0kg

### LIFT-002 @ 2026-03-18 21:47:15
- **Element:** `welcomeHeader` (Hoş Geldiniz)
- **Location:** (19, 138, 208, 179)
- **Before:** RGB(247,255,247) on RGB(76,176,80) = 2.7:1 ❌
- **After:** RGB(255,255,255) on RGB(56,142,60) = 4.95:1 ✅
- **Strategy:** adjust_background
- **Hue Shift:** 2° (preserved)
- **M:** 1.82 → 1.64 (Δ -0.18)
- **Weight:** 18kg 🏋️
- **Commit:** `a3f8d91`
- **Tests:** ✅ PASS

### LIFT-003 @ 2026-03-18 21:49:03
[continues...]
```

---

## 5. REACT NATIVE CODE GENERATION

### 5.1 Output Format

```typescript
/**
 * AUTO-GENERATED FIX - VisionUX Lift #002
 * Element: welcomeHeader
 * Contrast: 2.7:1 → 4.95:1 (+2.25)
 * Strategy: adjust_background
 * Date: 2026-03-18 21:47:15
 */

import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  welcomeHeader: {
    // Text color: Preserved
    color: '#FFFFFF',  // was: #F7FFF7 (minimal change)
    
    // Background: Darkened for contrast
    backgroundColor: '#388E3C',  // was: #4CB050 (-8% lightness)
    
    // Layout: Unchanged
    fontSize: 28,
    fontWeight: 'bold',
    padding: 16,
  },
  
  // WCAG 2.1 AA Compliance
  // ✅ Contrast Ratio: 4.95:1 (Target: 4.5:1)
  // ✅ M Metric Impact: -0.18 (1.82 → 1.64)
});

export default styles;
```

### 5.2 Integration Test

```typescript
// tests/lift_002.test.ts
describe('LIFT-002: welcomeHeader fix', () => {
  it('should meet WCAG AA contrast', () => {
    const textColor = '#FFFFFF';
    const bgColor = '#388E3C';
    
    const ratio = calculateContrast(textColor, bgColor);
    expect(ratio).toBeGreaterThanOrEqual(4.5);
  });
  
  it('should preserve brand hue', () => {
    const originalHue = rgbToHsl(76, 176, 80)[0];
    const fixedHue = rgbToHsl(56, 142, 60)[0];
    
    const hueShift = Math.abs(fixedHue - originalHue);
    expect(hueShift).toBeLessThan(15);
  });
});
```

---

## 6. CONSTRAINTS & GUARDRAILS

### 6.1 Immutable Rules
1. **Zero Regression:** M must decrease or stay same
2. **WCAG Compliance:** All fixes must reach ≥ 4.5:1
3. **Brand Integrity:** Hue shifts < 15°, Saturation ±20%
4. **Atomic Commits:** One lift = one fix = one commit
5. **Test Coverage:** Every lift has automated test

### 6.2 Rollback Triggers
- M metric increases
- Test suite fails
- Build breaks
- Manual override (emergency only)

### 6.3 Success Criteria (Project Complete)
- M = 0.0 (all elements compliant)
- 100% test pass rate
- Zero regressions in git history
- MOBILE.md complete with all lifts

---

## 7. DEPLOYMENT

### 7.1 Production Checklist
- [ ] All lifts logged in MOBILE.md
- [ ] M metric = 0.0
- [ ] Test coverage ≥ 95%
- [ ] Documentation complete
- [ ] React Native patches generated
- [ ] Before/after screenshots captured

### 7.2 Handoff Deliverables
1. `visionux_core.py` - Complete repair engine
2. `MOBILE.md` - Full lift history
3. `fixes/` - All React Native patches
4. `test_screenshots/` - Visual proof
5. `PROGRAM.md` - This specification

---

**Adherence:** This document is the single source of truth. Never deviate without explicit override.