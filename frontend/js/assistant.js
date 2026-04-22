async function sendRequest() {
  const input = document.getElementById("user-input").value.trim();
  const responseArea = document.getElementById("response-area");
  if (!input) {
    responseArea.textContent = t("assistant_response_wait");
    return;
  }
  responseArea.textContent = "…";
  try {
    const data = await apiPost("/assistant/ideas", { prompt: input, language: currentLang });
    responseArea.textContent = (data.ideas || []).map((x, i) => `${i + 1}. ${x}`).join("\n") || JSON.stringify(data);
  } catch (e) {
    responseArea.textContent = "Error: " + e.message + "\n\n(Backend offline? Start it with `cd backend && python -m neuronforge api`.)";
  }
}

window.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btn-assistant-send");
  if (btn) btn.addEventListener("click", sendRequest);
});
