const API = "https://ai-resume-analyzer-0ovp.onrender.com";

// ===============================
// ELEMENT REFERENCES
// ===============================
const form = document.getElementById("analyzeForm");
const loader = document.getElementById("loader");
const resultBox = document.getElementById("result");
const skillsBox = document.getElementById("skills");
const historyTable = document.getElementById("history");

const dropZone = document.getElementById("dropZone");
const resumeInput = document.getElementById("resumeInput");

// ===============================
// DRAG & DROP FUNCTIONALITY
// ===============================
dropZone.addEventListener("click", () => resumeInput.click());

dropZone.addEventListener("dragover", e => {
  e.preventDefault();
  dropZone.classList.add("active");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("active");
});

dropZone.addEventListener("drop", e => {
  e.preventDefault();
  dropZone.classList.remove("active");

  const file = e.dataTransfer.files[0];
  if (!file) return;

  if (file.type !== "application/pdf") {
    alert("Please upload a PDF file only.");
    return;
  }

  // ✅ Attach dropped file to real form input
  const dataTransfer = new DataTransfer();
  dataTransfer.items.add(file);
  resumeInput.files = dataTransfer.files;

  // ✅ Update UI text
  dropZone.querySelector("p").innerText = file.name;
});

// ===============================
// FORM SUBMIT HANDLER
// ===============================
form.addEventListener("submit", async function (e) {
  e.preventDefault();

  // ✅ Frontend validation
  const resumeFile = resumeInput.files[0];
  if (!resumeFile) {
    alert("Please upload your resume.");
    return;
  }

  // ✅ Show loader & hide result
  loader.classList.remove("hidden");
  resultBox.classList.add("hidden");

  const formData = new FormData(form);

  try {
    const response = await fetch(`${API}/analyze`, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("Server error while analyzing.");
    }

    const data = await response.json();

    // ✅ Hide loader & show result
    loader.classList.add("hidden");
    resultBox.classList.remove("hidden");
    resultBox.classList.add("result");

    document.getElementById("ats").innerText = data.ats_score;
    document.getElementById("match").innerText = data.jd_match;
    document.getElementById("suggestion").innerText = data.suggestion;

    // ✅ Skills rendering
    let skillsHTML = "";
    for (let category in data.skills_found) {
      const list = data.skills_found[category]?.length
        ? data.skills_found[category].join(", ")
        : "None";

      skillsHTML += `<p><b>${category.toUpperCase()}:</b> ${list}</p>`;
    }

    skillsBox.innerHTML = skillsHTML;

    // ✅ Reload history
    loadHistory();

  } catch (err) {
    loader.classList.add("hidden");
    alert("❌ Failed to analyze resume. Please try again.");
    console.error(err);
  }
});

// ===============================
// LOAD HISTORY
// ===============================
async function loadHistory() {
  try {
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

    historyTable.innerHTML = rows;

  } catch (error) {
    console.error("Error loading history:", error);
  }
}

// ===============================
// INITIAL PAGE LOAD
// ===============================
loadHistory();
