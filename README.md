# VisionUX: Stagewise Mobile UX Repair Agent

VisionUX, mobil uygulama arayüzlerini WCAG 2.1 (Web Content Accessibility Guidelines) standartlarına göre denetleyen ve elde edilen deterministik verileri LLM (Large Language Model) mimarisi üzerinden otomatik onarım reçetelerine dönüştüren akademik bir Deneyim Mühendisliği (Experience Engineering) projesidir.

## 1. Proje Vizyonu ve Kapsam (MVP 2.0)

Projenin kapsamı, akademik geri bildirimler doğrultusunda 10 haftalık geliştirme sürecine uygun olarak "Kontrast Erişilebilirliği ve Kaynak Kod Onarımı" üzerine odaklanmıştır. Sistemin temel çalışma akışı şu şekildedir:

1. Girdi: Mobil arayüz ekran görüntüsü (Screenshot).
2. Denetim: Deterministik matematiksel modellerle kontrast analizi (Audit).
3. Onarım: Tespit edilen hataların stagewise mimariyle kod seviyesinde onarılması (Repair).

## 2. Mühendislik Yol Haritası (Roadmap)

Proje, Yazılım Geliştirme Yaşam Döngüsü (SDLC) prensiplerine uygun olarak aşağıdaki takvimle ilerlemektedir:

| Hafta | Aşama (SDLC) | Hedeflenen Çıktı / Teslimat | Durum |
| :--- | :--- | :--- | :--- |
| 1 (20 Mart) | Analiz & Prototip | Python Kontrast Scripti (EasyOCR & Pillow) ve Kapsam Daraltma. | TAMAMLANDI |
| 2 | Veri Toplama | 20 Ekranlık "Ground Truth" Mobil Veri Setinin Oluşturulması. | Planlandı |
| 3 | Geliştirme (I) | alibaba/page-agent mantığıyla Element Segmentasyonu iyileştirmesi. | Planlandı |
| 4 | Geliştirme (II) | LLM (GPT-4o/Gemini) API Entegrasyonu ve Prompt Engineering. | Planlandı |
| 5 | Test & Doğrulama | LLM tarafından üretilen Fix Snippet'lerin (RN/Flutter) manuel kontrolü. | Planlandı |
| 6-8 | Entegrasyon | Stagewise Onarım Mantığı ve Web Dashboard Geliştirme. | Planlandı |
| 9-10 | Finalizasyon | Benchmark Raporu, Teknik Dokümantasyon ve Tez Taslağı Teslimi. | Planlandı |

## 3. Akademik Analiz ve Benchmarking

VisionUX, literatürdeki ve endüstrideki mevcut araçların sunduğu boşlukları kapatmayı hedefler:

* Google Stitch (Tahminleme): Stitch, kullanıcı odağını (Attention) tahmin ederken; VisionUX bu odak noktalarının teknik sağlığını (Erişilebilirlik) denetler.
* UX Doctor (Web): Mevcut UX Doctor çözümleri yalnızca web tabanlı DOM yapısını kapsar. VisionUX, bu vizyonu Mobile Native (View Hierarchy) bağlamına taşır.
* Stagewise Mimari: Proje, stagewise-io mimarisinden esinlenerek kaynak kod seviyesinde onarım önerileri üretir.

Kritik Süreç Kuralı: Proje prensibi gereği, Google Stitch üzerinden prototip onayı alınmaksızın uygulama (implementation) aşamasına geçilmemesi esastır.

## 4. Teknik Detaylar (Core Engine)

### 4.1. Kontrast Hesaplama Modeli
Sistem, subjektif yorumları bertaraf etmek için aşağıdaki deterministik modelleri kullanır:

* Bağıl Parlaklık (Relative Luminance):
  L = 0.2126 * R + 0.7152 * G + 0.0722 * B
* Kontrast Oranı (Contrast Ratio):
  C = (L1 + 0.05) / (L2 + 0.05)
* Standartlar: WCAG AA (4.5:1) ve AAA (7.0:1) eşik değerleri.

### 4.2. Teknoloji Yığını
* OCR Engine: EasyOCR (Deep Learning tabanlı metin tespiti).
* Görüntü İşleme: Pillow (PIL) ve NumPy.
* Kod Üretimi: LLM-based Fix Snippet (React Native / Flutter).

## 5. Kurulum ve Proje Çalıştırma

### 5.1. Gereksinimler
Sistemin çalışması için Python 3.9+ sürümü gereklidir. Gerekli kütüphaneleri yüklemek için:

pip install -r requirements.txt

### 5.2. Kurulum Adımları
Depoyu klonlayın:
git clone https://github.com/enesgadis/visionx.git
cd visionx

Sanal ortam oluşturun (Önerilen):
python -m venv venv

Windows için:
venv\Scripts\activate

Linux/Mac için:
source venv/bin/activate

### 5.3. Çalıştırma
Analiz motorunu bir ekran görüntüsü üzerinde test etmek için aşağıdaki komutu kullanın:


python wcag_contrast_checker.py <dosya_yolu/ekran_goruntusu.png>

## 6. İletişim
Geliştirici: Enes Gadiş

Kurum: Samsun Üniversitesi, Yazılım Mühendisliği Anabilim Dalı

Tarih: Mart 2026
