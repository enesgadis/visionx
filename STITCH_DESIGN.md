# VisionUX + Google Stitch Integration Design

**Project:** VisionUX - Autonomous Mobile Accessibility Repair  
**Author:** Enes Gadis  
**Date:** 26 April 2026  
**Purpose:** Combined UX Flow Analysis + WCAG Compliance System

---

## 🎯 INTEGRATION VISION

**Problem:** Google Stitch predicts where users look, but not what they can/can't read.

**Solution:** VisionUX + Stitch = Complete UX + Accessibility Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│                   UNIFIED UX DASHBOARD                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐         ┌──────────────────┐        │
│  │  GOOGLE STITCH   │   +     │    VISIONUX      │        │
│  │                  │         │                  │        │
│  │  • User Intent   │         │  • WCAG Detect   │        │
│  │  • Flow Analysis │         │  • Auto Repair   │        │
│  │  • Attention Map │         │  • Code Gen      │        │
│  └──────────────────┘         └──────────────────┘        │
│                                                             │
│              ↓                          ↓                   │
│    ┌─────────────────────────────────────────┐            │
│    │   COMBINED PRIORITY MATRIX              │            │
│    │                                         │            │
│    │   High Attention + WCAG Fail = 🔴      │            │
│    │   High Attention + WCAG Pass = 🟢      │            │
│    │   Low Attention + WCAG Fail  = 🟡      │            │
│    └─────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 STITCH DESIGN MOCKUP COMPONENTS

### 1. Mobile App Screenshot Analysis View

**Layout:** Split-screen comparison

```
┌─────────────────────────────────────────────────────────────┐
│  ORIGINAL SCREEN              │    FIXED + ANNOTATED         │
├───────────────────────────────┼──────────────────────────────┤
│                               │                              │
│  [Screenshot]                 │  [Screenshot]                │
│                               │                              │
│  Stitch Overlay:              │  VisionUX Overlay:           │
│  • Red circles = User focus   │  • Yellow boxes = Violations │
│  • Heat map (0-100%)          │  • Green checks = Fixed      │
│                               │  • Contrast ratios shown     │
│                               │                              │
│  🔴 "Giriş Yap" button        │  🟢 Fixed: 2.7:1 → 4.6:1    │
│     Attention: 87%            │     ΔE: 1.93 (brand-safe)   │
│                               │                              │
└───────────────────────────────┴──────────────────────────────┘
```

### 2. Priority Matrix (Quadrant View)

**X-axis:** User Attention (Stitch score 0-100)  
**Y-axis:** WCAG Severity (Contrast deficit)

```
        High Severity
            ↑
            |
  🟡 Medium │  🔴 CRITICAL
  Priority  │  (Fix First)
            |
  ─────────┼─────────────→ High Attention
            |
  🟢 Low    │  🟡 Medium
  Priority  │  Priority
            |
            ↓
```

**Example Plot:**
- **"Giriş Yap" button:** (87% attention, 1.8 deficit) → 🔴 Critical
- **"Hesabım" nav icon:** (45% attention, 0.5 deficit) → 🟡 Medium
- **Footer link:** (12% attention, 0.2 deficit) → 🟢 Low

### 3. Repair Timeline (Stagewise View)

```
┌─────────────────────────────────────────────────────────────┐
│  REPAIR WORKFLOW                                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Stage 1: STITCH ANALYSIS                                  │
│  ├─ Input: 5 screenshots (login → home → search)          │
│  ├─ Output: 12 elements with high attention               │
│  └─ Duration: 2 seconds                                    │
│                                                             │
│  Stage 2: VISIONUX SCAN                                    │
│  ├─ Input: Same 5 screenshots                             │
│  ├─ Output: 22 WCAG violations detected                   │
│  └─ Duration: 8 seconds                                    │
│                                                             │
│  Stage 3: PRIORITY MERGE                                   │
│  ├─ Cross-reference: 8 violations on high-attention items │
│  ├─ Priority queue: [Critical: 8, Medium: 10, Low: 4]    │
│  └─ Duration: 1 second                                     │
│                                                             │
│  Stage 4: AUTO-REPAIR                                      │
│  ├─ VisionUX repairs 8 critical violations                │
│  ├─ M-metric: 1.46 → 0.52 (partial fix)                  │
│  └─ Duration: 12 seconds                                   │
│                                                             │
│  Stage 5: STITCH VALIDATION                                │
│  ├─ Re-analyze: Do fixes break UX flow?                   │
│  ├─ Result: ✅ Flow intact (95% confidence)               │
│  └─ Duration: 3 seconds                                    │
│                                                             │
│  Stage 6: CODE EXPORT                                      │
│  ├─ Generate: accessibility_fixes.tsx                     │
│  └─ Status: Ready for PR                                   │
│                                                             │
│  TOTAL TIME: 26 seconds                                    │
│  MANUAL EQUIVALENT: ~2 hours (designer + dev)              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 INTEGRATION WORKFLOW (Step-by-Step)

### User Journey

1. **Upload Screenshots**
   - User drags 5 mobile screens into dashboard
   - Auto-detects platform (iOS/Android/React Native)

2. **Dual Analysis (Parallel)**
   - **Stitch:** Runs attention prediction model
   - **VisionUX:** Runs WCAG contrast detection
   - Both complete in ~10 seconds

3. **Combined Report**
   - Dashboard shows:
     - Priority matrix (quadrant view)
     - Element list sorted by (attention × severity)
     - Side-by-side before/after previews

4. **Interactive Repair**
   - User clicks "Fix Critical" button
   - VisionUX auto-repairs top 8 violations
   - Live preview updates in real-time

5. **Validation**
   - Stitch re-runs flow analysis
   - Checks: "Does button color change affect CTA?"
   - Result: ✅ "Submit button still highest attention"

6. **Export**
   - Download `accessibility_fixes.tsx`
   - Get Figma plugin export (future)
   - Copy/paste into codebase

---

## 📐 STITCH DESIGN SPECIFICATIONS

### Screen 1: Upload & Analysis

**Purpose:** Entry point for users

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  VisionUX + Stitch Dashboard                    [Settings]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│         ┌─────────────────────────────────────┐            │
│         │                                     │            │
│         │    📱 Drag screenshots here         │            │
│         │       or click to upload            │            │
│         │                                     │            │
│         │    Supported: PNG, JPEG             │            │
│         │    Max 10 screens per analysis      │            │
│         │                                     │            │
│         └─────────────────────────────────────┘            │
│                                                             │
│  Quick Start:                                              │
│  • Upload login screen → Submit button accessibility       │
│  • Upload home screen → Navigation contrast issues         │
│                                                             │
│  Recent Analyses:                                          │
│  • Halısaha App (22 fixes) - 26 Apr 2026                  │
│  • Sample UI (4 fixes) - 17 Apr 2026                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Screen 2: Combined Analysis Results

**Purpose:** Show Stitch + VisionUX insights

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  Analysis: Halısaha Mobile App          [Export] [Fix All] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 SUMMARY                                                 │
│  ├─ Screens analyzed: 5                                    │
│  ├─ Elements detected: 47                                  │
│  ├─ High-attention elements: 12 (Stitch)                  │
│  ├─ WCAG violations: 22 (VisionUX)                        │
│  └─ Critical fixes needed: 8                               │
│                                                             │
│  🎯 PRIORITY MATRIX                                         │
│                                                             │
│    High Severity                                           │
│      │                                                      │
│   🟡 │  🔴 🔴 🔴  ← 8 Critical                             │
│      │  🔴 🔴 🔴                                            │
│   🟢 │─────────────────→ Attention                         │
│      │  🟡 🟡                                               │
│                                                             │
│  📋 ELEMENT LIST (sorted by priority)                      │
│                                                             │
│  1. 🔴 "Giriş Yap" Button                                  │
│     Current: 2.70:1 | Target: 4.5:1 | Attention: 87%      │
│     [Preview] [Fix Now] [Skip]                             │
│                                                             │
│  2. 🔴 "Hesabını Oluştur" Link                             │
│     Current: 2.96:1 | Target: 4.5:1 | Attention: 78%      │
│     [Preview] [Fix Now] [Skip]                             │
│                                                             │
│  3. 🔴 Navigation Icon (Home)                              │
│     Current: 2.30:1 | Target: 4.5:1 | Attention: 72%      │
│     [Preview] [Fix Now] [Skip]                             │
│                                                             │
│  [Show all 22 violations]                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Screen 3: Repair Preview

**Purpose:** Interactive fix with live preview

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  Fixing: "Giriş Yap" Button                    [< Back]     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BEFORE                          AFTER                      │
│  ┌─────────────────┐           ┌─────────────────┐        │
│  │                 │           │                 │        │
│  │  [Giriş Yap]   │           │  [Giriş Yap]   │        │
│  │  ^^^^^^^^^^^^^^ │           │  ^^^^^^^^^^^^^^ │        │
│  │  #F7FFF7 on     │           │  #313331 on     │        │
│  │  #4CB050        │           │  #4CB050        │        │
│  │                 │           │                 │        │
│  │  Contrast:      │           │  Contrast:      │        │
│  │  2.70:1 ❌      │           │  4.63:1 ✅      │        │
│  │                 │           │                 │        │
│  └─────────────────┘           └─────────────────┘        │
│                                                             │
│  📊 METRICS                                                 │
│  • Improvement: +71.5%                                     │
│  • Delta-E: 1.93 (brand-safe 🟢)                          │
│  • Strategy: darken_text                                   │
│  • Stitch impact: Attention unchanged (87%)                │
│                                                             │
│  💾 CODE PATCH                                              │
│  ```typescript                                             │
│  GirisYap_Button: {                                        │
│    color: '#313331',  // was: #f7fff7                      │
│    backgroundColor: '#4cb050',  // preserved               │
│    // Contrast: 2.70:1 → 4.63:1 (+71.5%)                  │
│  }                                                          │
│  ```                                                        │
│                                                             │
│  [Apply Fix] [Try Alternative] [Reject]                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Screen 4: Export Results

**Purpose:** Deliver production-ready code

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  Export: Halısaha Accessibility Fixes          [Download]   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ REPAIR COMPLETE                                         │
│                                                             │
│  📊 Summary:                                                │
│  • Elements fixed: 22/22 (100%)                            │
│  • M-metric: 1.46 → 0.0 (perfect compliance)              │
│  • Average improvement: +15.72:1 per element              │
│  • Brand-safe repairs: 3 (ΔE < 5.0)                       │
│  • Total time: 26 seconds                                  │
│                                                             │
│  📂 Files Generated:                                        │
│  • accessibility_fixes.tsx (255 lines)                     │
│  • before_after_screenshots.zip                            │
│  • MOBILE.md (lift log)                                    │
│  • repair_report.pdf                                       │
│                                                             │
│  🔗 Integration:                                            │
│  • React Native: Merge with existing StyleSheet           │
│  • Stitch validation: ✅ UX flow intact                    │
│  • Lighthouse score: 100/100 (accessibility)              │
│                                                             │
│  📋 Next Steps:                                             │
│  1. Create PR with fixes                                   │
│  2. Run unit tests                                         │
│  3. Deploy to staging                                      │
│  4. Re-scan with VisionUX                                  │
│                                                             │
│  [Download All] [Create PR] [Share Report]                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 VISUAL DESIGN GUIDELINES

### Color Palette

**Primary:**
- Stitch Blue: `#4285F4` (Google brand)
- VisionUX Green: `#4CB050` (accessibility pass)

**Status Colors:**
- Critical: `#EA4335` (red)
- Warning: `#FBBC04` (yellow)
- Success: `#34A853` (green)
- Neutral: `#5F6368` (gray)

### Typography

- **Headings:** Inter Bold, 24px
- **Body:** Inter Regular, 16px
- **Code:** JetBrains Mono, 14px
- **Metrics:** Inter Semibold, 18px

### Spacing

- Card padding: 24px
- Element gap: 16px
- Button height: 48px
- Border radius: 8px

---

## 🔧 TECHNICAL INTEGRATION POINTS

### Data Flow

```typescript
// 1. User uploads screenshot
const screenshot = await uploadFile('halısaha_login.png');

// 2. Parallel analysis
const [stitchResult, visionuxResult] = await Promise.all([
  stitch.analyzeAttention(screenshot),
  visionux.detectViolations(screenshot)
]);

// 3. Merge results
const priorityQueue = mergePriorities(
  stitchResult.attentionMap,  // {elementId: attentionScore}
  visionuxResult.violations    // {elementId: contrastDeficit}
);

// 4. Sort by combined score
priorityQueue.sort((a, b) => 
  (b.attention * b.deficit) - (a.attention * a.deficit)
);

// 5. Auto-repair critical items
const fixes = await visionux.autoRepair(
  priorityQueue.filter(item => item.severity === 'critical')
);

// 6. Validate with Stitch
const validation = await stitch.validateFlow(screenshot, fixes);

// 7. Export
return {
  patches: fixes.styleSheet,
  report: { before: visionuxResult.M, after: fixes.M },
  stitchValidation: validation.flowIntact
};
```

### API Contracts

**Stitch Input:**
```json
{
  "screenshot_url": "https://...",
  "platform": "mobile",
  "analysis_type": "attention"
}
```

**Stitch Output:**
```json
{
  "elements": [
    {
      "id": "giris_yap_button",
      "bbox": [120, 450, 280, 520],
      "attention_score": 0.87,
      "predicted_action": "tap"
    }
  ]
}
```

**VisionUX Output:**
```json
{
  "violations": [
    {
      "element_id": "giris_yap_button",
      "text": "Giriş Yap",
      "text_color": "#f7fff7",
      "bg_color": "#4cb050",
      "ratio": 2.70,
      "deficit": 1.80
    }
  ],
  "M_metric": 1.46
}
```

**Combined Priority:**
```json
{
  "priority_queue": [
    {
      "element_id": "giris_yap_button",
      "attention": 0.87,
      "deficit": 1.80,
      "severity": "critical",
      "combined_score": 1.566
    }
  ]
}
```

---

## 📈 EXPECTED OUTCOMES

### Quantitative Impact

| Metric | Before Integration | After Integration |
|--------|-------------------|------------------|
| **Designer time** | 2-3 hours/app | 5 minutes/app |
| **Fix accuracy** | ~70% (manual) | ~95% (automated) |
| **Brand-safe repairs** | Requires designer | Automatic (ΔE < 5) |
| **UX flow validation** | Manual testing | Automatic (Stitch) |

### User Value Proposition

**For Designers:**
- "Fix accessibility without breaking brand identity"
- See Stitch attention maps + WCAG violations in one view

**For Developers:**
- "Get production-ready StyleSheet patches in 30 seconds"
- Integrate with CI/CD (PR automation)

**For Product Managers:**
- "Ensure legal compliance (WCAG 2.1 AA) on critical user paths"
- Prioritize fixes by user impact (Stitch attention)

---

## 🎯 STITCH DESIGN LINK

**[Click here to view interactive Stitch design]**

*(Note: Link will be generated after creating the actual Stitch mockup)*

---

## 📝 NOTES FOR IMPLEMENTATION

1. **Stitch API Integration:**
   - Request access to Google Stitch API
   - Alternative: Use open-source attention models (e.g., Saliency maps)

2. **Dashboard Technology:**
   - Frontend: React + TypeScript
   - Backend: FastAPI (Python)
   - Database: PostgreSQL (user history)

3. **Real-time Preview:**
   - Use Canvas API for live color changes
   - WebSocket for progress updates

4. **Export Formats:**
   - React Native: `.tsx`
   - Flutter: `.dart`
   - Figma: Plugin integration (future)

---

**Design Status:** Ready for review  
**Next Step:** Create interactive Stitch mockup and submit to advisor  
**Deadline:** 26 April 2026, 23:59
