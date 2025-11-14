const ADMIN_PASSWORD = "1234"; // ← change this to your real password

// Open Admin Panel (asks only for password)
function openAdmin() {
    const entered = prompt("Enter Admin Password:");

    if (entered === ADMIN_PASSWORD) {
        document.getElementById("adminPanel").classList.remove("hidden");
    } else if (entered !== null) {
        alert("Incorrect password.");
    }
}

function closeAdmin() {
    document.getElementById("adminPanel").classList.add("hidden");
}

// Apply Manual Scores
function applyManualScores() {
    const houses = ["acrobats", "quicksilver", "druids", "bravehearts"];

    houses.forEach(h => {
        const input = document.getElementById(`admin-${h}`);
        const score = parseInt(input.value);

        if (!isNaN(score) && score >= 0) {
            document.getElementById(`score-${h}`).textContent = score;
        }
    });

    alert("Scores updated successfully!");
    closeAdmin();
}
