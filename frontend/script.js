const API = "http://127.0.0.1:8000";

document.getElementById("analyzeForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  document.getElementById("loading").style.display = "block";
  document.getElementById("result").style.display = "none";

  const formData = new FormData(this);

  const response = await fetch(`${API}/analyze`, {
    method: "POST",
    body: formData
  });

  const data = await response.json();

  document.getElementById("loading").style.display = "none";
  document.getElementById("result").style.display = "block";

  document.getElementById("ats").innerText = data.ats_score;
  document.getElementById("match").innerText = data.jd_match;
  document.getElementById("suggestion").innerText = data.suggestion;

  let skillsHTML = "";
  for (let category in data.skills_found) {
    skillsHTML += `<p><b>${category.toUpperCase()}:</b> ${data.skills_found[category].join(", ") || "None"}</p>`;
  }
  document.getElementById("skills").innerHTML = skillsHTML;

  loadHistory();
});

async function loadHistory() {
  const res = await fetch(`${API}/history`);
  const data = await res.json();

  let rows = "";
  data.forEach(item => {
    rows += `
      <tr>
        <td>${item.name}</td>
        <td>${item.job_title}</td>
        <td>${item.ats_score}</td>
        <td>${item.jd_match}</td>
      </tr>
    `;
  });

  document.getElementById("history").innerHTML = rows;
}

loadHistory();
