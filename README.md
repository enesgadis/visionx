# VisionUX - WCAG Contrast Checker

Mobil ekran görüntülerinde text-background kontrast oranlarını WCAG 2.1 standartlarına göre analiz eden Python tool.

## Özellikler

- PNG ekran görüntüsü analizi
- OCR ile otomatik text tespiti
- Text ve background renk çiftleri çıkarımı
- WCAG 2.1 kontrast oranı hesaplama (relative luminance formülü)
- WCAG AA/AAA uyumluluk kontrolü

## Kurulum

```bash
# Virtual environment oluştur (önerilen)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

**Not:** İlk çalıştırmada EasyOCR model dosyalarını (~80MB) indirecek.

## Kullanım

```bash
python wcag_contrast_checker.py <screenshot.png>
```

### Örnek

```bash
python wcag_contrast_checker.py screenshots/mobile_app.png
```

## Çıktı Formatı

Script her text elementi için şunları raporlar:

- **Text içeriği**: OCR ile tespit edilen text
- **Pozisyon**: Bounding box koordinatları
- **Text rengi**: RGB ve hex formatında
- **Background rengi**: RGB ve hex formatında
- **Kontrast oranı**: X:1 formatında
- **WCAG AA durumu**: PASS/FAIL (minimum 4.5:1 normal text için)
- **WCAG AAA durumu**: PASS/FAIL (minimum 7.0:1 normal text için)
- **OCR güven skoru**: 0.0-1.0 arası

## WCAG 2.1 Standartları

| Level | Normal Text | Large Text (18pt+ veya 14pt+ bold) |
|-------|-------------|-------------------------------------|
| AA    | 4.5:1       | 3.0:1                              |
| AAA   | 7.0:1       | 4.5:1                              |

## Teknik Detaylar

### Kontrast Hesaplama

WCAG 2.1'e göre relative luminance formülü:

```
L = 0.2126 × R + 0.7152 × G + 0.0722 × B
```

Her kanal (R, G, B) için normalizasyon:

```
if c ≤ 0.03928:
    c_linear = c / 12.92
else:
    c_linear = ((c + 0.055) / 1.055) ^ 2.4
```

Kontrast oranı:

```
contrast_ratio = (L1 + 0.05) / (L2 + 0.05)
```

L1: daha açık renk, L2: daha koyu renk

## Limitasyonlar

Mevcut versiyon (v0.1):
- Sadece İngilizce text (EasyOCR yapılandırmasında değiştirilebilir)
- Background color tespiti basitleştirilmiş (bbox etrafındaki piksellerden örnekleme)
- Gradient veya kompleks background'lar için approximation
- Large text tespiti yok (tüm text'ler normal kabul edilir)

## Roadmap

Sonraki versiyonlarda:
- Multi-language support
- Font size tespiti (large text için farklı threshold)
- LLM entegrasyonu: React Native/Flutter fix snippet üretimi
- Ground truth veri seti ile doğrulama
- Web UI

## Referanslar

- [WCAG 2.1 Contrast Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [Alibaba Page Agent](https://github.com/alibaba/page-agent)
- [Stagewise](https://github.com/stagewise-io/stagewise)

## Lisans

MIT License

## İletişim

Proje: VisionUX - Mobil UX Accessibility Checker
Geliştirici: Enes
Tarih: Mart 2026
