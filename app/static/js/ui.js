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

export function initUI() {
    document.body.classList.add("page-enter");

    const overlay = document.querySelector(".loading-overlay");
    if (overlay) {
        setTimeout(() => overlay.classList.add("hide"), 550);
    }

    const themeToggle = document.getElementById("themeToggle");
    if (themeToggle) {
        const saved = localStorage.getItem("mts_theme");
        if (saved === "light") {
            document.body.classList.add("light-mode");
            themeToggle.textContent = "Dark Mode";
        }
        themeToggle.addEventListener("click", () => {
            document.body.classList.toggle("light-mode");
            const isLight = document.body.classList.contains("light-mode");
            localStorage.setItem("mts_theme", isLight ? "light" : "dark");
            themeToggle.textContent = isLight ? "Dark Mode" : "Light Mode";
        });
    }

    const reveals = document.querySelectorAll(".reveal");
    if (reveals.length) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) entry.target.classList.add("in");
                });
            },
            { threshold: 0.1 }
        );
        reveals.forEach((el) => observer.observe(el));
    }

    const particles = document.getElementById("particles");
    if (particles instanceof HTMLCanvasElement) {
        startParticles(particles);
    }
}

function startParticles(canvas) {
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let width = 0;
    let height = 0;
    const dots = Array.from({ length: 55 }).map(() => ({
        x: Math.random(),
        y: Math.random(),
        r: Math.random() * 1.8 + 0.6,
        vx: (Math.random() - 0.5) * 0.0004,
        vy: (Math.random() - 0.5) * 0.0004,
    }));

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }

    function frame() {
        ctx.clearRect(0, 0, width, height);
        dots.forEach((d) => {
            d.x += d.vx;
            d.y += d.vy;
            if (d.x < 0 || d.x > 1) d.vx *= -1;
            if (d.y < 0 || d.y > 1) d.vy *= -1;
            ctx.beginPath();
            ctx.fillStyle = "rgba(0, 245, 212, 0.35)";
            ctx.arc(d.x * width, d.y * height, d.r, 0, Math.PI * 2);
            ctx.fill();
        });
        requestAnimationFrame(frame);
    }

    resize();
    window.addEventListener("resize", resize);
    requestAnimationFrame(frame);
}
