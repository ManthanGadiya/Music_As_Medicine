import { apiGet } from "/static/js/api.js";
import { $, clearMessage, safeText, showMessage } from "/static/js/ui.js";

function drawMoodTrend(canvasId, progressData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const width = (canvas.width = canvas.clientWidth * (window.devicePixelRatio || 1));
    const height = (canvas.height = 240 * (window.devicePixelRatio || 1));
    ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);

    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#f7fcfa";
    ctx.fillRect(0, 0, canvas.clientWidth, 240);

    const valuesPre = progressData.map((p) => p.pre_mood_level ?? 0);
    const valuesPost = progressData.map((p) => p.post_mood_level ?? 0);
    const max = 10;
    const w = canvas.clientWidth;
    const h = 240;
    const stepX = progressData.length > 1 ? (w - 40) / (progressData.length - 1) : w - 40;

    function drawLine(values, color) {
        ctx.beginPath();
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        values.forEach((v, i) => {
            const x = 20 + i * stepX;
            const y = h - 20 - (v / max) * (h - 40);
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.stroke();
    }

    drawLine(valuesPre, "#2f7ca5");
    drawLine(valuesPost, "#69b89b");
}

async function loadParticipantOptions() {
    const participantSelect = $("#participant_id");
    if (!participantSelect) return;
    const participants = (await apiGet("/participants")).data || [];
    participantSelect.innerHTML = participants
        .map((p) => `<option value="${p.participant_id}">${p.name} (ID ${p.participant_id})</option>`)
        .join("");
}

export async function initDashboard() {
    if (!$("#recentSessionsBody")) return;
    clearMessage("dashboardMessage");
    try {
        const participants = (await apiGet("/participants")).data || [];
        $("#totalParticipants").textContent = String(participants.length);

        const sessionSets = await Promise.all(
            participants.slice(0, 8).map((p) => apiGet(`/participants/${p.participant_id}/sessions`))
        );
        const sessions = sessionSets.flatMap((r) => r.data || []);
        const recent = sessions
            .sort((a, b) => String(b.session_date).localeCompare(String(a.session_date)))
            .slice(0, 8);
        $("#recentSessionsBody").innerHTML = recent
            .map(
                (s) => `
                    <tr>
                        <td>${safeText(s.session_id)}</td>
                        <td>${safeText(s.participant_id)}</td>
                        <td>${safeText(s.session_date)}</td>
                        <td>${safeText(s.duration_min)}</td>
                    </tr>
                `
            )
            .join("");
        $("#recentSessionCount").textContent = String(recent.length);
    } catch (error) {
        showMessage("dashboardMessage", error.message, "error");
    }
}

export async function initProgressReport() {
    if (!$("#progressForm")) return;
    try {
        await loadParticipantOptions();
    } catch (error) {
        showMessage("reportMessage", error.message, "error");
    }

    $("#progressForm").addEventListener("submit", async (event) => {
        event.preventDefault();
        clearMessage("reportMessage");
        try {
            const participantId = Number($("#participant_id").value);
            const progress = (await apiGet(`/participants/${participantId}/progress`)).data || [];

            const improvements = progress.map((p) => (p.post_mood_level ?? 0) - (p.pre_mood_level ?? 0));
            const averageImprovement = improvements.length
                ? (improvements.reduce((a, b) => a + b, 0) / improvements.length).toFixed(2)
                : "0.00";

            $("#sessionCount").textContent = String(progress.length);
            $("#avgMoodImprovement").textContent = averageImprovement;
            $("#feedbackSummary").textContent = progress.length
                ? "Feedback data available for selected participant"
                : "No feedback found";

            $("#progressBody").innerHTML = progress
                .map(
                    (row) => `
                        <tr>
                            <td>${safeText(row.session_id)}</td>
                            <td>${safeText(row.session_date)}</td>
                            <td>${safeText(row.pre_mood_level)}</td>
                            <td>${safeText(row.post_mood_level)}</td>
                            <td>${safeText(row.behavior_change)}</td>
                        </tr>
                    `
                )
                .join("");

            drawMoodTrend("moodChart", progress);
        } catch (error) {
            showMessage("reportMessage", error.message, "error");
        }
    });
}
