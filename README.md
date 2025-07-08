# 🛍️ Inditex Stock Checker

Automated stock tracking Python project for Inditex stores (Zara, Bershka, Stradivarius). Runs for free in the cloud using GitHub Actions.

## ✨ Features

- ⚡ **Super Fast:** Stock check every 5 minutes (GitHub Actions minimum)
- 🚀 **Optimized Performance:** ~2 minute execution, maximum speed
- 🌐 **Multi-Store:** Zara, Bershka, Stradivarius support
- 👥 **Person Tracking:** Specify person name for each product and show in notifications
- 📱 **Smart Notifications:** Instant alerts when stock found, no spam
- 🗑️ **Auto Cleanup:** Found products automatically removed from list
- 🔒 **Bot Detection Bypass:** Real browser usage with Selenium
- ☁️ **Cloud Operation:** Free hosting with GitHub Actions
- 🆓 **Completely Free:** Unlimited minutes on public repo

## 🚀 Setup

### 1. Fork the Repository
Fork this repository to your own GitHub account.

### 2. Create Telegram Bot
1. Send `/newbot` to [@BotFather](https://t.me/botfather)
2. Save your bot token (e.g., `1234567890:ABC...`)
3. Get your Chat ID by messaging [@userinfobot](https://t.me/userinfobot)

### 3. Setup GitHub Secrets
Repository Settings > Secrets and Variables > Actions:

- **BOT_API:** Your Telegram bot token
- **CHAT_ID:** Your Telegram chat ID

### 4. Configure Product URLs
Edit the `config.json` file:

```json
{
  "urls": [
    {
      "store": "zara",
      "url": "https://www.zara.com/tr/tr/product-link",
      "sizes": ["S", "M", "L"],
      "person": "John"
    },
    {
      "store": "bershka", 
      "url": "https://www.bershka.com/tr/tr/product-link",
      "sizes": ["36", "38"],
      "person": "Jane"
    }
  ],
  "sleep_min_seconds": 60,
  "sleep_max_seconds": 180
}
```

## 📁 File Structure

```
├── .github/workflows/
│   └── stock-checker.yml      # GitHub Actions workflow
├── main_github.py            # Main stock checker (for GitHub Actions)
├── main.py                   # For local usage
├── scraperHelpers.py         # Scraping functions  
├── config.json               # Configuration
└── requirements.txt          # Python dependencies
```

## 🔧 Usage

### Automatic Operation
- GitHub Actions runs automatically every 5 minutes
- Sends Telegram notification when stock is found
- Found products are automatically removed from tracking list

### Manual Test
1. Repository > Actions > "Inditex Stock Checker"
2. Click "Run workflow" button
3. Follow the logs

### Local Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Single check
python main_github.py

# Continuous operation (infinite loop)
python main.py
```

## ⚙️ Configuration

### Supported Stores
- **Zara:** `"store": "zara"`
- **Bershka:** `"store": "bershka"`  
- **Stradivarius:** `"store": "stradivarius"`

### Configuration Details

#### **URL Fields:**
- **store:** Store name (`"zara"`, `"bershka"`, `"stradivarius"`)
- **url:** Product link
- **sizes:** Sizes to check for this product
- **person:** Name of person tracking the product (shown in Telegram messages)

#### **Size Formats:**
- **Numeric:** `"36", "38", "40"`
- **Letter:** `"XS", "S", "M", "L", "XL"`

#### **Sleep Settings:**
- **sleep_min_seconds:** Minimum wait time (seconds)
- **sleep_max_seconds:** Maximum wait time (seconds)

### 💬 Telegram Notification Example

```
🛍️ STOCK FOUND!

👤 Person: John
📏 Size: M
🏪 Store: ZARA
🔗 Product Link
⏰ Time: 14:30:25

🗑️ Product removed from tracking list
```

## 📊 GitHub Actions Details

- **Frequency:** Every 5 minutes (`*/5 * * * *`) - GitHub minimum limit
- **Execution Time:** ~2 minutes (super optimized)
- **Timeout:** 8 minutes maximum (GitHub Actions workflow limit)
- **Chrome:** Pre-installed, all features disabled for speed
- **Python:** 3.9 with cached dependencies
- **OS:** Ubuntu Latest
- **Auto-Remove:** Found products automatically removed from config

## 🐛 Troubleshooting

### Check Actions Logs
1. Repository > Actions
2. Click on latest run
3. Open "Run stock checker" step

### Common Issues
- **No Telegram messages:** Check BOT_API and CHAT_ID secrets
- **Stock not found:** Ensure URLs are current
- **Actions not running:** Ensure repository is public

## 🤝 Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add some amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Legal Notice and Disclaimer

**IMPORTANT:** This project is for **educational and research purposes only**.

### 🚨 **Usage Limitations:**
- This tool should only be used for **personal, non-commercial** purposes
- May violate target sites' **Terms of Service**
- User acts at their own responsibility
- **Legal liability** belongs to the user

### ⚖️ **Recommended Usage:**
- Use for **your own products** you plan to purchase
- Run at **reasonable frequency** (few times per day)
- **Do not use commercially**
- Respect sites' **rate limiting**

### 🛡️ **Legal Alternatives:**
- Use official mobile apps
- Subscribe to newsletters
- Use official notification systems
- Use open APIs if available

**By using this tool, you acknowledge accepting all legal risks.**

## ⚡ Performance Optimizations

### **Speed Features:**
- **Sparse Checkout:** Only necessary files downloaded
- **Cached Dependencies:** Python packages loaded from cache
- **Chrome Optimizations:** Images, CSS, JS disabled
- **Smart Timeouts:** 15s page load, 5s implicit wait
- **Fast Transitions:** 1-2s delays between checks

### **Smart Notifications:**
- **Instant Alerts:** Immediate Telegram when stock found
- **No Spam:** Only hourly summary if no stock
- **Auto Remove:** Found products automatically deleted from config

---

**⚡ Tip:** Super fast (5 minutes), completely free and smart stock tracking system!

---

# 🛍️ Inditex Stok Takipçisi

Inditex mağazalarında (Zara, Bershka, Stradivarius) otomatik stok takibi yapan Python projesi. GitHub Actions kullanarak cloud'da ücretsiz çalışır.

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
1. Repository > Actions > "Inditex Stock Checker"
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
