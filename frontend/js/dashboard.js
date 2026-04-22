async function refreshStatus() {
  const statusEl = document.getElementById("api-status");
  try {
    const data = await apiGet("/health");
    statusEl.textContent = t("backend_online") + " (v" + (data.version || "?") + ")";
    statusEl.className = "status-ok";
    return true;
  } catch (e) {
    statusEl.textContent = t("backend_offline");
    statusEl.className = "status-err";
    return false;
  }
}

async function refreshChannels() {
  const listEl = document.getElementById("channels-list");
  const selectEl = document.getElementById("channel-select");
  try {
    const data = await apiGet("/channels");
    const channels = data.channels || [];
    if (channels.length === 0) {
      listEl.innerHTML = "<em>No channels configured. See backend/channels/.</em>";
      selectEl.innerHTML = "";
      return;
    }
    listEl.innerHTML = channels
      .map(c => `<div><strong>${c.id}</strong> — ${c.niche} (${c.language}, ${c.platform})</div>`)
      .join("");
    selectEl.innerHTML = channels.map(c => `<option value="${c.id}">${c.id}</option>`).join("");
  } catch (e) {
    listEl.innerHTML = "<em>Backend offline.</em>";
  }
}

async function refreshRuns() {
  const tbody = document.querySelector("#runs-table tbody");
  try {
    const data = await apiGet("/runs?limit=20");
    tbody.innerHTML = (data.runs || []).map(r => `
      <tr>
        <td>${r.created_at}</td>
        <td>${r.channel_id}</td>
        <td>${(r.topic || "").slice(0, 60)}</td>
        <td>${r.status}</td>
        <td>${r.video_url ? `<a href="${r.video_url}" target="_blank">link</a>` : "—"}</td>
      </tr>
    `).join("");
  } catch (e) {
    tbody.innerHTML = "";
  }
}

function appendLog(line) {
  const out = document.getElementById("output-area");
  const stamp = new Date().toLocaleTimeString();
  out.textContent = `[${stamp}] ${line}\n` + out.textContent;
}

async function triggerRun(dryRun) {
  const channel = document.getElementById("channel-select").value;
  if (!channel) {
    appendLog("No channel selected.");
    return;
  }
  appendLog(`Triggering ${dryRun ? "dry run" : "full run"} for ${channel}…`);
  try {
    const data = await apiPost(`/channels/${channel}/run`, { dry_run: dryRun });
    appendLog("Queued: " + JSON.stringify(data));
    setTimeout(refreshRuns, 2000);
  } catch (e) {
    appendLog("Error: " + e.message);
  }
}

window.addEventListener("DOMContentLoaded", async () => {
  document.getElementById("btn-run-now").addEventListener("click", () => triggerRun(false));
  document.getElementById("btn-dry-run").addEventListener("click", () => triggerRun(true));
  const ok = await refreshStatus();
  if (ok) {
    await refreshChannels();
    await refreshRuns();
    setInterval(refreshRuns, 10000);
  }
});
