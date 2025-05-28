# Video Akışı ve İşleme Uygulaması

Gerçek zamanlı RTMP video akışını alıp analiz eden, Google Cloud Video Intelligence API ile entegre çalışan ve analiz sonuçlarını MongoDB'ye kaydeden bir Python tabanlı video işleme uygulamasıdır.

---

## Özellikler

*  RTMP yayını alır ve görüntüleri işler (`rtmp_viewer.py`)
*  Google Cloud Video Intelligence API ile sahne analizi yapar (`gcloud_vision.py`)
*  MongoDB'ye analiz sonuçlarını kaydeder (`database.py`)
*  Docker kullanılmadan lokal olarak çalıştırılabilir
*  Gerçek zamanlı görüntü üzerine bounding box çizimi (`draw_boxes.py`)
*  HTML arayüz üzerinden video yayını ve analiz sonuçları izlenebilir (`live.html`)

---

##  Klasör Yapısı

```
Video-Akisi-ve-Isleme-Uygulamasi/
├── backend/
│   ├── app.py                 # Ana API sunucusu
│   ├── bbox_viewer.py         # Kutu görselleştirme
│   ├── rtmp_viewer.py         # RTMP akış yakalayıcı
│   ├── gcloud_vision.py       # GCP API çağrıları
│   ├── draw_boxes.py          # Görüntü üzerine kutu çizimi
│   ├── database.py            # MongoDB bağlantısı
│   ├── templates/live.html    # Basit arayüz
│   └── requirements.txt       # Python bağımlılıkları
├── credentials/
│   └── README.txt             # Anahtar dosyası açıklamaları (JSON dosyaları .gitignore’a eklenmeli!)
├── nginx-rtmp/
│   └── nginx-rtmp-win32/...  # RTMP sunucusu dosyaları (nginx.exe ve config)
```

---

##  Kurulum

### 1. Ortam Kurulumu

```bash
cd backend
pip install -r requirements.txt
```

### 2. RTMP Sunucusu (Windows için)

```bash
cd nginx-rtmp/nginx-rtmp-win32-1.2.1
start nginx.exe
```

OBS veya benzeri bir araçtan yayın başlatın:

```
rtmp://localhost/live
```

---

##  Uygulama Çalıştırma

```bash
cd backend
python app.py
```

Ardından tarayıcınızdan `http://localhost:8000/live` adresini ziyaret edin.

---

##  Güvenlik Uyarısı

> `credentials/` klasöründeki Google Cloud kimlik bilgileri `.gitignore` dosyasına eklenmeli ve GitHub'a gönderilmemelidir. Git commit geçmişinden temizlenmesi önerilir.

---

## 📷 API Entegrasyonu

Google Cloud Video Intelligence API'den etiket, nesne, zaman bilgisi alınır.
`gcloud_vision.py` içinde API çağrıları yapılır ve analiz sonucu JSON olarak döner.
