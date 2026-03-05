const API_BASE = `${window.location.origin}/api/v1`;

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

function setAuth(authPayload) {
    localStorage.setItem("auth", JSON.stringify(authPayload));
}

function getAuth() {
    const raw = localStorage.getItem("auth");
    return raw ? JSON.parse(raw) : null;
}

function clearAuth() {
    localStorage.removeItem("auth");
}

function requireAuth() {
    if (!getAuth()) {
        window.location.href = "/login";
    }
}

function ensureLoggedOutUsersStayOnLogin() {
    if (getAuth()) {
        window.location.href = "/dashboard";
    }
}

function bindLogout(buttonId = "logoutBtn") {
    const btn = document.getElementById(buttonId);
    if (!btn) return;
    btn.addEventListener("click", () => {
        clearAuth();
        window.location.href = "/login";
    });
}
