const API_BASE = "http://127.0.0.1:8000/api/v1";

async function apiRequest(path, method = "GET", body = null) {
    const config = { method, headers: { "Content-Type": "application/json" } };
    if (body) {
        config.body = JSON.stringify(body);
    }
    const response = await fetch(`${API_BASE}${path}`, config);
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.detail || "Request failed");
    }
    return data;
}

function showJson(elementId, data) {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = JSON.stringify(data, null, 2);
}

function getIntValue(id) {
    const value = document.getElementById(id).value;
    return value === "" ? null : Number(value);
}
