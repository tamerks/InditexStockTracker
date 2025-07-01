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
      url: "https://www.stradivarius.com/tr/tr/pensli-ve-dokumlu-straight-fit-pantolon-l04562600"
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

// Gelişmiş User-Agent havuzu (gerçek browser'lardan)
const ADVANCED_USER_AGENTS = [
  // Chrome on Windows
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
  
  // Chrome on Mac
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
  
  // Edge
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
  
  // Firefox
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
  
  // Safari
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
];

// Rastgele User-Agent seç ve uyumlu headers oluştur
function generateRealisticHeaders() {
  const userAgent = ADVANCED_USER_AGENTS[Math.floor(Math.random() * ADVANCED_USER_AGENTS.length)];
  
  // User-Agent'a göre uyumlu headers
  const isChrome = userAgent.includes('Chrome') && !userAgent.includes('Edg');
  const isFirefox = userAgent.includes('Firefox');
  const isSafari = userAgent.includes('Safari') && !userAgent.includes('Chrome');
  const isEdge = userAgent.includes('Edg');
  
  let headers = {
    'User-Agent': userAgent,
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
  };

  if (isChrome || isEdge) {
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7';
    headers['Sec-Ch-Ua'] = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"';
    headers['Sec-Ch-Ua-Mobile'] = '?0';
    headers['Sec-Ch-Ua-Platform'] = '"Windows"';
    headers['Sec-Fetch-Dest'] = 'document';
    headers['Sec-Fetch-Mode'] = 'navigate';
    headers['Sec-Fetch-Site'] = 'none';
    headers['Sec-Fetch-User'] = '?1';
  } else if (isFirefox) {
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8';
  } else if (isSafari) {
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8';
  }

  return headers;
}

// Session manager - çerezleri takip et
class SessionManager {
  constructor() {
    this.cookies = new Map();
    this.sessionId = Math.random().toString(36).substring(2);
  }

  updateCookies(response) {
    const setCookieHeader = response.headers.get('set-cookie');
    if (setCookieHeader) {
      // Set-Cookie header'ını parse et
      const cookies = setCookieHeader.split(',');
      cookies.forEach(cookie => {
        const [nameValue] = cookie.split(';');
        const [name, value] = nameValue.split('=');
        if (name && value) {
          this.cookies.set(name.trim(), value.trim());
        }
      });
    }
  }

  getCookieString() {
    const cookieArray = [];
    for (const [name, value] of this.cookies.entries()) {
      cookieArray.push(`${name}=${value}`);
    }
    return cookieArray.join('; ');
  }
}

// Gelişmiş delay fonksiyonu - insan davranışını taklit et
function humanLikeDelay() {
  // İnsan benzeri rastgele gecikmeler
  const delays = [
    Math.random() * 2000 + 1000,  // 1-3 saniye
    Math.random() * 1500 + 500,   // 0.5-2 saniye  
    Math.random() * 3000 + 2000,  // 2-5 saniye
  ];
  
  const selectedDelay = delays[Math.floor(Math.random() * delays.length)];
  return new Promise(resolve => setTimeout(resolve, selectedDelay));
}

// Zara stok kontrolü (Gelişmiş Bot Detection Bypass)
async function checkStockZara(url, sizesToCheck) {
  const sessionManager = new SessionManager();
  let attempt = 0;
  const maxAttempts = 3;

  while (attempt < maxAttempts) {
    attempt++;
    
    try {
      console.log(`🔍 Checking Zara (attempt ${attempt}): ${url}`);
      
      // Her denemede farklı headers kullan
      const headers = generateRealisticHeaders();
      
      // Önceki session'dan cookies varsa ekle
      if (sessionManager.getCookieString()) {
        headers['Cookie'] = sessionManager.getCookieString();
      }

      // Referrer ekle (direkt link değil, arama motorundan geliyormuş gibi)
      if (attempt === 1) {
        headers['Referer'] = 'https://www.google.com/';
      } else {
        headers['Referer'] = 'https://www.zara.com/tr/tr/';
      }

      // İlk önce ana sayfayı ziyaret et (bot gibi görünmemek için)
      if (attempt === 1) {
        console.log('🌐 Warming up session with homepage visit...');
        const warmupResponse = await fetch('https://www.zara.com/tr/tr/', {
          headers: headers
        });
        sessionManager.updateCookies(warmupResponse);
        await humanLikeDelay();
      }

      // Ana isteği gönder
      const response = await fetch(url, {
        headers: {
          ...headers,
          'Cookie': sessionManager.getCookieString(),
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache'
        }
      });

      sessionManager.updateCookies(response);

      if (!response.ok) {
        console.log(`❌ Zara fetch failed (attempt ${attempt}): ${response.status}`);
        
        if (response.status === 403 || response.status === 429) {
          console.log(`⚠️ Rate limited, waiting longer before retry...`);
          await new Promise(resolve => setTimeout(resolve, 10000 + Math.random() * 5000));
          continue;
        }
        
        if (attempt === maxAttempts) return null;
        await humanLikeDelay();
        continue;
      }

      const html = await response.text();
      
      // Bot detection kontrolleri
      const botDetectionKeywords = [
        'bm-verify', 'interstitial', 'challenge', 'blocked', 
        'access denied', 'forbidden', 'cloudflare',
        'rate limit', 'too many requests', 'suspicious activity'
      ];
      
      const hasDetection = botDetectionKeywords.some(keyword => 
        html.toLowerCase().includes(keyword.toLowerCase())
      );

      if (hasDetection) {
        console.log(`⚠️ Bot detection triggered (attempt ${attempt}). Trying alternative approaches...`);
        
        // Alternative API endpoint dene
        const productId = url.match(/p(\d+)/)?.[1];
        if (productId) {
          console.log('🔄 Trying alternative API endpoint...');
          
          const apiHeaders = {
            ...generateRealisticHeaders(),
            'Accept': 'application/json, text/plain, */*',
            'Referer': url,
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': sessionManager.getCookieString()
          };
          
          const apiUrls = [
            `https://www.zara.com/tr/tr/products/${productId}.json`,
            `https://www.zara.com/tr/tr/products/${productId}/availability`,
            `https://www.zara.com/tr/tr/share/product/${productId}.json`
          ];
          
          for (const apiUrl of apiUrls) {
            try {
              await humanLikeDelay();
              const apiResponse = await fetch(apiUrl, { headers: apiHeaders });
              
              if (apiResponse.ok) {
                const productData = await apiResponse.json();
                console.log('✅ Successfully accessed Zara API endpoint');
                
                // API response'unu parse et
                const result = parseZaraApiResponse(productData, sizesToCheck);
                if (result) return result;
              }
            } catch (apiError) {
              console.log(`⚠️ API endpoint failed: ${apiError.message}`);
            }
          }
        }
        
        if (attempt < maxAttempts) {
          console.log(`🔄 Retrying with different approach in ${5 + attempt * 2} seconds...`);
          await new Promise(resolve => setTimeout(resolve, (5 + attempt * 2) * 1000));
          continue;
        }
        
        return null;
      }
      
      // Normal HTML parsing
      console.log('📄 Parsing regular Zara page...');
      return parseZaraHtml(html, sizesToCheck);
      
    } catch (error) {
      console.log(`❌ Zara error (attempt ${attempt}): ${error.message}`);
      
      if (attempt < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, 3000 * attempt));
        continue;
      }
      
      return null;
    }
  }
  
  return null;
}

// Zara API response parser
function parseZaraApiResponse(productData, sizesToCheck) {
  try {
    if (productData.detail && productData.detail.colors) {
      for (const color of productData.detail.colors) {
        if (color.sizes) {
          for (const size of color.sizes) {
            const sizeValue = size.value || size.name;
            if (sizesToCheck.includes(sizeValue)) {
              const isAvailable = size.availability === 'in_stock' || 
                                size.available === true || 
                                size.stock > 0;
              
              if (isAvailable) {
                console.log(`✅ Zara API - ${sizeValue} size is in stock!`);
                return sizeValue;
              }
            }
          }
        }
      }
    }
    
    // Alternative API structure
    if (productData.product && productData.product.detail && productData.product.detail.colors) {
      return parseZaraApiResponse({ detail: productData.product.detail }, sizesToCheck);
    }
    
  } catch (error) {
    console.log(`⚠️ Error parsing Zara API response: ${error.message}`);
  }
  
  return null;
}

// Zara HTML parser
function parseZaraHtml(html, sizesToCheck) {
  // Method 1: window.__INITIAL_STATE__
  const jsonRegex = /window\.__INITIAL_STATE__\s*=\s*({.*?});/s;
  const match = html.match(jsonRegex);
  
  if (match) {
    try {
      const initialState = JSON.parse(match[1]);
      const product = initialState?.product || initialState?.products?.[0];
      
      if (product && product.detail && product.detail.colors) {
        for (const color of product.detail.colors) {
          if (color.sizes) {
            for (const size of color.sizes) {
              const sizeValue = size.value || size.name;
              if (sizesToCheck.includes(sizeValue) && size.availability === 'in_stock') {
                console.log(`✅ Zara JSON - ${sizeValue} size is in stock!`);
                return sizeValue;
              }
            }
          }
        }
      }
    } catch (jsonError) {
      console.log("⚠️ Zara JSON parse error:", jsonError.message);
    }
  }
  
  // Method 2: Script tag içindeki JSON yapıları
  const scriptRegex = /<script[^>]*>(.*?)<\/script>/gs;
  const scripts = html.match(scriptRegex) || [];
  
  for (const script of scripts) {
    try {
      const sizeDataRegex = /"sizes":\s*\[([^\]]+)\]/g;
      const sizeMatches = script.match(sizeDataRegex);
      
      if (sizeMatches) {
        for (const sizeMatch of sizeMatches) {
          try {
            const sizesData = JSON.parse(`{${sizeMatch}}`);
            if (sizesData.sizes) {
              for (const size of sizesData.sizes) {
                const sizeValue = size.value || size.name || size.size;
                if (sizesToCheck.includes(sizeValue) && (size.availability === 'in_stock' || size.stock > 0)) {
                  console.log(`✅ Zara Script - ${sizeValue} size is in stock!`);
                  return sizeValue;
                }
              }
            }
          } catch (e) {
            continue;
          }
        }
      }
    } catch (e) {
      continue;
    }
  }
  
  // Method 3: HTML attribute parsing
  const sizeSelectors = [
    /data-qa-qualifier="size-selector-sizes-size-label"[^>]*>([^<]+).*?data-qa-action="size-in-stock"/g,
    /class="[^"]*size[^"]*"[^>]*>([^<]+).*?(?:in-stock|available)/g,
    /data-size="([^"]+)"[^>]*class="[^"]*(?:available|in-stock)/g
  ];
  
  for (const selector of sizeSelectors) {
    let match;
    while ((match = selector.exec(html)) !== null) {
      const sizeValue = match[1].trim();
      if (sizesToCheck.includes(sizeValue)) {
        console.log(`✅ Zara HTML - ${sizeValue} size is in stock!`);
        return sizeValue;
      }
    }
  }
  
  console.log(`❌ Zara - No stock found for sizes: ${sizesToCheck.join(', ')}`);
  return null;
}

// Bershka stok kontrolü (Güncellenmiş headers ile)
async function checkStockBershka(url, sizesToCheck) {
  try {
    console.log(`🔍 Checking Bershka: ${url}`);
    
    const headers = generateRealisticHeaders();
    
    const response = await fetch(url, { headers });

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
        if (initialState.product && initialState.product.sizes) {
          for (const size of initialState.product.sizes) {
            if (sizesToCheck.includes(size.value) && size.stock > 0) {
              console.log(`✅ Bershka - ${size.value} size is in stock!`);
              return size.value;
            }
          }
        }
      } catch (jsonError) {
        console.log("⚠️ Bershka JSON parse error:", jsonError.message);
      }
    }
    
    console.log(`❌ Bershka - No stock found for sizes: ${sizesToCheck.join(', ')}`);
    return null;
    
  } catch (error) {
    console.log(`❌ Bershka error: ${error}`);
    return null;
  }
}

// Stradivarius stok kontrolü (Güncellenmiş headers ile)
async function checkStockStradivarius(url, sizesToCheck) {
  try {
    console.log(`🔍 Checking Stradivarius: ${url}`);
    
    const headers = generateRealisticHeaders();
    
    const response = await fetch(url, { headers });

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
        console.log("⚠️ Stradivarius JSON parse error:", jsonError.message);
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
      
      // İnsan benzeri bekleme süresi
      await humanLikeDelay();
      
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