VisionUX: Stagewise Mobile UX Repair Agent
VisionUX, mobil uygulama arayüzlerini WCAG 2.1 erişilebilirlik standartlarına göre denetleyen ve deterministik analiz sonuçlarını LLM tabanlı "onarım reçetelerine" dönüştüren yüksek lisans düzeyinde bir Deneyim Mühendisliği (Experience Engineering) projesidir.

Proje Vizyonu ve Kapsam (MVP 2.0)
Nurettin Hoca'nın akademik geri bildirimleri doğrultusunda projenin kapsamı, 10 haftalık geliştirme sürecine uygun şekilde "Kontrast Erişilebilirliği ve Kaynak Kod Onarımı" üzerine odaklanmıştır.

Yeni MVP Akışı:

Screenshot (Mobil Ekran) ➔ Deterministic Audit (WCAG Analizi) ➔ Stagewise Repair (LLM Tabanlı Kod Onarımı)


Shutterstock
10 Haftalık Mühendislik Yol Haritası (Roadmap)
Hafta	Aşama (SDLC)	Hedeflenen Çıktı / Teslimat	Durum
1 (20 Mart)	Analiz & Prototip	Python Kontrast Scripti (EasyOCR & Pillow) ve Kapsam Daraltma.	TAMAMLANDI ✅
2	Veri Toplama	20 Ekranlık "Ground Truth" Mobil Veri Setinin Oluşturulması.	Planlandı
3	Geliştirme (I)	alibaba/page-agent mantığıyla Element Segmentasyonu iyileştirmesi.	Planlandı
4	Geliştirme (II)	LLM (GPT-4o/Gemini) API Entegrasyonu ve Prompt Engineering.	Planlandı
5	Test & Doğrulama	LLM tarafından üretilen Fix Snippet'lerin (RN/Flutter) manuel kontrolü.	Planlandı
6-8	Entegrasyon	Stagewise Onarım Mantığı ve Web Dashboard Geliştirme.	Planlandı
9-10	Finalizasyon	Benchmark Raporu, Teknik Dokümantasyon ve Tez Taslağı Teslimi.	Planlandı
 Akademik Analiz ve Benchmarking
VisionUX, pazardaki ve literatürdeki araçların boşluklarını kapatmak üzere kurgulanmıştır:

Google Stitch (Tahminleme): Stitch, kullanıcının nereye bakacağını (Heatmap) tahmin eder; VisionUX, bu odağın mühendislik sağlığını (kontrast) denetler.

UX Doctor (Web): UX Doctor web sayfalarında stagewise onarım yapar; VisionUX, bu vizyonu Mobile Native (View Hierarchy) bağlamına taşır.

Stagewise Mimari: Proje, sadece hata bulmakla kalmaz; stagewise-io mimarisinden esinlenerek kaynak kod seviyesinde onarım (Source Code Repair) önerileri üretir.

 Kritik Süreç Kuralı
"Experience Engineering Prensibi: Proje, teknik implementasyondan önce insancıl katmana (empati ve deneyim) odaklanır. Bu doğrultuda; Google Stitch üzerinden prototip onayı alınmaksızın kesinlikle uygulama (implementation) aşamasına geçilmeyecektir."

Teknik Detaylar (Core Engine)
Kontrast Hesaplama Modeli
VisionUX, subjektif yorumları bertaraf etmek için deterministik matematiksel modeller kullanır:

Bağıl Parlaklık (L): L=0.2126⋅R+0.7152⋅G+0.0722⋅B

Kontrast Oranı (C): C=(L1+0.05)/(L2+0.05)

Standartlar: WCAG AA (4.5:1) ve AAA (7.0:1) eşik değerleri.

Teknoloji Yığını
OCR Engine: EasyOCR (Deep Learning tabanlı metin tespiti)

Image Processing: Pillow (PIL) & NumPy

Code Generation: LLM-based Fix Snippet (React Native / Flutter)

Kurulum ve Çalıştırma
Bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Analizi başlat
python wcag_contrast_checker.py test_screenshots/sample_mobile_ui.png
 İletişim
Geliştirici: Enes Gadiş

Kurum: Samsun Üniversitesi, Yazılım Mühendisliği Anabilim Dalı

Tarih: Mart 2026
