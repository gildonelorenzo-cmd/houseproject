/* ---------------- ADMIN PANEL ---------------- */
function openAdmin() {
    document.getElementById("adminPanel").classList.remove("hidden");
}

function closeAdmin() {
    document.getElementById("adminPanel").classList.add("hidden");
}

/* ---------------- SCORE SAVE / LOAD ---------------- */
function saveScores() {
    const scores = {
        acrobats: document.getElementById("score-acrobats").textContent,
        quicksilver: document.getElementById("score-quicksilver").textContent,
        druids: document.getElementById("score-druids").textContent,
        bravehearts: document.getElementById("score-bravehearts").textContent
    };
    localStorage.setItem("houseScores", JSON.stringify(scores));
}

function loadScores() {
    const saved = localStorage.getItem("houseScores");
    if (saved) {
        const scores = JSON.parse(saved);
        document.getElementById("score-acrobats").textContent = scores.acrobats;
        document.getElementById("score-quicksilver").textContent = scores.quicksilver;
        document.getElementById("score-druids").textContent = scores.druids;
        document.getElementById("score-bravehearts").textContent = scores.bravehearts;
    }
}

/* ---------------- MANUAL SCORE CHANGES ---------------- */
function applyManualScores() {

    const fields = [
        { input: "admin-acrobats", score: "score-acrobats" },
        { input: "admin-quicksilver", score: "score-quicksilver" },
        { input: "admin-druids", score: "score-druids" },
        { input: "admin-bravehearts", score: "score-bravehearts" }
    ];

    fields.forEach(item => {
        const inputEl = document.getElementById(item.input);
        if (inputEl.value.trim() !== "") {
            const scoreEl = document.getElementById(item.score);
            const current = parseInt(scoreEl.textContent);
            const change = parseInt(inputEl.value);
            scoreEl.textContent = current + change;
        }
        inputEl.value = "";
    });

    saveScores();
    updateLeaderboard();
    closeAdmin();
}

/* ---------------- LEADERBOARD ---------------- */
function updateLeaderboard() {
    const scores = [
        { name: "Acrobats", score: parseInt(document.getElementById("score-acrobats").textContent), class: "lb-acrobats" },
        { name: "Quicksilver", score: parseInt(document.getElementById("score-quicksilver").textContent), class: "lb-quicksilver" },
        { name: "Druids", score: parseInt(document.getElementById("score-druids").textContent), class: "lb-druids" },
        { name: "Bravehearts", score: parseInt(document.getElementById("score-bravehearts").textContent), class: "lb-bravehearts" }
    ];

    scores.sort((a, b) => b.score - a.score);

    const list = document.getElementById("leaderboard-list");
    list.innerHTML = "";

    scores.forEach(entry => {
        const li = document.createElement("li");
        li.className = entry.class;
        li.innerHTML = `${entry.name} <span>${entry.score}</span>`;
        list.appendChild(li);
    });
}

/* ---------------- DARK MODE ---------------- */
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}

/* ---------------- INITIALIZE ---------------- */
loadScores();
updateLeaderboard();
