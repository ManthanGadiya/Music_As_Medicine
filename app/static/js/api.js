const API_BASE = `${window.location.origin}/api/v1`;

async function request(path, options = {}) {
    const config = {
        method: options.method || "GET",
        headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    };
    if (options.body) {
        config.body = JSON.stringify(options.body);
    }

    const response = await fetch(`${API_BASE}${path}`, config);
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(data.detail || "Unable to process request");
    }
    return data;
}

export function apiGet(path) {
    return request(path, { method: "GET" });
}

export function apiPost(path, body) {
    return request(path, { method: "POST", body });
}
