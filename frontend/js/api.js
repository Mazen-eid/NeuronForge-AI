// Simple API client for the NeuronForge backend.
// Override by setting `window.NEURONFORGE_API` before loading this script, e.g.
// <script>window.NEURONFORGE_API = "http://localhost:8000";</script>
const API_BASE = (window.NEURONFORGE_API || "http://localhost:8000").replace(/\/$/, "");

async function apiGet(path) {
  const res = await fetch(API_BASE + path);
  if (!res.ok) throw new Error("HTTP " + res.status);
  return res.json();
}

async function apiPost(path, body) {
  const res = await fetch(API_BASE + path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  if (!res.ok) throw new Error("HTTP " + res.status + ": " + (await res.text()));
  return res.json();
}

function showApiUrl() {
  const el = document.getElementById("api-url");
  if (el) el.textContent = API_BASE;
}
window.addEventListener("DOMContentLoaded", showApiUrl);
