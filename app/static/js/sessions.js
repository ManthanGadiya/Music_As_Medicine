import { apiGet, apiPost } from "/static/js/api.js";
import { $, clearMessage, getQueryParam, showMessage } from "/static/js/ui.js";

async function loadSelectors() {
    const [participantsRes, musicRes] = await Promise.all([apiGet("/participants"), apiGet("/music")]);
    const participants = participantsRes.data || [];
    const tracks = musicRes.data || [];

    const participantSelect = $("#participant_id");
    const musicSelect = $("#music_id");
    if (participantSelect) {
        participantSelect.innerHTML = participants
            .map((p) => `<option value="${p.participant_id}">${p.name} (ID ${p.participant_id})</option>`)
            .join("");
    }
    if (musicSelect) {
        musicSelect.innerHTML = tracks
            .map((m) => `<option value="${m.music_id}">${m.title} (ID ${m.music_id})</option>`)
            .join("");
    }
}

export async function initSessionPage() {
    if (!$("#sessionForm")) return;
    try {
        await loadSelectors();
    } catch (error) {
        showMessage("sessionMessage", error.message, "error");
    }

    $("#sessionForm").addEventListener("submit", async (event) => {
        event.preventDefault();
        clearMessage("sessionMessage");
        try {
            const payload = {
                participant_id: Number($("#participant_id").value),
                therapist_id: Number($("#therapist_id").value),
                music_id: Number($("#music_id").value),
                session_date: $("#session_date").value,
                duration_min: Number($("#duration_min").value),
                session_notes: $("#session_notes").value.trim() || null,
            };
            if (!payload.session_date || Number.isNaN(payload.duration_min)) {
                throw new Error("Session date and duration are required");
            }
            const response = await apiPost("/sessions", payload);
            const sessionId = response.data?.session_id;
            localStorage.setItem("last_session_id", String(sessionId || ""));
            localStorage.setItem("last_participant_id", String(payload.participant_id || ""));
            showMessage("sessionMessage", `Session started (ID: ${sessionId})`, "success");
            setTimeout(() => {
                window.location.href = `/pre-assessment?session_id=${sessionId}&participant_id=${payload.participant_id}`;
            }, 300);
        } catch (error) {
            showMessage("sessionMessage", error.message, "error");
        }
    });
}

export function initPreAssessmentPage() {
    const form = $("#preAssessmentForm");
    if (!form) return;
    const querySessionId = getQueryParam("session_id");
    const queryParticipantId = getQueryParam("participant_id");
    const lastSessionId = querySessionId || localStorage.getItem("last_session_id");
    const lastParticipantId = queryParticipantId || localStorage.getItem("last_participant_id");
    if (lastSessionId) $("#session_id").value = lastSessionId;
    if (lastParticipantId) localStorage.setItem("last_participant_id", String(lastParticipantId));

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearMessage("preMessage");
        try {
            const sessionId = Number($("#session_id").value);
            const payload = {
                mood_level: Number($("#mood_level").value),
                stress_level: Number($("#stress_level").value),
                attention_level: Number($("#attention_level").value),
                notes: $("#notes").value.trim() || null,
            };
            await apiPost(`/sessions/${sessionId}/pre-assessment`, payload);
            showMessage("preMessage", "Pre-assessment saved", "success");
            const participantId = localStorage.getItem("last_participant_id") || "";
            setTimeout(() => {
                window.location.href = `/post-feedback?session_id=${sessionId}&participant_id=${participantId}`;
            }, 300);
        } catch (error) {
            showMessage("preMessage", error.message, "error");
        }
    });
}

export function initPostFeedbackPage() {
    const form = $("#postFeedbackForm");
    if (!form) return;
    const querySessionId = getQueryParam("session_id");
    const queryParticipantId = getQueryParam("participant_id");
    const lastSessionId = querySessionId || localStorage.getItem("last_session_id");
    const lastParticipantId = queryParticipantId || localStorage.getItem("last_participant_id");
    if (lastSessionId) $("#session_id").value = lastSessionId;
    if (lastParticipantId) localStorage.setItem("last_participant_id", String(lastParticipantId));

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearMessage("postMessage");
        try {
            const sessionId = Number($("#session_id").value);
            const payload = {
                mood_level: Number($("#mood_level").value),
                behavior_change: $("#behavior_change").value.trim() || null,
                attention_change: $("#attention_change").value.trim() || null,
                social_response: $("#social_response").value.trim() || null,
                comments: $("#comments").value.trim() || null,
            };
            await apiPost(`/sessions/${sessionId}/feedback`, payload);
            showMessage("postMessage", "Post-session feedback saved", "success");
            const participantId = localStorage.getItem("last_participant_id") || "";
            setTimeout(() => {
                window.location.href = `/progress-report?participant_id=${participantId}`;
            }, 300);
        } catch (error) {
            showMessage("postMessage", error.message, "error");
        }
    });
}
