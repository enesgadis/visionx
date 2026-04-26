# VisionUX - Form Submission Checklist

## 📋 FORM DOLUM BİLGİLERİ

### 1. Adınız ve Soyadınız
```
Enes Gadis
```

### 2. Google Stitch Tasarım Share Link
```
https://github.com/enesgadis/visionux/blob/main/STITCH_DESIGN.md

(Alternatif görsel mockup için: Text-based design specifications ile detaylı 4-screen mockup)
```

### 3. idea.md Dosyanızın Gist (PUBLIC) Linki
```
Şimdi oluşturulacak - GitHub üzerinden IDEA.md'yi public gist olarak yükle:
https://gist.github.com/enesgadis/[ID]

Dosya adı: VisionUX_IDEA_v2.0.md
İçerik: d:\visionx\IDEA.md (438 satır, complete IDEA standard)
```

### 4. Kurumsal/Öğrenci E-posta Adresiniz
```
enes5544686753@gmail.com
```

### 5. Projenizin Başlığı (Title)
```
VisionUX: Autonomous Mobile Accessibility Repair with LLM-Assisted Code Generation
```

### 6. Projenizin Karpathy LLM-wiki/Autoresearch ile İlişkisi
```
SEÇİM: "Otonom Araştırma Ajanları (Autoresearch)"

AÇIKLAMA:
VisionUX, Karpathy'nin Autoresearch metodolojisini WCAG erişilebilirlik alanına uygulayan 
ilk otonom ajan sistemidir. "NAIM Lift" disiplini ile 15 dakikalık sprint'lerde, 
metrik-driven (M-metric) bir şekilde regresyon olmaksızın (ratchet principle) 
kontrast ihlallerini tespit edip onarır. Her lift, Git commit ile atomik olarak 
kaydedilir ve MOBILE.md'de "weight lifted" (kg) metriği ile loglanır.

Autoresearch Prensipleri:
• Autonomous operation: İnsan müdahalesi olmadan çalışır
• Metric-driven: M = (1/N) * Σ max(0, 4.5 - C)
• Ratchet mechanism: M her lift'te azalır veya eşit kalır, asla artmaz
• Atomic operations: Her repair bir Git commit
• Self-documenting: MOBILE.md otomatik güncellenir

LLM Integration (Future):
• GPT-4V: Görsel context için (gradients, overlays)
• Code generation: React Native StyleSheet patches
• Semantic understanding: "Submit button" vs "decorative icon"
```

### 7. Projenizin Tahmini Zorluk Seviyesi
```
SEÇİM: 4 (Zor)

GEREKÇE:
• Computer vision (OCR + segmentation)
• Perceptual color science (CIE Delta-E 2000)
• Optimization (100-step binary search)
• K-Means clustering (gradient handling)
• Git workflow automation
• Mobile native code generation
• Multi-platform support (React Native/Flutter)
```

---

## 📂 DOSYA YÜKLEMELERİ

### IDEA.md → GitHub Gist

**Adımlar:**
1. GitHub'a giriş yap
2. https://gist.github.com/ → "Create new gist"
3. Filename: `VisionUX_IDEA_v2.0.md`
4. Content: `d:\visionx\IDEA.md` içeriğini kopyala
5. "Create public gist" tıkla
6. URL'yi kopyala ve forma yapıştır

**Gist Özellikleri:**
- 438 satır, Markdown formatted
- IDEA v2.0 standardında (thesis, problem, architecture, constraints, risks)
- Tüm mühendislik sorularına cevap verilmiş
- Karpathy Autoresearch metodolojisi ile uyumlu

### STITCH_DESIGN.md → GitHub

**Mevcut URL:**
```
https://github.com/enesgadis/visionux/blob/main/STITCH_DESIGN.md
```

**Alternatif (görsel mockup için):**
Eğer gerçek bir Figma/Excalidraw link gerekiyorsa:
- Excalidraw.com'da 4 screen mockup çiz
- Share link al
- VEYA mevcut text-based design'ı reference et

---

## ✅ KONTROL LİSTESİ

- [x] IDEA.md güncel (2026-04-26)
- [x] IDEA.md tüm standart bölümleri içeriyor
- [x] STITCH_DESIGN.md hazır (4 screen mockup)
- [x] GitHub'a push edildi (commit: 6819254)
- [ ] IDEA.md Gist olarak yüklenecek
- [ ] Form doldurulacak
- [ ] Deadline öncesi submit (26.04.2026 23:59)

---

## 📊 PROJE ÖZETİ (Form İçin)

**Problem:** 
Mevcut accessibility araçları (Lighthouse, axe-core) WCAG kontrast ihlallerini tespit eder 
ama otomatik onarım yapmaz. Tasarımcılar manuel olarak renk dener, developer'lar StyleSheet'e 
manuel yazar. 20-50 ihlal tipik üretim uygulamaları için 15-30 dakika/ihlal harcanır.

**Çözüm:** 
VisionUX, ekran görüntülerinden OCR ile text tespit eder, WCAG kontrast hesaplar, 
CIE Delta-E 2000 ile marka renklerini koruyarak minimal değişiklikle onarır, 
ve production-ready React Native kodu üretir. Tüm süreç ~30 saniye.

**Yenilik:** 
1. Mobil-native (web değil)
2. Marka koruması (Delta-E < 5.0)
3. Gradient handling (K-Means clustering)
4. Otonom (Autoresearch NAIM discipline)
5. Kod üretimi (StyleSheet patches)

**Sonuçlar:**
- Halısaha app: 22/22 ihlal düzeltildi (M: 1.46 → 0.0)
- Ortalama iyileştirme: +15.72:1/element
- Marka-güvenli onarımlar: %13.6 (ΔE < 5.0)
- Süre: 26 saniye (vs 2 saat manuel)

**Google Stitch Entegrasyonu:**
Stitch kullanıcı dikkat haritası sağlar (nereye bakıyorlar), VisionUX WCAG uyumluluk 
sağlar (neyi okuyabiliyorlar). Kombine priority matrix: 
(yüksek dikkat × yüksek ihlal) = kritik düzeltme önceliği.

---

## 🔗 LİNKLER

**GitHub Repo:**
https://github.com/enesgadis/visionux

**IDEA.md (Raw):**
https://raw.githubusercontent.com/enesgadis/visionux/main/IDEA.md

**STITCH_DESIGN.md:**
https://github.com/enesgadis/visionux/blob/main/STITCH_DESIGN.md

**README.md:**
https://github.com/enesgadis/visionux/blob/main/README.md

**MOBILE.md (Lift Log):**
https://github.com/enesgadis/visionux/blob/main/MOBILE.md

---

## 📧 E-POSTA TASLAK (Hocaya)

Konu: VisionUX - Google Stitch Entegrasyon Tasarımı Teslim

Sayın Nurettin Senyer Hocam,

VisionUX projesi için IDEA v2.0 dokümanını ve Google Stitch entegrasyon tasarımını 
hazırladım. Verdiğiniz feedback'ler temelinde:

1. IDEA.md'yi Karpathy standardına göre yeniden yazdım:
   - Thesis statement (tek cümle)
   - Problem definition (mevcut araçların neden yetersiz olduğu)
   - Detect → Analyze → Repair → Validate pipeline (I/O contracts ile)
   - Constraints & Risks (HIGH/MEDIUM/LOW tier'lı)
   - Tüm mühendislik sorularına cevap (segmentation, Delta-E, differentiation, M-metric)

2. Google Stitch entegrasyonu için detaylı tasarım dökümanı oluşturdum:
   - 4-screen mockup specifications
   - Priority matrix (attention × severity)
   - Combined workflow (26 saniye, vs 2 saat manuel)
   - API integration contracts

Linkler:
- GitHub: https://github.com/enesgadis/visionux
- IDEA.md: [Gist linki eklenecek]
- STITCH_DESIGN.md: https://github.com/enesgadis/visionux/blob/main/STITCH_DESIGN.md

Formu 26 Nisan 23:59'a kadar dolduracağım.

Saygılarımla,
Enes Gadis
Yazılım Mühendisliği, Samsun Üniversitesi
