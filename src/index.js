// Cloudflare Workers Stock Checker
// Zara, Bershka, Stradivarius stok takip sistemi

// Konfigürasyon (config.json'dan alınan veriler)
const STOCK_CONFIG = {
  urls: [
    {
      store: "zara", 
      url: "https://www.zara.com/tr/tr/desenli-kisa-tul-elbise-p05039132.html?v1=442763765&v2=2580270"
    },
    {
      store: "stradivarius", 
      url: "https://www.stradivarius.com/tr/pensli-ve-dokumlu-straight-fit-pantolon-l04562600"
    },
    {
      store: "zara",
      url: "https://www.zara.com/tr/tr/asimetrik-cift-t-shirt-p05644213.html?v1=441578999"
    },
    {
      store: "zara", 
      url: "https://www.zara.com/tr/tr/halter-strec-top-p00085339.html?v1=444436822"
    }
  ],
  sizes_to_check: ["36", "38", "S", "M"],
  sleep_min_seconds: 12,
  sleep_max_seconds: 22
};

// Telegram mesajı gönderme fonksiyonu
async function sendTelegramMessage(message, env) {
  if (!env.BOT_API || !env.CHAT_ID) {
    console.log("⚠️ Telegram credentials not found");
    return false;
  }

  const url = `https://api.telegram.org/bot${env.BOT_API}/sendMessage`;
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chat_id: env.CHAT_ID,
        text: message
      })
    });

    if (response.ok) {
      console.log("✅ Telegram message sent successfully");
      return true;
    } else {
      console.log("❌ Failed to send Telegram message:", await response.text());
      return false;
    }
  } catch (error) {
    console.log("❌ Telegram error:", error);
    return false;
  }
}

// User-Agent başlıkları (bot tespitini önlemek için)
const USER_AGENTS = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
];

// Rastgele User-Agent seç
function getRandomUserAgent() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

// Zara stok kontrolü
async function checkStockZara(url, sizesToCheck) {
  try {
    console.log(`🔍 Checking Zara: ${url}`);
    
    const response = await fetch(url, {
      headers: {
        'User-Agent': getRandomUserAgent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
      }
    });

    if (!response.ok) {
      console.log(`❌ Zara fetch failed: ${response.status}`);
      return null;
    }

    const html = await response.text();
    
    // Zara'da stok bilgisi JSON'da gömülü olarak geliyor
    // window.__INITIAL_STATE__ veya benzer bir yapıda bulabiliriz
    const jsonRegex = /window\.__INITIAL_STATE__\s*=\s*({.*?});/s;
    const match = html.match(jsonRegex);
    
    if (match) {
      try {
        const initialState = JSON.parse(match[1]);
        
        // Zara'nın JSON yapısında size bilgilerini ara
        // Bu yapı değişebilir, farklı yollar denememiz gerekebilir
        const product = initialState?.product || initialState?.products?.[0];
        
        if (product && product.detail && product.detail.colors) {
          for (const color of product.detail.colors) {
            if (color.sizes) {
              for (const size of color.sizes) {
                const sizeValue = size.value || size.name;
                if (sizesToCheck.includes(sizeValue) && size.availability === 'in_stock') {
                  console.log(`✅ Zara - ${sizeValue} size is in stock!`);
                  return sizeValue;
                }
              }
            }
          }
        }
      } catch (jsonError) {
        console.log("⚠️ Zara JSON parse error:", jsonError);
      }
    }
    
    // JSON yöntemi çalışmazsa HTML parsing dene
    // Zara genellikle size bilgilerini script tag'lerinde saklar
    const sizeRegex = /"sizes":\s*\[(.*?)\]/g;
    const sizeMatches = [...html.matchAll(sizeRegex)];
    
    for (const sizeMatch of sizeMatches) {
      try {
        const sizesJson = JSON.parse(`[${sizeMatch[1]}]`);
        for (const sizeData of sizesJson) {
          if (sizeData.value && sizesToCheck.includes(sizeData.value) && sizeData.availability === 'in_stock') {
            console.log(`✅ Zara - ${sizeData.value} size is in stock!`);
            return sizeData.value;
          }
        }
      } catch (e) {
        continue;
      }
    }
    
    console.log(`❌ Zara - No stock found for sizes: ${sizesToCheck.join(', ')}`);
    return null;
    
  } catch (error) {
    console.log(`❌ Zara error: ${error}`);
    return null;
  }
}

// Bershka stok kontrolü  
async function checkStockBershka(url, sizesToCheck) {
  try {
    console.log(`🔍 Checking Bershka: ${url}`);
    
    const response = await fetch(url, {
      headers: {
        'User-Agent': getRandomUserAgent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
      }
    });

    if (!response.ok) {
      console.log(`❌ Bershka fetch failed: ${response.status}`);
      return null;
    }

    const html = await response.text();
    
    // Bershka size selector pattern: [data-qa-anchor='sizeListItem']
    const sizeRegex = /data-qa-anchor=['"']sizeListItem['"].*?class=['"']([^'"]*?)['"].*?<span[^>]*class=['"'][^'"]*text__label[^'"]*['"][^>]*>([^<]+)</g;
    
    let sizeMatch;
    while ((sizeMatch = sizeRegex.exec(html)) !== null) {
      const [, className, sizeText] = sizeMatch;
      const sizeValue = sizeText.trim();
      
      if (sizesToCheck.includes(sizeValue)) {
        // is-disabled class yoksa stokta demektir
        if (!className.includes('is-disabled')) {
          console.log(`✅ Bershka - ${sizeValue} size is in stock!`);
          return sizeValue;
        }
      }
    }
    
    // Alternatif yöntem: JSON data arama
    const jsonRegex = /window\.__INITIAL_STATE__\s*=\s*({.*?});/s;
    const jsonMatch = html.match(jsonRegex);
    
    if (jsonMatch) {
      try {
        const initialState = JSON.parse(jsonMatch[1]);
        // Bershka JSON yapısında size bilgilerini ara
        if (initialState.product && initialState.product.sizes) {
          for (const size of initialState.product.sizes) {
            if (sizesToCheck.includes(size.value) && size.stock > 0) {
              console.log(`✅ Bershka - ${size.value} size is in stock!`);
              return size.value;
            }
          }
        }
      } catch (jsonError) {
        console.log("⚠️ Bershka JSON parse error:", jsonError);
      }
    }
    
    console.log(`❌ Bershka - No stock found for sizes: ${sizesToCheck.join(', ')}`);
    return null;
    
  } catch (error) {
    console.log(`❌ Bershka error: ${error}`);
    return null;
  }
}

// Stradivarius stok kontrolü
async function checkStockStradivarius(url, sizesToCheck) {
  try {
    console.log(`🔍 Checking Stradivarius: ${url}`);
    
    const response = await fetch(url, {
      headers: {
        'User-Agent': getRandomUserAgent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
      }
    });

    if (!response.ok) {
      console.log(`❌ Stradivarius fetch failed: ${response.status}`);
      return null;
    }

    const html = await response.text();
    
    // Stradivarius genellikle JSON'da stok bilgisi saklar
    const jsonRegex = /window\.__INITIAL_STATE__\s*=\s*({.*?});/s;
    const jsonMatch = html.match(jsonRegex);
    
    if (jsonMatch) {
      try {
        const initialState = JSON.parse(jsonMatch[1]);
        
        // Stradivarius JSON yapısında size bilgilerini ara
        const product = initialState?.product || initialState?.products?.[0];
        
        if (product && product.sizes) {
          for (const size of product.sizes) {
            const sizeValue = size.value || size.name || size.size;
            if (sizesToCheck.includes(sizeValue) && (size.stock > 0 || size.available === true)) {
              console.log(`✅ Stradivarius - ${sizeValue} size is in stock!`);
              return sizeValue;
            }
          }
        }
      } catch (jsonError) {
        console.log("⚠️ Stradivarius JSON parse error:", jsonError);
      }
    }
    
    // HTML parsing alternatifi
    const sizePatterns = [
      /data-qa-qualifier=['"']size-selector-sizes-size-label['"][^>]*>([^<]+).*?data-qa-action=['"']size-in-stock['"]|data-qa-action=['"']size-low-on-stock['"]/g,
      /class=['"'][^'"]*size[^'"]*['"][^>]*>([^<]+).*?(?!disabled|unavailable|out-of-stock)/gi
    ];
    
    for (const pattern of sizePatterns) {
      let match;
      while ((match = pattern.exec(html)) !== null) {
        const sizeValue = match[1].trim();
        if (sizesToCheck.includes(sizeValue)) {
          console.log(`✅ Stradivarius - ${sizeValue} size is in stock!`);
          return sizeValue;
        }
      }
    }
    
    console.log(`❌ Stradivarius - No stock found for sizes: ${sizesToCheck.join(', ')}`);
    return null;
    
  } catch (error) {
    console.log(`❌ Stradivarius error: ${error}`);
    return null;
  }
}

// Ana stok kontrolü fonksiyonu
async function checkStock(item, sizesToCheck) {
  const { store, url } = item;
  
  switch (store.toLowerCase()) {
    case 'zara':
      return await checkStockZara(url, sizesToCheck);
    case 'bershka':
      return await checkStockBershka(url, sizesToCheck);
    case 'stradivarius':
      return await checkStockStradivarius(url, sizesToCheck);
    default:
      console.log(`❌ Unsupported store: ${store}`);
      return null;
  }
}

// Ana stok takip fonksiyonu
async function runStockCheck(env) {
  console.log("🚀 Starting stock check...");
  
  for (const item of STOCK_CONFIG.urls) {
    try {
      console.log(`\n📋 Checking: ${item.store} - ${item.url}`);
      
      const sizeInStock = await checkStock(item, STOCK_CONFIG.sizes_to_check);
      
      if (sizeInStock) {
        const message = `🛍️ ${sizeInStock} beden stokta!!!!\nMağaza: ${item.store.toUpperCase()}\nLink: ${item.url}`;
        console.log(`🎉 STOCK FOUND: ${message}`);
        
        // Telegram mesajı gönder
        await sendTelegramMessage(message, env);
      } else {
        console.log(`❌ No stock found for ${item.store}`);
      }
      
      // Rate limiting için kısa bekleme
      await new Promise(resolve => setTimeout(resolve, 2000));
      
    } catch (error) {
      console.log(`❌ Error checking ${item.store}: ${error}`);
    }
  }
  
  console.log("✅ Stock check completed");
}

// Cloudflare Workers main handler
export default {
  // Cron trigger handler
  async scheduled(controller, env, ctx) {
    console.log("⏰ Cron triggered - running stock check");
    ctx.waitUntil(runStockCheck(env));
  },

  // HTTP request handler (test için)
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    if (url.pathname === '/test') {
      // Test endpoint
      ctx.waitUntil(runStockCheck(env));
      return new Response('Stock check started! Check logs for results.', {
        headers: { 'Content-Type': 'text/plain' }
      });
    }
    
    if (url.pathname === '/status') {
      return new Response(JSON.stringify({
        status: 'active',
        config: {
          stores: STOCK_CONFIG.urls.map(item => ({ store: item.store, url: item.url })),
          sizes: STOCK_CONFIG.sizes_to_check,
          cron: '*/10 * * * *'
        }
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return new Response('Stock Checker Worker\n\nEndpoints:\n- /test - Run manual stock check\n- /status - Check configuration', {
      headers: { 'Content-Type': 'text/plain' }
    });
  }
}; 