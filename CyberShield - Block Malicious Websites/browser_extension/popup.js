function storageGet(defaults) {
  return new Promise((resolve) => chrome.storage.local.get(defaults, resolve));
}

function storageSet(obj) {
  return new Promise((resolve) => chrome.storage.local.set(obj, resolve));
}

function dotClass(level) {
  if (level === "PHISHING") return "phishing";
  if (level === "SUSPICIOUS") return "suspicious";
  return "safe";
}

function fmt(ts) {
  try {
    const d = new Date(ts);
    return d.toLocaleString();
  } catch (e) {
    return String(ts || "");
  }
}

async function render() {
  const { cybershield_history } = await storageGet({ cybershield_history: [] });
  const history = Array.isArray(cybershield_history) ? cybershield_history : [];

  document.getElementById("count").textContent = String(history.length);
  const list = document.getElementById("list");
  const empty = document.getElementById("empty");
  list.innerHTML = "";

  if (history.length === 0) {
    empty.style.display = "block";
    return;
  }
  empty.style.display = "none";

  for (const h of history.slice(0, 10)) {
    const item = document.createElement("div");
    item.className = "item";

    const dot = document.createElement("div");
    dot.className = `dot ${dotClass(String(h.level || ""))}`;

    const box = document.createElement("div");
    const url = document.createElement("div");
    url.className = "url";
    url.textContent = String(h.url || "");
    const meta = document.createElement("div");
    meta.className = "meta";
    meta.textContent = `${String(h.level || "UNKNOWN")} • ${String(h.score_10 ?? "")}/10 • ${fmt(h.ts)}`;

    box.appendChild(url);
    box.appendChild(meta);

    item.appendChild(dot);
    item.appendChild(box);
    list.appendChild(item);
  }
}

document.getElementById("clear").addEventListener("click", async () => {
  await storageSet({ cybershield_history: [], cybershield_last: null });
  await render();
});

render();

