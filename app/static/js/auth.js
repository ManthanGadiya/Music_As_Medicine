import { apiPost } from "/static/js/api.js";
import { $, clearMessage, showMessage } from "/static/js/ui.js";

const AUTH_KEY = "mts_auth";

export function setAuthSession(payload) {
    localStorage.setItem(AUTH_KEY, JSON.stringify(payload));
}

export function getAuthSession() {
    const raw = localStorage.getItem(AUTH_KEY);
    return raw ? JSON.parse(raw) : null;
}

export function clearAuthSession() {
    localStorage.removeItem(AUTH_KEY);
}

export function requireAuth() {
    if (!getAuthSession()) window.location.href = "/login";
}

export function redirectIfAuthenticated() {
    if (getAuthSession()) window.location.href = "/dashboard";
}

export function bindLogout(buttonId = "logoutBtn") {
    const btn = document.getElementById(buttonId);
    if (!btn) return;
    btn.addEventListener("click", () => {
        clearAuthSession();
        window.location.href = "/login";
    });
}

export function bindLoginForm(formId = "loginForm", messageId = "formMessage") {
    const form = document.getElementById(formId);
    if (!form) return;
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearMessage(messageId);
        try {
            const email = $("#email").value.trim();
            const password = $("#password").value.trim();
            if (!email || !password) throw new Error("Email and password are required");
            const response = await apiPost("/auth/login", { email, password });
            setAuthSession(response);
            showMessage(messageId, "Login successful. Redirecting...", "success");
            setTimeout(() => (window.location.href = "/dashboard"), 350);
        } catch (error) {
            showMessage(messageId, error.message, "error");
        }
    });
}

export function bindSignupForm(formId = "signupForm", messageId = "formMessage") {
    const form = document.getElementById(formId);
    if (!form) return;
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearMessage(messageId);
        try {
            const email = $("#email").value.trim();
            const password = $("#password").value.trim();
            const confirmPassword = $("#confirm_password").value.trim();
            if (!email || !password) throw new Error("Email and password are required");
            if (password !== confirmPassword) throw new Error("Passwords do not match");

            // No signup endpoint is defined, so signup follows login behavior.
            const response = await apiPost("/auth/login", { email, password });
            setAuthSession(response);
            showMessage(messageId, "Sign up successful. Redirecting...", "success");
            setTimeout(() => (window.location.href = "/dashboard"), 350);
        } catch (error) {
            showMessage(messageId, error.message, "error");
        }
    });
}
