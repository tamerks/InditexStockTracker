# 🚀 Cloudflare Workers Stok Takip Sistemi

Zara, Bershka ve Stradivarius için 7/24 çalışan **ücretsiz** stok takip sistemi.

## ✨ Özellikler

- 🆓 **Tamamen ücretsiz** (Cloudflare Workers Free Plan)
- ⏰ **7/24 otomatik çalışma** (her 10 dakikada kontrol)
- 📱 **Telegram bildirimleri**
- 🛍️ **3 mağaza desteği**: Zara, Bershka, Stradivarius
- 📏 **Çoklu beden takibi**: 36, 38, S, M
- 🌐 **Sunucusuz (Serverless)** - bakım gerektirmez

## 🔧 Kurulum

### 1. Ön Gereksinimler

```bash
# Node.js kurulu olmalı (zaten var)
node --version

# Wrangler CLI kur
npm install -g wrangler
```

### 2. Cloudflare Hesabı

1. [Cloudflare.com](https://cloudflare.com)'da ücretsiz hesap oluşturun
2. Workers sekmesine gidin

### 3. Proje Kurulumu

```bash
# Bu klasöre gidin
cd cloudflare-stock-checker

# Bağımlılıkları yükleyin
npm install -g wrangler

# Cloudflare'e giriş yapın
wrangler login
```

### 4. Environment Variables (Çevresel Değişkenler)

Telegram bot bilgilerinizi Cloudflare'de ayarlayın:

```bash
# Bot tokenınızı ekleyin
wrangler secret put BOT_API

# Chat ID'nizi ekleyin  
wrangler secret put CHAT_ID
```

**Veya Cloudflare Dashboard'dan:**
1. Workers & Pages > stock-checker > Settings > Variables
2. "Environment Variables" bölümüne ekleyin:
   - `BOT_API`: `7431981826:AAE3JlyFphcVFPCMHyqGXMYAvylIHF6NdZo`
   - `CHAT_ID`: `503294787`

### 5. Deploy (Dağıtım)

```bash
# Worker'ı Cloudflare'ye yükle
wrangler deploy
```

## 🎯 Kullanım

### Otomatik Çalışma
- Worker her 10 dakikada otomatik çalışır
- Stok bulunca Telegram mesajı gönderir

### Manuel Test
```bash
# Canlı URL (deploy sonrası alacaksınız):
curl https://stock-checker.your-subdomain.workers.dev/test
```

### Durum Kontrolü
```bash
curl https://stock-checker.your-subdomain.workers.dev/status
```

## 📱 Telegram Mesaj Örneği

```
🛍️ 38 beden stokta!!!!
Mağaza: ZARA
Link: https://www.zara.com/tr/tr/...
```

## ⚙️ Yapılandırma

Ürün listesini değiştirmek için `src/index.js` dosyasındaki `STOCK_CONFIG` bölümünü düzenleyin:

```javascript
const STOCK_CONFIG = {
  urls: [
    {
      store: "zara",
      url: "https://www.zara.com/tr/tr/yeni-urun-linki"
    }
  ],
  sizes_to_check: ["36", "38", "S", "M", "L"]
};
```

## 🔍 Logları Görme

```bash
# Canlı logları izle
wrangler tail
```

## 📊 Maliyet

- **Cloudflare Workers Free Plan:**
  - 100,000 request/gün (yeterli)
  - 10ms CPU time/request
  - **Tamamen ücretsiz!**

## 🆚 Selenium vs Cloudflare Workers

| Özellik | Selenium (Eski) | Cloudflare Workers (Yeni) |
|---------|-----------------|---------------------------|
| **Maliyet** | Bilgisayar açık | Ücretsiz |
| **Çalışma** | Manual | 7/24 Otomatik |
| **Hız** | Yavaş (tarayıcı) | Hızlı (direkt HTTP) |
| **Güvenilirlik** | Orta | Yüksek |
| **Bakım** | Gerekli | Sıfır |

## 🔧 Troubleshooting

### Worker çalışmıyor
```bash
wrangler tail  # Logları kontrol et
```

### Environment variables eksik
```bash
wrangler secret list  # Mevcut secret'ları gör
wrangler secret put BOT_API  # Yeniden ekle
```

### Deploy sorunu
```bash
wrangler login  # Yeniden giriş yap
wrangler deploy  # Tekrar deploy et
```

## 🎉 Başarı!

Artık sisteminiz 7/24 çalışıyor! Stok bulunduğunda Telegram'dan bildirim alacaksınız.

## 📞 Destek

Sorun yaşarsanız `wrangler tail` komutuyla logları kontrol edin veya bana ulaşın.
