const SERVICE_BASE = "http://127.0.0.1:8765";

// Keep-alive / activity ping so the desktop app can show extension status.
async function heartbeat() {
  try {
    await fetch(`${SERVICE_BASE}/heartbeat`, { method: "GET" });
  } catch (_) {
    // Ignore when service isn't running.
  }
}

heartbeat();
setInterval(heartbeat, 10_000);
const suppress = new Set(); // tabId to ignore next update
const allowOnce = new Map(); // tabId -> { url, expiresAt }

const SEARCH_ENGINE_HOSTS = new Set([
  "www.google.com",
  "google.com",
  "www.bing.com",
  "bing.com",
  "search.yahoo.com",
  "www.yahoo.com",
  "duckduckgo.com",
  "www.duckduckgo.com"
]);

function hostnameFromUrl(url) {
  try {
    const h = new URL(url).hostname || "";
    return h.toLowerCase();
  } catch (e) {
    return "";
  }
}

function baseDomainFromHost(host) {
  const parts = String(host || "")
    .toLowerCase()
    .split(".")
    .filter(Boolean);
  if (parts.length < 2) return "";
  return `${parts[parts.length - 2]}.${parts[parts.length - 1]}`;
}

function escapeRegex(s) {
  return String(s || "").replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function ruleIdForHost(host) {
  // Stable small hash in [10000..99999] to avoid collisions with other rule ids.
  let hash = 0;
  for (let i = 0; i < host.length; i++) {
    hash = (hash * 31 + host.charCodeAt(i)) >>> 0;
  }
  return 10000 + (hash % 90000);
}

async function blockHost(host) {
  host = (host || "").trim().toLowerCase();
  if (!host) return { ok: false, error: "invalid_host" };
  const hostId = ruleIdForHost(`host:${host}`);
  const base = baseDomainFromHost(host);
  const baseId = base ? ruleIdForHost(`base:${base}`) : null;
  const removeRuleIds = baseId ? [hostId, baseId] : [hostId];
  const addRules = [
    {
      id: hostId,
      priority: 1,
      action: { type: "block" },
      condition: { requestDomains: [host], resourceTypes: ["main_frame"] },
    },
  ];
  if (base && base !== host) {
    // Block any subdomain of the base domain too (covers redirects like www./m./login.).
    const re = `^https?://([a-z0-9-]+\\.)*${escapeRegex(base)}(/|$)`;
    addRules.push({
      id: baseId,
      priority: 1,
      action: { type: "block" },
      condition: { regexFilter: re, resourceTypes: ["main_frame"] },
    });
  }
  try {
    await chrome.declarativeNetRequest.updateSessionRules({
      removeRuleIds,
      addRules,
    });
    return { ok: true, host, base, ids: removeRuleIds };
  } catch (e) {
    return { ok: false, error: String(e) };
  }
}

async function unblockHost(host) {
  host = (host || "").trim().toLowerCase();
  if (!host) return { ok: false, error: "invalid_host" };
  const hostId = ruleIdForHost(`host:${host}`);
  const base = baseDomainFromHost(host);
  const baseId = base ? ruleIdForHost(`base:${base}`) : null;
  const removeRuleIds = baseId ? [hostId, baseId] : [hostId];
  try {
    await chrome.declarativeNetRequest.updateSessionRules({
      removeRuleIds,
      addRules: [],
    });
    return { ok: true, host, base, ids: removeRuleIds };
  } catch (e) {
    return { ok: false, error: String(e) };
  }
}

function isHttpUrl(url) {
  return typeof url === "string" && (url.startsWith("http://") || url.startsWith("https://"));
}

function isExtensionUrl(url) {
  return typeof url === "string" && url.startsWith("chrome-extension://");
}

function hostnameOf(url) {
  try {
    return new URL(url).hostname || "";
  } catch (e) {
    return "";
  }
}

function isSearchResultsPage(url) {
  try {
    const u = new URL(url);
    if (!SEARCH_ENGINE_HOSTS.has((u.hostname || "").toLowerCase())) return false;
    // Avoid gating search results pages themselves (noise),
    // but DO NOT exempt redirector URLs like `https://www.google.com/url?...`.
    const path = u.pathname || "/";
    if (path === "/search") return true;
    if (path === "/") {
      // Google/Bing home with query.
      return u.searchParams.has("q") || u.searchParams.has("p");
    }
    return false;
  } catch (e) {
    return false;
  }
}

function isAllowOnce(tabId, url) {
  const rec = allowOnce.get(tabId);
  if (!rec) return false;
  if (Date.now() > rec.expiresAt) {
    allowOnce.delete(tabId);
    return false;
  }
  if (rec.url === url) {
    // True one-time bypass.
    allowOnce.delete(tabId);
    return true;
  }
  return false;
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg && msg.type === "CYBERSHIELD_ALLOW_ONCE" && sender && sender.tab) {
    allowOnce.set(sender.tab.id, { url: msg.url, expiresAt: Date.now() + 30_000 });
    sendResponse({ ok: true });
    return true;
  }
  if (msg && msg.type === "CYBERSHIELD_BLOCK_URL") {
    const host = hostnameFromUrl(msg.url || "");
    Promise.resolve(blockHost(host)).then(sendResponse);
    return true;
  }
  if (msg && msg.type === "CYBERSHIELD_UNBLOCK_URL") {
    const host = hostnameFromUrl(msg.url || "");
    Promise.resolve(unblockHost(host)).then(sendResponse);
    return true;
  }
  return false;
});

chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  if (details.frameId !== 0) return;
  const tabId = details.tabId;
  const url = details.url;

  if (suppress.has(tabId)) {
    suppress.delete(tabId);
    return;
  }

  if (isExtensionUrl(url)) return;
  if (!isHttpUrl(url)) return;
  if (isSearchResultsPage(url)) return;
  if (isAllowOnce(tabId, url)) return;
  if (url.startsWith(chrome.runtime.getURL("warning.html"))) return;
  if (url.startsWith(chrome.runtime.getURL("scanning.html"))) return;

  // Gate the navigation through a scanning page first.
  // If the scan score is 0, scanning.html opens the site directly without showing the guard.
  // If the scan score is > 0, scanning.html routes to warning.html.
  //
  // Important: `onBeforeNavigate` is not cancelable in MV3, so we also add a temporary
  // DNR session block for the destination host immediately. Safe results will unblock
  // and proceed; risky results stay blocked until the user allows.
  suppress.add(tabId);
  try {
    await blockHost(hostnameFromUrl(url));
  } catch (e) {
    // Non-fatal; continue with scan gate (site might briefly start loading).
  }
  const gateUrl =
    chrome.runtime.getURL("scanning.html") +
    `?tab=${encodeURIComponent(tabId)}` +
    `&u=${encodeURIComponent(url)}`;
  chrome.tabs.update(tabId, { url: gateUrl });
});
