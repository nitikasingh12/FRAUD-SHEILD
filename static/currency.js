const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");

imageInput.addEventListener("change", () => {
  preview.innerHTML = "";
  const file = imageInput.files[0];
  if (!file) return;
  const img = document.createElement("img");
  img.src = URL.createObjectURL(file);
  preview.appendChild(img);
});

document.getElementById("checkBtn").addEventListener("click", async () => {
  const file = imageInput.files[0];
  if (!file) return;

  const resultBox = document.getElementById("result");
  const riskBadge = document.getElementById("riskBadge");
  const responseText = document.getElementById("responseText");

  riskBadge.textContent = "Checking...";
  riskBadge.className = "risk-badge";
  resultBox.classList.remove("hidden");
  responseText.textContent = "";

  const formData = new FormData();
  formData.append("image", file);

  try {
    const res = await fetch("/api/currency-check", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();

    if (data.error) {
      responseText.textContent = data.error;
      riskBadge.textContent = "Error";
      return;
    }

    const isReal = data.label === "real";
    riskBadge.textContent = isReal ? "Looks genuine" : "Possibly fake";
    riskBadge.className = `risk-badge risk-${isReal ? "Low" : "High"}`;
    responseText.textContent = `Confidence: ${data.confidence}%. This is a prototype model trained on limited data — always cross-check with official RBI security features for real decisions.`;
  } catch (err) {
    responseText.textContent = "Something went wrong. Check that the Flask server is running.";
  }
});