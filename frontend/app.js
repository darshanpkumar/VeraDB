const BASE_URL = "http://127.0.0.1:8000";
const output = document.getElementById("output");

// Step 3: Centralized Helper Output Monitor Formatter
function showResult(data) {
    output.textContent = JSON.stringify(data, null, 4);
}

// Global Dynamic Badge Tracker Synchronization Helper Route
async function updateBadge() {
    try {
        const res = await fetch(`${BASE_URL}/stats`);
        const stats = await res.json();
        document.getElementById("vector-badge").innerText = stats.vectors;
    } catch (e) {
        console.log("Telemetry reporting infrastructure metrics target offline.");
    }
}

async function insertVector() {
    const id = Number(document.getElementById("id").value);
    const vectorInput = document.getElementById("vector").value;
    const vector = vectorInput.split(",").map(Number);

    const response = await fetch(`${BASE_URL}/insert`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, vector })
    });

    const data = await response.json();
    showResult(data);
    updateBadge();
}

async function searchVector() {
    const queryInput = document.getElementById("query").value;
    const query = queryInput.split(",").map(Number);

    const response = await fetch(`${BASE_URL}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    });

    const data = await response.json();
    showResult(data);
}

async function getStats() {
    const response = await fetch(`${BASE_URL}/stats`);
    const data = await response.json();
    showResult(data);
    updateBadge();
}

async function deleteVector() {
    const id = document.getElementById("deleteId").value;
    const response = await fetch(`${BASE_URL}/delete/${id}`, { method: "DELETE" });
    const data = await response.json();
    showResult(data);
    updateBadge();
}

async function getAlgorithms() {
    const response = await fetch(`${BASE_URL}/algorithms`);
    const data = await response.json();
    showResult(data);
}

// Execute baseline metric tracking loop probe on script boot
updateBadge();