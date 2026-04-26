# VisionUX: Autonomous Mobile Accessibility Repair System

**Version:** 2.0  
**Date:** 2026-04-26  
**Status:** Active Development (MVP Complete)  
**Author:** Enes Gadis  
**Advisor:** Nurettin Senyer  
**Institution:** Samsun University, Software Engineering

---

## THESIS (Single Sentence)

VisionUX autonomously detects and repairs WCAG 2.1 contrast violations in mobile UI screenshots by combining computer vision segmentation, perceptual color science (CIE Delta-E 2000), and minimal-change optimization to generate production-ready StyleSheet patches that preserve brand identity while ensuring AA compliance (4.5:1 minimum contrast).

---

## 1. PROBLEM DEFINITION

### 1.1 The Gap in Current Tooling

**Existing accessibility tools (Lighthouse, axe-core, Android Accessibility Scanner) detect violations but do not repair them:**

| Tool | What It Does | What It Doesn't Do |
|------|-------------|-------------------|
| Lighthouse Accessibility | Reports contrast violations with specific ratios | ❌ No repair suggestions |
| axe-core | Identifies elements failing WCAG | ❌ No color recommendations |
| Android Scanner | Screenshots problematic areas | ❌ No StyleSheet generation |
| UX Doctor (Web) | Web-specific automated fixes | ❌ No mobile native support |
| Google Stitch | UX flow analysis, user intent prediction | ❌ No WCAG compliance checking |

**The missing capability:** Autonomous repair with brand preservation and code generation.

### 1.2 Real-World Pain Points

1. **Manual Labor:** Designer identifies violation → tries colors manually → developer implements → QA tests → repeat
   - **Time cost:** 15-30 minutes per violation
   - **Scale:** 20-50 violations typical in production apps

2. **Brand Breakage:** Naive fixes (e.g., all text → black) destroy visual identity
   - **Example:** Halısaha app - green brand color (#4CB050) requires careful text selection

3. **Gradient Blindness:** Tools report single color pairs but miss worst-case scenarios
   - **Example:** Text over image backgrounds - where's the lowest contrast?

4. **No Integration:** Fixes live in PDF reports, not codebase
   - **Gap:** Design → Code translation requires manual StyleSheet writing

### 1.3 Why Now?

- **WCAG 2.1 AA is legally required** (EU Accessibility Act 2025, ADA Section 508)
- **Mobile-first design** means more apps need native (React Native/Flutter) fixes
- **Color science mature:** CIE Delta-E 2000 provides perceptual distance metrics
- **Vision models accessible:** EasyOCR, ScreenshotAnalyzer enable text detection

---

## 2. SOLUTION ARCHITECTURE

### 2.1 System Overview

```
Input: Mobile Screenshot (PNG/JPEG)
    ↓
[1. DETECTION PIPELINE]
    → EasyOCR: Text bounding boxes + confidence scores
    → Enhanced extraction: Expand bbox ±10px for background sampling
    → K-Means clustering: Dominant background color (handles gradients)
    ↓
[2. ANALYSIS PIPELINE]
    → WCAG calculator: Relative luminance + contrast ratio
    → Violation filter: C < 4.5:1 flagged
    → M-metric: M = (1/N) * Σ max(0, 4.5 - C_actual)
    ↓
[3. REPAIR PIPELINE]
    → Strategy selection: darken_text | lighten_text | adjust_bg | force_maximum
    → Delta-E constraint: Minimize perceptual distance (prefer ΔE < 5.0)
    → Binary search: 100-step interpolation for optimal color
    ↓
[4. CODE GENERATION]
    → React Native StyleSheet.create() with HEX colors
    → Inline comments: before/after ratios + Delta-E
    → Export as .tsx file
    ↓
Output: Production-ready patches + MOBILE.md lift log
```

### 2.2 Input/Output Contracts

#### Input Specification
```typescript
interface ScreenshotInput {
  path: string;              // PNG/JPEG file path
  resolution: {width: number, height: number};
  colorSpace: 'sRGB';        // Required for WCAG calculations
  minTextSize?: number;      // Default: 14pt (OCR filter)
}
```

#### Output Specification
```typescript
interface RepairOutput {
  violations_detected: number;
  violations_fixed: number;
  M_before: number;          // Baseline metric
  M_after: number;           // Post-repair metric (target: 0.0)
  
  patches: StyleSheetPatch[];  // React Native code
  lift_log: LiftEntry[];       // MOBILE.md records
  
  metadata: {
    timestamp: ISO8601;
    total_weight: number;      // kg (NAIM metric)
    strategy_distribution: {[key: string]: number};
  };
}

interface StyleSheetPatch {
  element_id: string;
  element_text: string;
  
  original_text_color: HEX;
  fixed_text_color: HEX;
  original_bg_color: HEX;
  fixed_bg_color: HEX;
  
  ratio_before: number;
  ratio_after: number;
  delta_e: number;           // CIE 2000 perceptual distance
  
  strategy: 'darken_text' | 'lighten_text' | 'adjust_bg' | 'force_maximum';
  code: string;              // TypeScript StyleSheet snippet
}
```

---

## 3. TECHNICAL DEEP DIVE

### 3.1 Segmentation Strategy

**Problem:** OCR gives text bounding box, but background may be gradient/image/overlay.

**Solution: Three-tier approach**

```python
# Tier 1: Tight bbox for text color
text_region = image[y_min:y_max, x_min:x_max]
text_color = np.median(text_region[luminance < threshold])

# Tier 2: Expanded bbox + K-Means for background
bg_region = image[y_min-10:y_max+10, x_min-10:x_max+10]
kmeans = KMeans(n_clusters=3)
background_color = kmeans.fit(border_pixels).cluster_centers_[dominant]

# Tier 3: Worst-case for gradients
all_bg_colors = np.unique(bg_region)
worst_contrast = min([calculate_ratio(text, bg) for bg in all_bg_colors])
target_bg = bg_with_worst_contrast
```

**Edge Cases Handled:**
- ✅ Gradient backgrounds → K-Means finds dominant + worst-case
- ✅ Text over images → Border sampling avoids text pixels
- ✅ Semi-transparent overlays → OCR confidence filter (>0.7)
- ✅ Anti-aliasing artifacts → Percentile filtering (10th/90th)

### 3.2 Brand Identity Preservation

**Problem:** Naive fix (all text → black) destroys brand colors.

**Solution: CIE Delta-E 2000 constraint**

```python
# Delta-E thresholds (perceptual color science)
ΔE < 1.0:  # Not perceptible by human eyes
ΔE < 5.0:  # Brand-safe (preferred) 🟢
ΔE < 10.0: # Acceptable fallback 🟡
ΔE > 10.0: # Significant change (only if necessary) 🔴

# Optimization loop
for lightness in linspace(0, 1, 100):
    candidate = adjust_lightness(original, lightness)
    ratio = calculate_contrast(candidate, background)
    delta_e = cie_delta_e_2000(original, candidate)
    
    if ratio >= 4.5 and delta_e < 5.0:
        return candidate  # Brand-safe repair found
```

**Real Example (Halısaha app):**
- Green header: #F7FFF7 on #4CB050 = 2.7:1 ❌
- Naive fix: #000000 (black) = 21:1 but ΔE=66 🔴
- Smart fix: #313331 (dark gray) = 4.63:1 and ΔE=1.93 🟢

### 3.3 Metric: M = (1/N) * Σ max(0, 4.5 - C_actual)

**Why this formula?**

```
Problem with absolute distance:
M = (1/N) * Σ |4.5 - C|
→ Element with 21:1 contributes Δ=16.5 (false penalty)

Solution with deficit-only:
M = (1/N) * Σ max(0, 4.5 - C)
→ Element with 21:1 contributes 0 (no penalty)
→ Element with 3.0:1 contributes 1.5 (real deficit)

Target: M = 0 means 100% compliance
```

**Naim Lift Interpretation:**
- ΔM = M_before - M_after
- Weight = ΔM * 100 kg
- Each lift logged in MOBILE.md with timestamp

---

## 4. DIFFERENTIATION FROM EXISTING TOOLS

| Feature | VisionUX | Lighthouse | axe-core | UX Doctor | Stitch |
|---------|----------|------------|----------|-----------|--------|
| **Detects violations** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Generates repair code** | ✅ | ❌ | ❌ | ✅ (web only) | ❌ |
| **Mobile native support** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Brand preservation (ΔE)** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Gradient handling** | ✅ (K-Means) | ❌ | ❌ | ❌ | ❌ |
| **Autonomous operation** | ✅ (NAIM) | ❌ | ❌ | Partial | ❌ |
| **UX flow analysis** | ❌ | ❌ | ❌ | ❌ | ✅ |

**Value Proposition:**
VisionUX = Lighthouse (detection) + UX Doctor (repair) + Mobile Native + Brand Science + Autonomous Workflow

**Integration with Stitch:**
- Stitch → User intent + flow analysis
- VisionUX → WCAG compliance + automated fixes
- **Synergy:** Stitch validates UX, VisionUX ensures accessibility

---

## 5. CONSTRAINTS & RISKS

### 5.1 Technical Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| **OCR accuracy** | Text detection fails on stylized fonts | • EasyOCR confidence threshold (0.7+)<br>• Fallback to manual bbox annotation |
| **Screenshot-only** | Cannot access source code directly | • Generate StyleSheet patches for manual merge<br>• Future: Parse React Native AST |
| **Static analysis** | Misses dynamic color changes (dark mode) | • Require separate screenshots per theme<br>• Document: "Run per color scheme" |
| **Brand palette unknown** | Delta-E optimizes blindly without brand constraints | • Accept brand color CSV (future)<br>• For now: Delta-E < 5 is conservative |

### 5.2 Risk Assessment

#### HIGH RISK: False Positives (Over-correction)
- **Scenario:** Tool flags compliant element due to OCR error
- **Probability:** 5-10% (based on EasyOCR confidence scores)
- **Impact:** Designer rejects patches, manual review required
- **Mitigation:**
  1. Confidence threshold: Only process OCR results > 0.7
  2. Human-in-loop: Generate patches as PR, require approval
  3. Visual diff: Side-by-side before/after screenshots

#### MEDIUM RISK: Code Integration Breakage
- **Scenario:** Generated StyleSheet conflicts with existing styles
- **Probability:** 20-30% (CSS specificity, platform differences)
- **Impact:** Build fails or visual regression
- **Mitigation:**
  1. Clear docs: "Merge with `style={[existing, fixes.elementName]}`"
  2. Test generation: Auto-create unit tests for each patch
  3. Version lock: Specify React Native / Flutter version

#### LOW RISK: Brand Rejection
- **Scenario:** Delta-E < 5 repair still deemed "off-brand"
- **Probability:** 10-15%
- **Impact:** Requires manual designer override
- **Mitigation:**
  1. Provide 3 alternatives (ΔE < 5, < 10, maximum contrast)
  2. Export to Figma: Designer tweaks in design tool first

### 5.3 What This Project Does NOT Do

❌ **No source code parsing** - Works on screenshots, not React Native JSX  
❌ **No live app integration** - Not a runtime library  
❌ **No UX flow analysis** - Use Google Stitch for user journey  
❌ **No dark mode auto-detection** - Requires separate screenshots  
❌ **No font size detection** - Treats all text as normal (14pt+)  
❌ **No multi-language OCR** - English only (EasyOCR limitation)  

---

## 6. SUCCESS CRITERIA

### 6.1 Quantitative Metrics

| Metric | Target | Current Status |
|--------|--------|---------------|
| **M = 0** (Perfect compliance) | 100% of test apps | ✅ Halısaha: 1.46 → 0.0 |
| **Delta-E < 5** (Brand-safe) | >60% of repairs | 🟡 13.6% (3/22) |
| **Precision** (True violations) | >90% | 🔄 Pending ground truth |
| **Recall** (Caught all violations) | >95% | 🔄 Pending ground truth |
| **Time savings** | <2 min per violation | ✅ ~30s avg |

### 6.2 Qualitative Goals

1. **Designer Approval:** Patches accepted without modification (>70% target)
2. **Developer Integration:** StyleSheet merges without build errors (>90% target)
3. **QA Validation:** Lighthouse re-scan shows 0 violations (100% target)

### 6.3 Deliverables (10-Week Timeline)

- [x] **Week 1 (Mar 18-20):** Python contrast checker MVP - **DONE**
- [x] **Week 2 (Apr 17):** Autonomous repair engine (NAIM LIFT-001, 002, 003) - **DONE**
- [ ] **Week 3-4:** Ground truth dataset (20 production screenshots)
- [ ] **Week 5-6:** LLM integration (GPT-4V for visual context)
- [ ] **Week 7:** Google Stitch prototype design + approval
- [ ] **Week 8:** Web UI (drag-drop screenshot → instant patches)
- [ ] **Week 9:** Flutter support (expand beyond React Native)
- [ ] **Week 10:** Final report + thesis defense

---

## 7. PRIOR ART & REFERENCES

### 7.1 Academic Foundation

- **WCAG 2.1 Specification** (W3C, 2018): Relative luminance formula, 4.5:1 threshold
- **CIE Delta-E 2000** (Sharma et al., 2005): Perceptual color difference in LAB space
- **Karpathy Autoresearch** (2022): Autonomous research methodology, ratchet mechanism

### 7.2 Industry Tools

- **Google Stitch:** UX flow prediction (no accessibility focus)
- **UX Doctor:** Web accessibility repair (our mobile inspiration)
- **alibaba/page-agent:** Semantic web agent (DOM parsing reference)
- **stagewise-io:** Element selection pipeline (fix workflow reference)

### 7.3 Novelty Claims

1. **First mobile-native autonomous repair tool** (Lighthouse/axe don't repair)
2. **CIE Delta-E brand preservation** (UX Doctor doesn't use color science)
3. **K-Means gradient handling** (tools assume solid backgrounds)
4. **NAIM discipline for accessibility** (first application to WCAG domain)

---

## 8. OPEN QUESTIONS & FUTURE WORK

### 8.1 Unresolved Engineering Problems

1. **Icon accessibility:** Tool handles text, but icon color contrast also matters
   - **Explore:** Visual embedding similarity for "important" icons

2. **Dynamic theming:** Apps with 5+ color schemes need batch processing
   - **Explore:** Figma Variables API for automated theme export

3. **Localization:** Text length changes in i18n may cause layout-based contrast issues
   - **Explore:** Multi-language screenshot matrix

### 8.2 Research Extensions

1. **Predictive repair:** Given design mockup, proactively fix before implementation
2. **Semantic contrast:** Not just luminance - consider colorblind simulation
3. **Video accessibility:** Apply to video content (subtitles, overlays)

---

## 9. IMPLEMENTATION STATUS

### 9.1 Completed Components

```
visionux/
├── wcag_contrast_checker.py   ✅ Detection (OCR + WCAG math)
├── visionux_core.py           ✅ Repair engine (4 strategies + Delta-E)
├── MOBILE.md                  ✅ NAIM lift log
├── PROGRAM.md                 ✅ Technical spec
├── .cursorrules               ✅ Autonomous agent constitution
└── fixes/
    └── halısaha_*.tsx         ✅ Production patches (22 repairs)
```

### 9.2 GitHub Repository

**URL:** https://github.com/enesgadis/visionux  
**Status:** Public, 8 commits, 1,474kg total weight lifted  
**Test Coverage:** Manual (pending pytest suite)

---

## 10. NEXT IMMEDIATE ACTIONS

### Before Google Stitch Design:

1. **Ground Truth Validation** (Week 3)
   - Collect 20 production app screenshots
   - Manual annotation: true violations vs. false positives
   - Calculate precision/recall

2. **Expand Test Suite**
   - Gradient backgrounds (5 cases)
   - Text over images (5 cases)
   - Semi-transparent overlays (3 cases)
   - Edge cases: white on white, black on black

3. **Documentation Refinement**
   - API reference for `visionux_core.py`
   - Tutorial: "Your First Repair in 5 Minutes"
   - Video demo for thesis defense

### Google Stitch Integration Plan:

**Workflow:**
1. Stitch → Analyze UX flow, identify key screens
2. VisionUX → Scan those screens for WCAG violations
3. Stitch → Validate repairs don't break user journey
4. Combined report → "UX + Accessibility Score"

**Design Mockup To Create:**
- Unified dashboard showing both Stitch insights + VisionUX fixes
- Side-by-side: Original flow → Fixed flow (with contrast overlays)
- Get approval from advisor before implementation

---

## APPENDIX A: GLOSSARY

- **M-Metric:** Health metric, M = (1/N) * Σ max(0, 4.5 - C_actual), target M=0
- **Delta-E (ΔE):** CIE 2000 perceptual color distance, <5.0 is brand-safe
- **NAIM Lift:** 15-minute atomic repair operation, logged as weight (kg)
- **Ratchet:** Never regress principle (M must decrease or stay same)
- **WCAG AA:** 4.5:1 minimum contrast for normal text, 3:1 for large text

---

**Document Status:** IDEA v2.0 Complete  
**Last Updated:** 2026-04-26  
**Next Review:** After Google Stitch integration approval
