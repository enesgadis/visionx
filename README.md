# VisionUX: Autonomous Mobile Accessibility Repair System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![WCAG 2.1 AA](https://img.shields.io/badge/WCAG-2.1%20AA-green.svg)](https://www.w3.org/WAI/WCAG21/quickref/)

**Autonomous contrast violation detection and repair for mobile UI with brand preservation.**

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run on a screenshot
python visionux_core.py test_screenshots/your_app.png

# View generated fixes
cat fixes/your_app_accessibility_fixes.tsx
```

**Output:** React Native StyleSheet patches ready for production.

---

## What It Does

VisionUX takes a mobile app screenshot and:
1. **Detects** WCAG 2.1 contrast violations (text that's too light/dark)
2. **Repairs** them automatically with minimal color changes
3. **Generates** production-ready React Native code
4. **Preserves** your brand colors (using CIE Delta-E 2000)

### Example

**Before:** Green header with 2.7:1 contrast ❌  
**After:** Dark gray text with 4.63:1 contrast ✅ (only ΔE=1.93 perceptual change)

```typescript
// Generated fix
HosGeldiniz_000: {
  color: '#313331',  // was: #f7fff7
  backgroundColor: '#4cb050',  // preserved
  // Contrast: 2.70:1 → 4.63:1 (71.5% improvement)
}
```

---

## Why VisionUX?

| Tool | Detects | Repairs | Mobile | Brand-Safe |
|------|---------|---------|--------|------------|
| Lighthouse | ✅ | ❌ | ❌ | ❌ |
| axe-core | ✅ | ❌ | ❌ | ❌ |
| **VisionUX** | ✅ | ✅ | ✅ | ✅ (Delta-E) |

**Unique Features:**
- 🎨 **Brand preservation:** CIE Delta-E 2000 ensures minimal perceptual change
- 🌈 **Gradient handling:** K-Means clustering for complex backgrounds
- 📱 **Mobile-native:** Generates React Native/Flutter code
- 🤖 **Autonomous:** Naim Lift discipline with rollback protection

---

## Architecture

```
Screenshot → OCR Detection → WCAG Analysis → Color Optimization → Code Generation
               ↓                  ↓                ↓                    ↓
          EasyOCR          M-Metric Calc     Delta-E < 5.0      StyleSheet.tsx
```

**Key Components:**
- `wcag_contrast_checker.py` - Detection engine
- `visionux_core.py` - Repair engine with 4 strategies
- `ColorScience` class - CIE Delta-E 2000 + K-Means
- `MOBILE.md` - Naim Lift log (1,474kg total weight)

---

## Installation

### Requirements
- Python 3.12+
- 2GB RAM (for EasyOCR models)

### Setup

```bash
git clone https://github.com/enesgadis/visionux.git
cd visionux

# Install dependencies
pip install -r requirements.txt

# First run downloads EasyOCR models (~80MB)
python visionux_core.py test_screenshots/sample_mobile_ui.png
```

---

## Usage

### Basic

```bash
python visionux_core.py path/to/screenshot.png
```

### With Custom Threshold

```python
from visionux_core import VisionUXCore

core = VisionUXCore('screenshot.png', target_ratio=7.0)  # AAA standard
results = core.run_autonomous_repair()
```

### Output Structure

```
fixes/
  └── screenshot_accessibility_fixes.tsx  # React Native patches

MOBILE.md  # Updated with lift history
```

---

## Technical Details

### WCAG Formula

```python
# Relative luminance
L = 0.2126*R + 0.7152*G + 0.0722*B  # gamma corrected

# Contrast ratio
C = (L_lighter + 0.05) / (L_darker + 0.05)

# Compliance
AA: C ≥ 4.5:1  (normal text)
AAA: C ≥ 7.0:1  (normal text)
```

### M-Metric

```python
M = (1/N) * Σ max(0, 4.5 - C_actual)
```

- **M = 0:** Perfect compliance
- **M > 0:** Average deficit from threshold
- **Target:** Monotonically decrease M with each repair

### Delta-E Constraint

```
ΔE < 1.0:  Imperceptible
ΔE < 5.0:  Brand-safe (preferred) 🟢
ΔE < 10.0: Acceptable fallback 🟡
ΔE > 10.0: Significant change 🔴
```

---

## Real-World Results

### Halısaha Mobile App (Production Test)

- **Violations detected:** 22
- **Violations fixed:** 22 (100%)
- **M metric:** 1.46 → 0.0
- **Average improvement:** +15.72:1 per element
- **Strategy distribution:** 86% force_maximum, 14% minimal change
- **Time:** ~30 seconds total

**Notable Repairs:**
1. Green header: 2.70 → 4.63 (minimal, ΔE=1.93)
2. Navigation icons: 2.30-2.96 → 21.0 (maximum)
3. Card text: 3.14-3.66 → 21.0 (force)

---

## Documentation

- **[IDEA.md](IDEA.md)** - Complete project specification (IDEA v2.0 format)
- **[PROGRAM.md](PROGRAM.md)** - Technical architecture
- **[MOBILE.md](MOBILE.md)** - Naim Lift history (1,474kg lifted)
- **[TEST_RESULTS.md](TEST_RESULTS.md)** - Validation results

---

## Project Status

**MVP Complete (20 March 2026 Deadline ✅)**

### Completed Lifts

- **LIFT-001:** Auto-repair algorithm (1,328kg)
- **LIFT-002:** Real-world optimization (146kg)
- **LIFT-003:** Advanced color science (Delta-E + K-Means)

### Current Metrics

- M = 0.0 (perfect compliance on test apps)
- 100% success rate (0 regressions)
- 22/22 violations fixed (halısaha app)

---

## Roadmap

- [ ] **Week 3-4:** Ground truth dataset (20 screenshots)
- [ ] **Week 5-6:** LLM integration (GPT-4V)
- [ ] **Week 7:** Google Stitch integration design
- [ ] **Week 8:** Web UI (drag-drop interface)
- [ ] **Week 9:** Flutter support
- [ ] **Week 10:** Thesis defense

---

## Contributing

This is an academic thesis project (10-week MVP). Contributions welcome after May 2026.

### Development Setup

```bash
# Run tests
python wcag_contrast_checker.py test_screenshots/sample_mobile_ui.png

# Generate patches
python lift_002_execute.py

# Check code style
# (pytest suite pending)
```

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

## References

- **WCAG 2.1 Specification:** [W3C](https://www.w3.org/WAI/WCAG21/quickref/)
- **CIE Delta-E 2000:** Sharma et al. (2005)
- **Karpathy Autoresearch:** [Blog](https://karpathy.github.io/)
- **Inspired by:** UX Doctor, alibaba/page-agent, stagewise-io

---

## Citation

```bibtex
@software{visionux2026,
  author = {Gadis, Enes},
  title = {VisionUX: Autonomous Mobile Accessibility Repair System},
  year = {2026},
  url = {https://github.com/enesgadis/visionux}
}
```

---

## Contact

**Author:** Enes Gadis  
**Advisor:** Nurettin Senyer  
**Institution:** Samsun University  
**Date:** March-May 2026

---

**Built with:** Python • EasyOCR • OpenCV • scikit-learn • colormath • React Native
