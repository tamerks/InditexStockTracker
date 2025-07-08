# 🛍️ Zara Stock Checker

Zara, Bershka ve Stradivarius mağazalarında otomatik stok takibi yapan Python projesi. GitHub Actions kullanarak cloud'da ücretsiz çalışır.

## ✨ Özellikler

- ⚡ **Süper Hızlı:** Her 5 dakikada bir stok kontrolü (GitHub Actions minimum)
- 🚀 **Optimize Performans:** ~2 dakikada execution, maximum speed
- 🌐 **Multi-Store:** Zara, Bershka, Stradivarius desteği  
- 👥 **Kişi Takibi:** Her ürün için kişi ismi belirtme ve bildirimde gösterme
- 📱 **Akıllı Bildirimler:** Stok bulunduğunda anında haber, spam yok
- 🗑️ **Otomatik Temizlik:** Bulunan ürünler listeden otomatik çıkar
- 🔒 **Bot Detection Bypass:** Selenium ile gerçek browser kullanımı
- ☁️ **Cloud Çalışma:** GitHub Actions ile ücretsiz hosting
- 🆓 **Tamamen Ücretsiz:** Public repo'da unlimited minutes

## 🚀 Kurulum

### 1. Repository'yi Fork Edin
Bu repository'yi kendi GitHub hesabınıza fork edin.

### 2. Telegram Bot Oluşturun
1. [@BotFather](https://t.me/botfather)'a `/newbot` gönderin
2. Bot token'ınızı kaydedin (örn: `1234567890:ABC...`)
3. Chat ID'nizi öğrenmek için [@userinfobot](https://t.me/userinfobot)'a mesaj gönderin

### 3. GitHub Secrets Ayarlayın
Repository Settings > Secrets and Variables > Actions:

- **BOT_API:** Telegram bot token'ınız
- **CHAT_ID:** Telegram chat ID'niz

### 4. Ürün URL'lerini Yapılandırın
`config.json` dosyasını düzenleyin:

```json
{
  "urls": [
    {
      "store": "zara",
      "url": "https://www.zara.com/tr/tr/urun-linki",
      "sizes": ["S", "M", "L"],
      "person": "Ahmet"
    },
    {
      "store": "bershka", 
      "url": "https://www.bershka.com/tr/tr/urun-linki",
      "sizes": ["36", "38"],
      "person": "Ayşe"
    }
  ],
  "sleep_min_seconds": 60,
  "sleep_max_seconds": 180
}
```

## 📁 Dosya Yapısı

```
├── .github/workflows/
│   └── stock-checker.yml      # GitHub Actions workflow
├── main_github.py            # Ana stock checker (GitHub Actions için)
├── main.py                   # Lokal kullanım için
├── scraperHelpers.py         # Scraping fonksiyonları  
├── config.json               # Konfigürasyon
└── requirements.txt          # Python dependencies
```

## 🔧 Kullanım

### Otomatik Çalışma
- GitHub Actions her 5 dakikada otomatik çalışır
- Stok bulunduğunda Telegram'a bildirim gönderir
- Bulunan ürünler otomatik olarak takip listesinden çıkarılır

### Manuel Test
1. Repository > Actions > "Zara Stock Checker"
2. "Run workflow" butonuna tıklayın
3. Log'ları takip edin

### Lokal Çalışma
```bash
# Dependencies yükle
pip install -r requirements.txt

# Tek seferlik kontrol
python main_github.py

# Sürekli çalışma (sonsuz döngü)
python main.py
```

## ⚙️ Konfigürasyon

### Desteklenen Mağazalar
- **Zara:** `"store": "zara"`
- **Bershka:** `"store": "bershka"`  
- **Stradivarius:** `"store": "stradivarius"`

### Konfigürasyon Detayları

#### **URL Alanları:**
- **store:** Mağaza adı (`"zara"`, `"bershka"`, `"stradivarius"`)
- **url:** Ürün linki
- **sizes:** Bu ürün için kontrol edilecek bedenler
- **person:** Ürünü takip eden kişinin ismi (Telegram mesajlarında görünür)

#### **Beden Formatları:**
- **Sayısal:** `"36", "38", "40"`
- **Harf:** `"XS", "S", "M", "L", "XL"`

#### **Sleep Ayarları:**
- **sleep_min_seconds:** Minimum bekleme süresi (saniye)
- **sleep_max_seconds:** Maksimum bekleme süresi (saniye)

### 💬 Telegram Bildirim Örneği

```
🛍️ STOK BULUNDU!

👤 Kişi: Ahmet
📏 Beden: M
🏪 Mağaza: ZARA
🔗 Ürün Linki
⏰ Zaman: 14:30:25

🗑️ Ürün takip listesinden çıkarıldı
```

## 📊 GitHub Actions Detayları

- **Çalışma Sıklığı:** Her 5 dakika (`*/5 * * * *`) - GitHub minimum limit
- **Execution Time:** ~2 dakika (süper optimize)
- **Timeout:** 8 dakika maksimum (GitHub Actions workflow limit)
- **Chrome:** Pre-installed, all features disabled for speed
- **Python:** 3.9 with cached dependencies
- **OS:** Ubuntu Latest
- **Auto-Remove:** Bulunan ürünler otomatik olarak config'den çıkarılır

## 🐛 Sorun Giderme

### Actions Log'larını Kontrol Edin
1. Repository > Actions
2. Son çalışmaya tıklayın
3. "Run stock checker" adımını açın

### Yaygın Sorunlar
- **Telegram mesajı gelmiyorsa:** BOT_API ve CHAT_ID secrets'larını kontrol edin
- **Stok bulamıyorsa:** URL'lerin güncel olduğundan emin olun
- **Actions çalışmıyorsa:** Repository'nin public olduğundan emin olun

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add some amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## ⚠️ Yasal Uyarı ve Sorumluluk Reddi

**ÖNEMLI:** Bu proje sadece **eğitim ve araştırma amaçlı**dır.

### 🚨 **Kullanım Sınırlamaları:**
- Bu araç yalnızca **kişisel, ticari olmayan** amaçlarla kullanılmalıdır
- Hedef sitelerin **Terms of Service**'ini ihlal edebilir
- Kullanıcı kendi sorumluluğunda hareket eder
- **Yasal sorumluluk** kullanıcıya aittir

### ⚖️ **Tavsiye Edilen Kullanım:**
- Satın almayı planladığınız **kendi ürünleriniz** için kullanın
- **Makul frekans**ta çalıştırın (günde birkaç kez)
- **Ticari amaçla kullanmayın**
- Sites'in **rate limiting**'ine uyun

### 🛡️ **Yasal Alternatifler:**
- Resmi mobil uygulamaları kullanın
- Newsletter'lara kaydolun  
- Resmi notification sistemlerini tercih edin
- Açık API'ler varsa onları kullanın

**Bu araçı kullanarak, tüm yasal riskleri kabul ettiğinizi beyan edersiniz.**

## ⚡ Performans Optimizasyonları

### **Speed Features:**
- **Sparse Checkout:** Sadece gerekli dosyalar indirilir
- **Cached Dependencies:** Python paketleri cache'den yüklenir  
- **Chrome Optimizations:** Images, CSS, JS disabled
- **Smart Timeouts:** 15s page load, 5s implicit wait
- **Fast Transitions:** 1-2s delays between checks

### **Smart Notifications:**
- **Instant Alerts:** Stok bulunduğunda anında Telegram
- **No Spam:** Stok yoksa sadece saatlik özet
- **Auto Remove:** Bulunan ürünler config'den otomatik silinir

---

**⚡ İpucu:** Süper hızlı (5 dakika), tamamen ücretsiz ve akıllı stok takip sistemi!
