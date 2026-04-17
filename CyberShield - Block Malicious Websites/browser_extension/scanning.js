const SERVICE_BASE = "http://127.0.0.1:8765";
// Persist scan results across browser restarts.
// Cache SAFE domains for a long time, and cache risky domains for a shorter window.
const SAFE_CACHE_TTL_MS = 30 * 24 * 60 * 60 * 1000; // 30 days
const RISK_CACHE_TTL_MS = 6 * 60 * 60 * 1000; // 6 hours
const CACHE_MAX_ENTRIES = 200;

function qp(name) {
  const u = new URL(window.location.href);
  return u.searchParams.get(name) || "";
}

function storageLocalGet(defaults) {
  return new Promise((resolve) => chrome.storage.local.get(defaults, resolve));
}

function storageLocalSet(obj) {
  return new Promise((resolve) => chrome.storage.local.set(obj, resolve));
}

function storageSessionGet(defaults) {
  // storage.session is best (clears on browser restart); fallback to local.
  const area = (chrome.storage && chrome.storage.session) ? chrome.storage.session : chrome.storage.local;
  return new Promise((resolve) => area.get(defaults, resolve));
}

function storageSessionSet(obj) {
  const area = (chrome.storage && chrome.storage.session) ? chrome.storage.session : chrome.storage.local;
  return new Promise((resolve) => area.set(obj, resolve));
}

async function cacheKeyForUrl(url) {
  // Cache by hostname (so different pages on youtube.com reuse the same scan).
  // Fallback to the full URL if parsing fails.
  let basis = String(url || "");
  try {
    basis = (new URL(basis)).hostname.replace(/^www\./i, "").toLowerCase() || basis;
  } catch (e) {}

  const data = new TextEncoder().encode(basis);
  const digest = await crypto.subtle.digest("SHA-256", data);
  const bytes = Array.from(new Uint8Array(digest));
  const hex = bytes.map((b) => b.toString(16).padStart(2, "0")).join("");
  return `cybershield_cache:${hex}`;
}

async function readCachedResult(url) {
  const key = await cacheKeyForUrl(url);
  const res = await storageLocalGet({ [key]: null });
  const entry = res ? res[key] : null;
  if (!entry || !entry.ts || !entry.result) return null;
  const ttl = Number(entry.ttl_ms || 0);
  if (!ttl || Date.now() - Number(entry.ts) > ttl) return null;
  return entry.result;
}

async function writeCachedResult(url, result) {
  const key = await cacheKeyForUrl(url);
  const decision = String(result && result.decision ? result.decision : "");
  const ttl_ms = decision === "AUTO_OPEN" ? SAFE_CACHE_TTL_MS : RISK_CACHE_TTL_MS;
  const ts = Date.now();
  const expires_at = ts + ttl_ms;

  await storageLocalSet({ [key]: { ts, ttl_ms, expires_at, result } });

  // Best-effort cleanup / size cap.
  try {
    const idxKey = "cybershield_cache_index";
    const { cybershield_cache_index } = await storageLocalGet({ [idxKey]: [] });
    const index = Array.isArray(cybershield_cache_index) ? cybershield_cache_index : [];
    const next = [{ key, expires_at }, ...index.filter((i) => i && i.key && i.key !== key)];
    const fresh = next.filter((i) => Number(i.expires_at || 0) > Date.now());
    await storageLocalSet({ [idxKey]: fresh.slice(0, CACHE_MAX_ENTRIES) });
  } catch (e) {}
}

async function score(url) {
  const resp = await fetch(`${SERVICE_BASE}/score?url=${encodeURIComponent(url)}`);
  return await resp.json();
}

(async () => {
  let tabId = parseInt(qp("tab"), 10);
  const url = qp("u");
  document.getElementById("url").textContent = url;
  const noteEl = document.getElementById("note");

  if (Number.isNaN(tabId)) {
    try {
      const current = await chrome.tabs.getCurrent();
      tabId = current && current.id ? current.id : tabId;
    } catch (e) {}
  }

  const warningUrl =
    chrome.runtime.getURL("warning.html") +
    `?tab=${encodeURIComponent(tabId)}` +
    `&u=${encodeURIComponent(url)}`;

  try {
    // Cache: if we've already scanned this URL recently, reuse the result.
    let result = await readCachedResult(url);
    if (!result) {
      result = await score(url);
      if (result && result.ok) {
        await writeCachedResult(url, result);
      }
    } else if (noteEl) {
      noteEl.textContent = "Using cached scan result (no rescan).";
    }
    if (result && result.ok) {
      // Only show the guard page when the scan says it's risky (score > 0/10).
      if (String(result.decision || "") === "AUTO_OPEN") {
        try {
          await chrome.runtime.sendMessage({ type: "CYBERSHIELD_UNBLOCK_URL", url });
        } catch (e) {}
        try {
          await chrome.runtime.sendMessage({ type: "CYBERSHIELD_ALLOW_ONCE", url });
        } catch (e) {}
        chrome.tabs.update(tabId, { url });
        return;
      }

      // Enforce: block the risky host at the network layer for main-frame loads.
      // This prevents the website from opening until the user explicitly allows it.
      try {
        const resp = await chrome.runtime.sendMessage({ type: "CYBERSHIELD_BLOCK_URL", url });
        if (noteEl && resp && resp.ok === false) {
          noteEl.textContent = `Blocking failed: ${String(resp.error || resp)}`;
        }
      } catch (e) {}

      // Cache the scan result so warning.html can render instantly without re-scanning.
      const cacheKey = `scan:${tabId}`;
      await storageSessionSet({
        [cacheKey]: {
          ts: Date.now(),
          url,
          result,
        },
      });
      chrome.tabs.update(tabId, { url: warningUrl });
      return;
    }
  } catch (e) {
    // fall through to warning
  }

  // If scan fails, still show the guard so the user can choose (safer default).
  if (noteEl) noteEl.textContent = "Scan failed or service not reachable. Showing CyberShield Guard.";
  chrome.tabs.update(tabId, { url: warningUrl });
})();
