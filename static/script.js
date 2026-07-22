document.getElementById("checkBtn").addEventListener("click", async () => {
  const message = document.getElementById("messageInput").value.trim();
  if (!message) return;

  const resultBox = document.getElementById("result");
  const riskBadge = document.getElementById("riskBadge");
  const scoreLine = document.getElementById("scoreLine");
  const responseText = document.getElementById("responseText");

  riskBadge.textContent = "Checking...";
  riskBadge.className = "risk-badge";
  resultBox.classList.remove("hidden");

  try {
    const res = await fetch("/api/assess", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();

    if (data.error) {
      responseText.textContent = data.error;
      return;
    }

    riskBadge.textContent = `${data.risk_level} risk`;
    riskBadge.className = `risk-badge risk-${data.risk_level}`;

    const mlText = data.ml_probability !== null
      ? `ML score: ${data.ml_probability}% | `
      : "";
    scoreLine.textContent = `${mlText}Rule score: ${data.rule_score} | Combined: ${data.risk_score}`;

    responseText.textContent = data.response;
  } catch (err) {
    responseText.textContent = "Something went wrong. Check that the Flask server is running.";
  }
});