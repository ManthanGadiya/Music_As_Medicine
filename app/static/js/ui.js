export function $(selector) {
    return document.querySelector(selector);
}

export function showMessage(targetId, message, type = "success") {
    const el = document.getElementById(targetId);
    if (!el) return;
    el.textContent = message;
    el.className = `msg show ${type}`;
}

export function clearMessage(targetId) {
    const el = document.getElementById(targetId);
    if (!el) return;
    el.textContent = "";
    el.className = "msg";
}

export function safeText(value) {
    return value ?? "-";
}

export function getQueryParam(key) {
    return new URLSearchParams(window.location.search).get(key);
}

export function requireValue(value, label) {
    if (value === undefined || value === null || value === "") {
        throw new Error(`${label} is required`);
    }
}
