var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// .wrangler/tmp/bundle-usyn5i/checked-fetch.js
var urls = /* @__PURE__ */ new Set();
function checkURL(request, init) {
  const url = request instanceof URL ? request : new URL(
    (typeof request === "string" ? new Request(request, init) : request).url
  );
  if (url.port && url.port !== "443" && url.protocol === "https:") {
    if (!urls.has(url.toString())) {
      urls.add(url.toString());
      console.warn(
        `WARNING: known issue with \`fetch()\` requests to custom HTTPS ports in published Workers:
 - ${url.toString()} - the custom port will be ignored when the Worker is published using the \`wrangler deploy\` command.
`
      );
    }
  }
}
__name(checkURL, "checkURL");
globalThis.fetch = new Proxy(globalThis.fetch, {
  apply(target, thisArg, argArray) {
    const [request, init] = argArray;
    checkURL(request, init);
    return Reflect.apply(target, thisArg, argArray);
  }
});

// src/index.js
var STOCK_CONFIG = {
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
async function sendTelegramMessage(message, env) {
  if (!env.BOT_API || !env.CHAT_ID) {
    console.log("\u26A0\uFE0F Telegram credentials not found");
    return false;
  }
  const url = `https://api.telegram.org/bot${env.BOT_API}/sendMessage`;
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        chat_id: env.CHAT_ID,
        text: message
      })
    });
    if (response.ok) {
      console.log("\u2705 Telegram message sent successfully");
      return true;
    } else {
      console.log("\u274C Failed to send Telegram message:", await response.text());
      return false;
    }
  } catch (error) {
    console.log("\u274C Telegram error:", error);
    return false;
  }
}
__name(sendTelegramMessage, "sendTelegramMessage");
var ADVANCED_USER_AGENTS = [
  // Chrome on Windows
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
  // Chrome on Mac
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  // Edge
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
  // Firefox
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
  // Safari
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
];
function generateRealisticHeaders() {
  const userAgent = ADVANCED_USER_AGENTS[Math.floor(Math.random() * ADVANCED_USER_AGENTS.length)];
  const isChrome = userAgent.includes("Chrome") && !userAgent.includes("Edg");
  const isFirefox = userAgent.includes("Firefox");
  const isSafari = userAgent.includes("Safari") && !userAgent.includes("Chrome");
  const isEdge = userAgent.includes("Edg");
  let headers = {
    "User-Agent": userAgent,
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
  };
  if (isChrome || isEdge) {
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7";
    headers["Sec-Ch-Ua"] = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"';
    headers["Sec-Ch-Ua-Mobile"] = "?0";
    headers["Sec-Ch-Ua-Platform"] = '"Windows"';
    headers["Sec-Fetch-Dest"] = "document";
    headers["Sec-Fetch-Mode"] = "navigate";
    headers["Sec-Fetch-Site"] = "none";
    headers["Sec-Fetch-User"] = "?1";
  } else if (isFirefox) {
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8";
  } else if (isSafari) {
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8";
  }
  return headers;
}
__name(generateRealisticHeaders, "generateRealisticHeaders");
var SessionManager = class {
  static {
    __name(this, "SessionManager");
  }
  constructor() {
    this.cookies = /* @__PURE__ */ new Map();
    this.sessionId = Math.random().toString(36).substring(2);
  }
  updateCookies(response) {
    const setCookieHeader = response.headers.get("set-cookie");
    if (setCookieHeader) {
      const cookies = setCookieHeader.split(",");
      cookies.forEach((cookie) => {
        const [nameValue] = cookie.split(";");
        const [name, value] = nameValue.split("=");
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
    return cookieArray.join("; ");
  }
};
function humanLikeDelay() {
  const delays = [
    Math.random() * 2e3 + 1e3,
    // 1-3 saniye
    Math.random() * 1500 + 500,
    // 0.5-2 saniye  
    Math.random() * 3e3 + 2e3
    // 2-5 saniye
  ];
  const selectedDelay = delays[Math.floor(Math.random() * delays.length)];
  return new Promise((resolve) => setTimeout(resolve, selectedDelay));
}
__name(humanLikeDelay, "humanLikeDelay");
async function checkStockZara(url, sizesToCheck) {
  const sessionManager = new SessionManager();
  let attempt = 0;
  const maxAttempts = 3;
  while (attempt < maxAttempts) {
    attempt++;
    try {
      console.log(`\u{1F50D} Checking Zara (attempt ${attempt}): ${url}`);
      const headers = generateRealisticHeaders();
      if (sessionManager.getCookieString()) {
        headers["Cookie"] = sessionManager.getCookieString();
      }
      if (attempt === 1) {
        headers["Referer"] = "https://www.google.com/";
      } else {
        headers["Referer"] = "https://www.zara.com/tr/tr/";
      }
      if (attempt === 1) {
        console.log("\u{1F310} Warming up session with homepage visit...");
        const warmupResponse = await fetch("https://www.zara.com/tr/tr/", {
          headers
        });
        sessionManager.updateCookies(warmupResponse);
        await humanLikeDelay();
      }
      const response = await fetch(url, {
        headers: {
          ...headers,
          "Cookie": sessionManager.getCookieString(),
          "Cache-Control": "no-cache",
          "Pragma": "no-cache"
        }
      });
      sessionManager.updateCookies(response);
      if (!response.ok) {
        console.log(`\u274C Zara fetch failed (attempt ${attempt}): ${response.status}`);
        if (response.status === 403 || response.status === 429) {
          console.log(`\u26A0\uFE0F Rate limited, waiting longer before retry...`);
          await new Promise((resolve) => setTimeout(resolve, 1e4 + Math.random() * 5e3));
          continue;
        }
        if (attempt === maxAttempts) return null;
        await humanLikeDelay();
        continue;
      }
      const html = await response.text();
      const botDetectionKeywords = [
        "bm-verify",
        "interstitial",
        "challenge",
        "blocked",
        "access denied",
        "forbidden",
        "cloudflare",
        "rate limit",
        "too many requests",
        "suspicious activity"
      ];
      const hasDetection = botDetectionKeywords.some(
        (keyword) => html.toLowerCase().includes(keyword.toLowerCase())
      );
      if (hasDetection) {
        console.log(`\u26A0\uFE0F Bot detection triggered (attempt ${attempt}). Trying alternative approaches...`);
        const productId = url.match(/p(\d+)/)?.[1];
        if (productId) {
          console.log("\u{1F504} Trying alternative API endpoint...");
          const apiHeaders = {
            ...generateRealisticHeaders(),
            "Accept": "application/json, text/plain, */*",
            "Referer": url,
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": sessionManager.getCookieString()
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
                console.log("\u2705 Successfully accessed Zara API endpoint");
                const result = parseZaraApiResponse(productData, sizesToCheck);
                if (result) return result;
              }
            } catch (apiError) {
              console.log(`\u26A0\uFE0F API endpoint failed: ${apiError.message}`);
            }
          }
        }
        if (attempt < maxAttempts) {
          console.log(`\u{1F504} Retrying with different approach in ${5 + attempt * 2} seconds...`);
          await new Promise((resolve) => setTimeout(resolve, (5 + attempt * 2) * 1e3));
          continue;
        }
        return null;
      }
      console.log("\u{1F4C4} Parsing regular Zara page...");
      return parseZaraHtml(html, sizesToCheck);
    } catch (error) {
      console.log(`\u274C Zara error (attempt ${attempt}): ${error.message}`);
      if (attempt < maxAttempts) {
        await new Promise((resolve) => setTimeout(resolve, 3e3 * attempt));
        continue;
      }
      return null;
    }
  }
  return null;
}
__name(checkStockZara, "checkStockZara");
function parseZaraApiResponse(productData, sizesToCheck) {
  try {
    if (productData.detail && productData.detail.colors) {
      for (const color of productData.detail.colors) {
        if (color.sizes) {
          for (const size of color.sizes) {
            const sizeValue = size.value || size.name;
            if (sizesToCheck.includes(sizeValue)) {
              const isAvailable = size.availability === "in_stock" || size.available === true || size.stock > 0;
              if (isAvailable) {
                console.log(`\u2705 Zara API - ${sizeValue} size is in stock!`);
                return sizeValue;
              }
            }
          }
        }
      }
    }
    if (productData.product && productData.product.detail && productData.product.detail.colors) {
      return parseZaraApiResponse({ detail: productData.product.detail }, sizesToCheck);
    }
  } catch (error) {
    console.log(`\u26A0\uFE0F Error parsing Zara API response: ${error.message}`);
  }
  return null;
}
__name(parseZaraApiResponse, "parseZaraApiResponse");
function parseZaraHtml(html, sizesToCheck) {
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
              if (sizesToCheck.includes(sizeValue) && size.availability === "in_stock") {
                console.log(`\u2705 Zara JSON - ${sizeValue} size is in stock!`);
                return sizeValue;
              }
            }
          }
        }
      }
    } catch (jsonError2) {
      console.log("\u26A0\uFE0F Zara JSON parse error:", jsonError2.message);
    }
  }
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
                if (sizesToCheck.includes(sizeValue) && (size.availability === "in_stock" || size.stock > 0)) {
                  console.log(`\u2705 Zara Script - ${sizeValue} size is in stock!`);
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
  const sizeSelectors = [
    /data-qa-qualifier="size-selector-sizes-size-label"[^>]*>([^<]+).*?data-qa-action="size-in-stock"/g,
    /class="[^"]*size[^"]*"[^>]*>([^<]+).*?(?:in-stock|available)/g,
    /data-size="([^"]+)"[^>]*class="[^"]*(?:available|in-stock)/g
  ];
  for (const selector of sizeSelectors) {
    let match2;
    while ((match2 = selector.exec(html)) !== null) {
      const sizeValue = match2[1].trim();
      if (sizesToCheck.includes(sizeValue)) {
        console.log(`\u2705 Zara HTML - ${sizeValue} size is in stock!`);
        return sizeValue;
      }
    }
  }
  console.log(`\u274C Zara - No stock found for sizes: ${sizesToCheck.join(", ")}`);
  return null;
}
__name(parseZaraHtml, "parseZaraHtml");
async function checkStockBershka(url, sizesToCheck) {
  try {
    console.log(`\u{1F50D} Checking Bershka: ${url}`);
    const headers = generateRealisticHeaders();
    const response = await fetch(url, { headers });
    if (!response.ok) {
      console.log(`\u274C Bershka fetch failed: ${response.status}`);
      return null;
    }
    const html = await response.text();
    const sizeRegex = /data-qa-anchor=['"']sizeListItem['"].*?class=['"']([^'"]*?)['"].*?<span[^>]*class=['"'][^'"]*text__label[^'"]*['"][^>]*>([^<]+)</g;
    let sizeMatch;
    while ((sizeMatch = sizeRegex.exec(html)) !== null) {
      const [, className, sizeText] = sizeMatch;
      const sizeValue = sizeText.trim();
      if (sizesToCheck.includes(sizeValue)) {
        if (!className.includes("is-disabled")) {
          console.log(`\u2705 Bershka - ${sizeValue} size is in stock!`);
          return sizeValue;
        }
      }
    }
    const jsonRegex = /window\.__INITIAL_STATE__\s*=\s*({.*?});/s;
    const jsonMatch = html.match(jsonRegex);
    if (jsonMatch) {
      try {
        const initialState = JSON.parse(jsonMatch[1]);
        if (initialState.product && initialState.product.sizes) {
          for (const size of initialState.product.sizes) {
            if (sizesToCheck.includes(size.value) && size.stock > 0) {
              console.log(`\u2705 Bershka - ${size.value} size is in stock!`);
              return size.value;
            }
          }
        }
      } catch (jsonError2) {
        console.log("\u26A0\uFE0F Bershka JSON parse error:", jsonError2.message);
      }
    }
    console.log(`\u274C Bershka - No stock found for sizes: ${sizesToCheck.join(", ")}`);
    return null;
  } catch (error) {
    console.log(`\u274C Bershka error: ${error}`);
    return null;
  }
}
__name(checkStockBershka, "checkStockBershka");
async function checkStockStradivarius(url, sizesToCheck) {
  try {
    console.log(`\u{1F50D} Checking Stradivarius: ${url}`);
    const headers = generateRealisticHeaders();
    const response = await fetch(url, { headers });
    if (!response.ok) {
      console.log(`\u274C Stradivarius fetch failed: ${response.status}`);
      return null;
    }
    const html = await response.text();
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
              console.log(`\u2705 Stradivarius - ${sizeValue} size is in stock!`);
              return sizeValue;
            }
          }
        }
      } catch (jsonError2) {
        console.log("\u26A0\uFE0F Stradivarius JSON parse error:", jsonError2.message);
      }
    }
    const sizePatterns = [
      /data-qa-qualifier=['"']size-selector-sizes-size-label['"][^>]*>([^<]+).*?data-qa-action=['"']size-in-stock['"]|data-qa-action=['"']size-low-on-stock['"]/g,
      /class=['"'][^'"]*size[^'"]*['"][^>]*>([^<]+).*?(?!disabled|unavailable|out-of-stock)/gi
    ];
    for (const pattern of sizePatterns) {
      let match;
      while ((match = pattern.exec(html)) !== null) {
        const sizeValue = match[1].trim();
        if (sizesToCheck.includes(sizeValue)) {
          console.log(`\u2705 Stradivarius - ${sizeValue} size is in stock!`);
          return sizeValue;
        }
      }
    }
    console.log(`\u274C Stradivarius - No stock found for sizes: ${sizesToCheck.join(", ")}`);
    return null;
  } catch (error) {
    console.log(`\u274C Stradivarius error: ${error}`);
    return null;
  }
}
__name(checkStockStradivarius, "checkStockStradivarius");
async function checkStock(item, sizesToCheck) {
  const { store, url } = item;
  switch (store.toLowerCase()) {
    case "zara":
      return await checkStockZara(url, sizesToCheck);
    case "bershka":
      return await checkStockBershka(url, sizesToCheck);
    case "stradivarius":
      return await checkStockStradivarius(url, sizesToCheck);
    default:
      console.log(`\u274C Unsupported store: ${store}`);
      return null;
  }
}
__name(checkStock, "checkStock");
async function runStockCheck(env) {
  console.log("\u{1F680} Starting stock check...");
  for (const item of STOCK_CONFIG.urls) {
    try {
      console.log(`
\u{1F4CB} Checking: ${item.store} - ${item.url}`);
      const sizeInStock = await checkStock(item, STOCK_CONFIG.sizes_to_check);
      if (sizeInStock) {
        const message = `\u{1F6CD}\uFE0F ${sizeInStock} beden stokta!!!!
Ma\u011Faza: ${item.store.toUpperCase()}
Link: ${item.url}`;
        console.log(`\u{1F389} STOCK FOUND: ${message}`);
        await sendTelegramMessage(message, env);
      } else {
        console.log(`\u274C No stock found for ${item.store}`);
      }
      await humanLikeDelay();
    } catch (error) {
      console.log(`\u274C Error checking ${item.store}: ${error}`);
    }
  }
  console.log("\u2705 Stock check completed");
}
__name(runStockCheck, "runStockCheck");
var src_default = {
  // Cron trigger handler
  async scheduled(controller, env, ctx) {
    console.log("\u23F0 Cron triggered - running stock check");
    ctx.waitUntil(runStockCheck(env));
  },
  // HTTP request handler (test için)
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/test") {
      ctx.waitUntil(runStockCheck(env));
      return new Response("Stock check started! Check logs for results.", {
        headers: { "Content-Type": "text/plain" }
      });
    }
    if (url.pathname === "/status") {
      return new Response(JSON.stringify({
        status: "active",
        config: {
          stores: STOCK_CONFIG.urls.map((item) => ({ store: item.store, url: item.url })),
          sizes: STOCK_CONFIG.sizes_to_check,
          cron: "*/10 * * * *"
        }
      }), {
        headers: { "Content-Type": "application/json" }
      });
    }
    return new Response("Stock Checker Worker\n\nEndpoints:\n- /test - Run manual stock check\n- /status - Check configuration", {
      headers: { "Content-Type": "text/plain" }
    });
  }
};

// ../../../../../opt/homebrew/lib/node_modules/wrangler/templates/middleware/middleware-ensure-req-body-drained.ts
var drainBody = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } finally {
    try {
      if (request.body !== null && !request.bodyUsed) {
        const reader = request.body.getReader();
        while (!(await reader.read()).done) {
        }
      }
    } catch (e) {
      console.error("Failed to drain the unused request body.", e);
    }
  }
}, "drainBody");
var middleware_ensure_req_body_drained_default = drainBody;

// ../../../../../opt/homebrew/lib/node_modules/wrangler/templates/middleware/middleware-miniflare3-json-error.ts
function reduceError(e) {
  return {
    name: e?.name,
    message: e?.message ?? String(e),
    stack: e?.stack,
    cause: e?.cause === void 0 ? void 0 : reduceError(e.cause)
  };
}
__name(reduceError, "reduceError");
var jsonError = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } catch (e) {
    const error = reduceError(e);
    return Response.json(error, {
      status: 500,
      headers: { "MF-Experimental-Error-Stack": "true" }
    });
  }
}, "jsonError");
var middleware_miniflare3_json_error_default = jsonError;

// .wrangler/tmp/bundle-usyn5i/middleware-insertion-facade.js
var __INTERNAL_WRANGLER_MIDDLEWARE__ = [
  middleware_ensure_req_body_drained_default,
  middleware_miniflare3_json_error_default
];
var middleware_insertion_facade_default = src_default;

// ../../../../../opt/homebrew/lib/node_modules/wrangler/templates/middleware/common.ts
var __facade_middleware__ = [];
function __facade_register__(...args) {
  __facade_middleware__.push(...args.flat());
}
__name(__facade_register__, "__facade_register__");
function __facade_invokeChain__(request, env, ctx, dispatch, middlewareChain) {
  const [head, ...tail] = middlewareChain;
  const middlewareCtx = {
    dispatch,
    next(newRequest, newEnv) {
      return __facade_invokeChain__(newRequest, newEnv, ctx, dispatch, tail);
    }
  };
  return head(request, env, ctx, middlewareCtx);
}
__name(__facade_invokeChain__, "__facade_invokeChain__");
function __facade_invoke__(request, env, ctx, dispatch, finalMiddleware) {
  return __facade_invokeChain__(request, env, ctx, dispatch, [
    ...__facade_middleware__,
    finalMiddleware
  ]);
}
__name(__facade_invoke__, "__facade_invoke__");

// .wrangler/tmp/bundle-usyn5i/middleware-loader.entry.ts
var __Facade_ScheduledController__ = class ___Facade_ScheduledController__ {
  constructor(scheduledTime, cron, noRetry) {
    this.scheduledTime = scheduledTime;
    this.cron = cron;
    this.#noRetry = noRetry;
  }
  static {
    __name(this, "__Facade_ScheduledController__");
  }
  #noRetry;
  noRetry() {
    if (!(this instanceof ___Facade_ScheduledController__)) {
      throw new TypeError("Illegal invocation");
    }
    this.#noRetry();
  }
};
function wrapExportedHandler(worker) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return worker;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  const fetchDispatcher = /* @__PURE__ */ __name(function(request, env, ctx) {
    if (worker.fetch === void 0) {
      throw new Error("Handler does not export a fetch() function.");
    }
    return worker.fetch(request, env, ctx);
  }, "fetchDispatcher");
  return {
    ...worker,
    fetch(request, env, ctx) {
      const dispatcher = /* @__PURE__ */ __name(function(type, init) {
        if (type === "scheduled" && worker.scheduled !== void 0) {
          const controller = new __Facade_ScheduledController__(
            Date.now(),
            init.cron ?? "",
            () => {
            }
          );
          return worker.scheduled(controller, env, ctx);
        }
      }, "dispatcher");
      return __facade_invoke__(request, env, ctx, dispatcher, fetchDispatcher);
    }
  };
}
__name(wrapExportedHandler, "wrapExportedHandler");
function wrapWorkerEntrypoint(klass) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return klass;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  return class extends klass {
    #fetchDispatcher = /* @__PURE__ */ __name((request, env, ctx) => {
      this.env = env;
      this.ctx = ctx;
      if (super.fetch === void 0) {
        throw new Error("Entrypoint class does not define a fetch() function.");
      }
      return super.fetch(request);
    }, "#fetchDispatcher");
    #dispatcher = /* @__PURE__ */ __name((type, init) => {
      if (type === "scheduled" && super.scheduled !== void 0) {
        const controller = new __Facade_ScheduledController__(
          Date.now(),
          init.cron ?? "",
          () => {
          }
        );
        return super.scheduled(controller);
      }
    }, "#dispatcher");
    fetch(request) {
      return __facade_invoke__(
        request,
        this.env,
        this.ctx,
        this.#dispatcher,
        this.#fetchDispatcher
      );
    }
  };
}
__name(wrapWorkerEntrypoint, "wrapWorkerEntrypoint");
var WRAPPED_ENTRY;
if (typeof middleware_insertion_facade_default === "object") {
  WRAPPED_ENTRY = wrapExportedHandler(middleware_insertion_facade_default);
} else if (typeof middleware_insertion_facade_default === "function") {
  WRAPPED_ENTRY = wrapWorkerEntrypoint(middleware_insertion_facade_default);
}
var middleware_loader_entry_default = WRAPPED_ENTRY;
export {
  __INTERNAL_WRANGLER_MIDDLEWARE__,
  middleware_loader_entry_default as default
};
//# sourceMappingURL=index.js.map
