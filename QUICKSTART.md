# Quick Start

Bu script Python 3.8+ gerektirir.

## Windows Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Test screenshot oluştur
python create_test_screenshot.py

# Analiz çalıştır
python wcag_contrast_checker.py test_screenshots\sample_mobile_ui.png
```

## MacOS/Linux Kurulum

```bash
# Virtual environment oluştur (önerilen)
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Test screenshot oluştur
python create_test_screenshot.py

# Analiz çalıştır
python wcag_contrast_checker.py test_screenshots/sample_mobile_ui.png
```

## Not

İlk çalıştırmada EasyOCR model dosyalarını (~80MB) otomatik indirecektir.
