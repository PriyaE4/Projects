const SERVICE_BASE = "http://127.0.0.1:8765";

function qp(name) {
  const u = new URL(window.location.href);
  return u.searchParams.get(name) || "";
}

function storageGet(defaults) {
  return new Promise((resolve) => chrome.storage.local.get(defaults, resolve));
}

function storageSet(obj) {
  return new Promise((resolve) => chrome.storage.local.set(obj, resolve));
}

function storageSessionGet(defaults) {
  const area = (chrome.storage && chrome.storage.session) ? chrome.storage.session : chrome.storage.local;
  return new Promise((resolve) => area.get(defaults, resolve));
}

async function launchBlock(url) {
  await fetch(`${SERVICE_BASE}/launch_block?url=${encodeURIComponent(url)}`);
}

async function score(url) {
  const resp = await fetch(`${SERVICE_BASE}/score?url=${encodeURIComponent(url)}`);
  return await resp.json();
}

function score10FromResult(result) {
  if (result && typeof result.score_10 === "number") return result.score_10;
  const s100 = Number(result && result.score ? result.score : 0);
  if (!Number.isFinite(s100) || s100 <= 0) return 0;
  const v = Math.max(0, Math.min(10, Math.round(s100 / 10)));
  return Math.max(1, v);
}

function levelFromScore10(score10) {
  if (score10 >= 7) return "PHISHING";
  if (score10 >= 3) return "SUSPICIOUS";
  return "SAFE";
}

function setBadge(level) {
  const badge = document.getElementById("levelBadge");
  if (!badge) return;
  badge.textContent = level;
  badge.classList.remove("safe", "suspicious", "phishing");
  if (level === "SAFE") badge.classList.add("safe");
  else if (level === "SUSPICIOUS") badge.classList.add("suspicious");
  else if (level === "PHISHING") badge.classList.add("phishing");
}

function fillList(id, items) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = "";
  const arr = Array.isArray(items) ? items : (items ? [String(items)] : []);
  if (arr.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No details available.";
    el.appendChild(li);
    return;
  }
  for (const it of arr) {
    const li = document.createElement("li");
    li.textContent = String(it);
    el.appendChild(li);
  }
}

function formatHits(hits) {
  if (!hits) return [];
  if (Array.isArray(hits)) return hits;
  if (typeof hits === "object") {
    return Object.entries(hits).map(([k, v]) => `${k}: ${v}`);
  }
  return [String(hits)];
}

async function addToHistory(entry) {
  try {
    const { cybershield_history } = await storageGet({ cybershield_history: [] });
    const history = Array.isArray(cybershield_history) ? cybershield_history : [];
    const next = [entry, ...history].slice(0, 50);
    await storageSet({ cybershield_history: next, cybershield_last: entry });
  } catch (e) {
    // Non-fatal.
  }
}

(async () => {
  let tabId = parseInt(qp("tab"), 10);
  const url = qp("u");
  let scoreValue = null;
  let riskValue = "UNKNOWN";
  let decisionValue = "WARN";

  document.getElementById("url").textContent = url;

  if (Number.isNaN(tabId)) {
    try {
      const current = await chrome.tabs.getCurrent();
      tabId = current && current.id ? current.id : tabId;
    } catch (e) {
      // keep NaN; update will no-op
    }
  }

  const openBtn = document.getElementById("openSite");
  const dontOpenBtn = document.getElementById("dontOpen");
  openBtn.disabled = true;
  dontOpenBtn.disabled = true;

  const openModal = document.getElementById("openConfirmModal");
  const openText = document.getElementById("openConfirmText");
  const openYes = document.getElementById("openConfirmYes");
  const openNo = document.getElementById("openConfirmNo");

  const blockModal = document.getElementById("blockModal");
  const blockText = document.getElementById("blockText");
  const blockYes = document.getElementById("blockYes");
  const blockNo = document.getElementById("blockNo");

  function showOpenConfirm() {
    openText.textContent = `This site is marked as ${riskValue} (risk ${scoreValue}/10).\n\nOpen anyway?\n\n${url}`;
    openModal.classList.add("open");
  }

  function hideOpenConfirm() {
    openModal.classList.remove("open");
  }

  function showBlockPrompt() {
    blockText.textContent = `Do you want to block this website using CyberShield?\n\n${url}`;
    blockModal.classList.add("open");
  }

  function hideBlockPrompt() {
    blockModal.classList.remove("open");
  }

  // Step 1: user chooses to open -> Step 2: confirm "Are you sure?"
  openBtn.addEventListener("click", () => {
    showOpenConfirm();
  });

  openNo.addEventListener("click", () => {
    hideOpenConfirm();
  });

  openYes.addEventListener("click", async () => {
    try {
      const un = await chrome.runtime.sendMessage({ type: "CYBERSHIELD_UNBLOCK_URL", url });
      if (un && un.ok === false) {
        document.getElementById("note").textContent = `Unblock failed: ${String(un.error || un)}`;
      }
      await chrome.runtime.sendMessage({ type: "CYBERSHIELD_ALLOW_ONCE", url });
    } catch (e) {
      // If message fails, navigation may re-trigger warning.
    }
    hideOpenConfirm();
    chrome.tabs.update(tabId, { url });
  });

  // Step 1: user chooses not to open -> Step 2: ask if they want to block in CyberShield.
  dontOpenBtn.addEventListener("click", () => {
    showBlockPrompt();
  });

  blockNo.addEventListener("click", () => {
    // For non-BLOCK decisions, do not keep the site permanently blocked if the user just cancels.
    (async () => {
      try {
        if (decisionValue !== "BLOCK" && riskValue !== "PHISHING") {
          await chrome.runtime.sendMessage({ type: "CYBERSHIELD_UNBLOCK_URL", url });
          document.getElementById("note").textContent = "Not opened. You can try again later.";
        }
      } catch (e) {}
      hideBlockPrompt();
    })();
  });

  blockYes.addEventListener("click", async () => {
    try {
      await chrome.runtime.sendMessage({ type: "CYBERSHIELD_BLOCK_URL", url });
      await launchBlock(url);
      document.getElementById("note").textContent = "CyberShield launched. You can block the site there.";
    } catch (e) {
      document.getElementById("note").textContent = "Could not contact CyberShield service. Is it running?";
    }
    hideBlockPrompt();
    chrome.tabs.update(tabId, { url: "about:blank" });
  });

  // Fetch score and decide.
  try {
    const cacheKey = `scan:${tabId}`;
    const cached = await storageSessionGet({ [cacheKey]: null });
    let result = cached ? cached[cacheKey] : null;
    if (result && result.url === url && result.result) {
      result = result.result;
    } else {
      result = await score(url);
    }
    if (result && result.ok) {
      scoreValue = score10FromResult(result);
      riskValue = String(result.level || levelFromScore10(scoreValue));
      decisionValue = String(result.decision || (riskValue === "PHISHING" ? "BLOCK" : (riskValue === "SAFE" ? "AUTO_OPEN" : "WARN")));

      document.getElementById("domain").textContent = String(result.domain || "—");
      document.getElementById("score").textContent = `${scoreValue}/10`;
      document.getElementById("risk").textContent = riskValue;
      setBadge(riskValue);
      dontOpenBtn.disabled = false;

      fillList("sources", result.sources || []);
      fillList("reasons", result.phishing_reasons || []);
      fillList("hits", formatHits(result.phishing_hits));

      if (riskValue === "PHISHING") {
        document.getElementById("note").textContent = "Recommended: Don’t open this website unless you’re absolutely sure.";
        document.getElementById("details").open = true;
      } else if (riskValue === "SUSPICIOUS") {
        document.getElementById("note").textContent = "Proceed with caution. Avoid entering credentials or payment details.";
      }

      // Hard-block mode: do not ask for consent, and do not allow opening.
      if (decisionValue === "BLOCK" || riskValue === "PHISHING") {
        openBtn.style.display = "none";
        openModal.classList.remove("open");
        openText.textContent = "";
        document.getElementById("note").textContent = "Blocked by CyberShield (high risk). This website will not be opened.";
        document.getElementById("details").open = true;
      } else {
        openBtn.disabled = false;
      }

      // Persist risky URLs locally (for demo + audit trail).
      if (riskValue !== "SAFE") {
        await addToHistory({
          ts: new Date().toISOString(),
          url: result.url || url,
          domain: result.domain || "",
          level: riskValue,
          score_10: scoreValue,
          score_100: Number(result.score || 0),
          sources: Array.isArray(result.sources) ? result.sources : [],
        });
      }

      // Auto-open only when the service explicitly says so (score == 0/10).
      if (decisionValue === "AUTO_OPEN") {
        try {
          await chrome.runtime.sendMessage({ type: "CYBERSHIELD_ALLOW_ONCE", url });
        } catch (e) {}
        chrome.tabs.update(tabId, { url });
      }
    } else {
      document.getElementById("score").textContent = "N/A";
      document.getElementById("risk").textContent = "UNKNOWN";
      document.getElementById("domain").textContent = "N/A";
      setBadge("UNKNOWN");
      document.getElementById("note").textContent = "Could not score this URL. Service response invalid.";
      openBtn.disabled = false;
      dontOpenBtn.disabled = false;
    }
  } catch (e) {
    document.getElementById("score").textContent = "N/A";
    document.getElementById("risk").textContent = "UNKNOWN";
    document.getElementById("domain").textContent = "N/A";
    setBadge("UNKNOWN");
    document.getElementById("note").textContent = "Could not contact CyberShield service. Start `python cybershield_service.py`.";
    openBtn.disabled = false;
    dontOpenBtn.disabled = false;
  }
})();
