function countChars() {
  let text = document.getElementById("textInput").value;
  document.getElementById("charCount").innerText = text.length + " characters";
}

function clearText() {
  document.getElementById("textInput").value = "";
  document.getElementById("charCount").innerText = "0 characters";
  document.getElementById("result").innerHTML = "";
}

function analyzeEmotion() {
  const text = document.getElementById("textInput").value;

  if (!text.trim()) {
    alert("Please enter some text.");
    return;
  }

  fetch("/emotion", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: text }),
  })
    .then((res) => res.json())
    .then((data) => {
      let highlighted = text;
      data.keywords.forEach((word) => {
        const regex = new RegExp(`(${word})`, "gi");
        highlighted = highlighted.replace(regex, `<mark>$1</mark>`);
      });

      document.getElementById("result").innerHTML = `
        <h2>${data.emoji} ${data.emotion.toUpperCase()}</h2>
        <p><b>Confidence:</b> ${data.confidence}%</p>
        <p>${highlighted}</p>
      `;
    });
}
