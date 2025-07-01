# 🛍️ Zara Stock Checker

Zara, Bershka ve Stradivarius mağazalarında otomatik stok takibi yapan Python projesi. GitHub Actions kullanarak cloud'da ücretsiz çalışır.

## ✨ Özellikler

- 🔄 **Otomatik Kontrol:** Her 10 dakikada bir stok kontrolü
- 🌐 **Multi-Store:** Zara, Bershka, Stradivarius desteği  
- 📱 **Telegram Bildirimleri:** Stok bulunduğunda anında haber
- 🔒 **Bot Detection Bypass:** Selenium ile gerçek browser kullanımı
- ☁️ **Cloud Çalışma:** GitHub Actions ile ücretsiz hosting
- 🆓 **Tamamen Ücretsiz:** GitHub Actions 2000 dakika/ay limit

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
      "url": "https://www.zara.com/tr/tr/urun-linki"
    }
  ],
  "sizes_to_check": ["36", "38", "S", "M"]
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
- GitHub Actions her 10 dakikada otomatik çalışır
- Stok bulunduğunda Telegram'a bildirim gönderir

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

### Beden Formatları
- **Sayısal:** `"36", "38", "40"`
- **Harf:** `"XS", "S", "M", "L", "XL"`

## 📊 GitHub Actions Detayları

- **Çalışma Sıklığı:** Her 10 dakika (`*/10 * * * *`)
- **Timeout:** 15 dakika maksimum
- **Chrome Version:** Otomatik güncel
- **Python Version:** 3.9
- **OS:** Ubuntu Latest

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

## ⚠️ Yasal Uyarı

Bu araç sadece eğitim amaçlıdır. Web scraping yaparken hedef sitenin kullanım şartlarına uygun hareket edin.

---

**💡 İpucu:** GitHub Actions ile tamamen ücretsiz ve otomatik çalışan stok takip sistemi!
