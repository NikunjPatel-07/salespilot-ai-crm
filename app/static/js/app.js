// SalesPilot AI CRM — main JS

// ── AI assistant panel helpers ─────────────────────────────────────────────

async function askAI(endpoint, leadId, outputEl) {
  outputEl.textContent = "⏳ Thinking...";
  try {
    const resp = await fetch(`/ai/${endpoint}/${leadId}`, {
      headers: { "Accept": "application/json" },
      credentials: "same-origin",
    });
    if (!resp.ok) {
      const err = await resp.json();
      outputEl.textContent = "Error: " + (err.detail || resp.statusText);
      return;
    }
    const data = await resp.json();
    outputEl.textContent = data.result;
  } catch (e) {
    outputEl.textContent = "Request failed. Please try again.";
  }
}

function initAIPanel(leadId) {
  const panel = document.getElementById("ai-panel");
  const output = document.getElementById("ai-result");
  if (!panel || !output) return;

  panel.querySelectorAll("[data-ai-action]").forEach(btn => {
    btn.addEventListener("click", () => {
      const action = btn.dataset.aiAction;
      askAI(action, leadId, output);
    });
  });
}

// ── Copy to clipboard ─────────────────────────────────────────────────────

function copyAIResult() {
  const el = document.getElementById("ai-result");
  if (!el) return;
  navigator.clipboard.writeText(el.textContent).then(() => {
    const btn = document.getElementById("copy-btn");
    if (btn) { btn.textContent = "Copied!"; setTimeout(() => btn.textContent = "Copy", 1500); }
  });
}

// ── Delete confirmation ───────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-confirm]").forEach(form => {
    form.addEventListener("submit", e => {
      if (!confirm(form.dataset.confirm || "Are you sure?")) e.preventDefault();
    });
  });

  // Auto-dismiss flash messages after 4 seconds
  document.querySelectorAll(".alert[data-auto-dismiss]").forEach(el => {
    setTimeout(() => el.style.opacity = "0", 3500);
    setTimeout(() => el.remove(), 4000);
  });
});
