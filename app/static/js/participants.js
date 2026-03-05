import { apiGet, apiPost } from "/static/js/api.js";
import { $, clearMessage, getQueryParam, safeText, showMessage } from "/static/js/ui.js";

function participantRowMarkup(row) {
    return `
        <tr data-id="${row.participant_id}">
            <td>${safeText(row.name)}</td>
            <td>${safeText(row.age)}</td>
            <td>${safeText(row.category)}</td>
            <td>${safeText(row.special_need_type)}</td>
        </tr>
    `;
}

export async function initParticipantsPage() {
    const tableBody = $("#participantsBody");
    if (!tableBody) return;

    let allParticipants = [];

    async function loadParticipants() {
        const response = await apiGet("/participants");
        allParticipants = response.data || [];
        renderRows(allParticipants);
    }

    function renderRows(items) {
        tableBody.innerHTML = items.map(participantRowMarkup).join("");
        tableBody.querySelectorAll("tr").forEach((row) => {
            row.addEventListener("click", () => {
                window.location.href = `/participant-profile?id=${row.dataset.id}`;
            });
        });
    }

    $("#searchInput").addEventListener("input", (event) => {
        const q = event.target.value.trim().toLowerCase();
        const filtered = allParticipants.filter((item) =>
            `${item.name} ${item.category} ${item.special_need_type || ""}`.toLowerCase().includes(q)
        );
        renderRows(filtered);
    });

    $("#createParticipantForm").addEventListener("submit", async (event) => {
        event.preventDefault();
        clearMessage("participantsMessage");
        try {
            const payload = {
                name: $("#name").value.trim(),
                age: Number($("#age").value),
                gender: $("#gender").value.trim(),
                category: $("#category").value,
                special_need_type: $("#special_need_type").value.trim() || null,
                medical_history: $("#medical_history").value.trim() || null,
            };
            if (!payload.name || Number.isNaN(payload.age) || !payload.gender) {
                throw new Error("Name, age, and gender are required");
            }
            await apiPost("/participants", payload);
            showMessage("participantsMessage", "Participant created successfully", "success");
            event.target.reset();
            await loadParticipants();
        } catch (error) {
            showMessage("participantsMessage", error.message, "error");
        }
    });

    try {
        await loadParticipants();
    } catch (error) {
        showMessage("participantsMessage", error.message, "error");
    }
}

export async function initParticipantProfilePage() {
    const profileBlock = $("#profileDetails");
    if (!profileBlock) return;

    const participantId = getQueryParam("id") || $("#participantIdInput").value;
    if (!participantId) {
        showMessage("profileMessage", "Participant ID is required", "error");
        return;
    }
    $("#participantIdInput").value = participantId;

    async function loadProfile(id) {
        const [participantRes, sessionsRes, progressRes] = await Promise.all([
            apiGet(`/participants/${id}`),
            apiGet(`/participants/${id}/sessions`),
            apiGet(`/participants/${id}/progress`),
        ]);

        const participant = participantRes.data;
        const sessions = sessionsRes.data || [];
        const progress = progressRes.data || [];
        const avgImprovement =
            progress.length > 0
                ? (
                      progress
                          .map((p) => (p.post_mood_level ?? 0) - (p.pre_mood_level ?? 0))
                          .reduce((sum, v) => sum + v, 0) / progress.length
                  ).toFixed(2)
                : "0.00";

        profileBlock.innerHTML = `
            <p><strong>Name:</strong> ${safeText(participant.name)}</p>
            <p><strong>Age:</strong> ${safeText(participant.age)}</p>
            <p><strong>Gender:</strong> ${safeText(participant.gender)}</p>
            <p><strong>Category:</strong> ${safeText(participant.category)}</p>
            <p><strong>Special Need Type:</strong> ${safeText(participant.special_need_type)}</p>
            <p><strong>Medical History:</strong> ${safeText(participant.medical_history)}</p>
        `;
        $("#progressSummary").textContent = `Sessions: ${sessions.length} | Avg Mood Improvement: ${avgImprovement}`;
        $("#sessionsBody").innerHTML = sessions
            .map(
                (s) => `
                    <tr>
                        <td>${safeText(s.session_id)}</td>
                        <td>${safeText(s.session_date)}</td>
                        <td>${safeText(s.duration_min)}</td>
                        <td>${safeText(s.session_notes)}</td>
                    </tr>
                `
            )
            .join("");
    }

    $("#loadProfileBtn").addEventListener("click", async () => {
        clearMessage("profileMessage");
        try {
            await loadProfile($("#participantIdInput").value.trim());
        } catch (error) {
            showMessage("profileMessage", error.message, "error");
        }
    });

    try {
        await loadProfile(participantId);
    } catch (error) {
        showMessage("profileMessage", error.message, "error");
    }
}
