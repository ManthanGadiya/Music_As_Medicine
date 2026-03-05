import { apiGet, apiPost } from "/static/js/api.js";
import { $, clearMessage, safeText, showMessage } from "/static/js/ui.js";

export async function initMusicPage() {
    const body = $("#musicBody");
    if (!body) return;

    async function loadMusic() {
        const response = await apiGet("/music");
        const tracks = response.data || [];
        body.innerHTML = tracks
            .map(
                (t) => `
                    <tr>
                        <td>${safeText(t.title)}</td>
                        <td>${safeText(t.genre)}</td>
                        <td>${safeText(t.instrument)}</td>
                        <td>${safeText(t.tempo)}</td>
                        <td>${safeText(t.duration_sec)}</td>
                    </tr>
                `
            )
            .join("");
    }

    $("#musicForm").addEventListener("submit", async (event) => {
        event.preventDefault();
        clearMessage("musicMessage");
        try {
            const payload = {
                title: $("#title").value.trim(),
                genre: $("#genre").value.trim(),
                instrument: $("#instrument").value.trim(),
                tempo: Number($("#tempo").value),
                frequency_range: $("#frequency_range").value.trim(),
                duration_sec: Number($("#duration_sec").value),
                file_path: $("#file_path").value.trim(),
            };
            if (!payload.title || !payload.genre || !payload.instrument || Number.isNaN(payload.tempo)) {
                throw new Error("Title, genre, instrument, and tempo are required");
            }
            await apiPost("/music", payload);
            showMessage("musicMessage", "Track added successfully", "success");
            event.target.reset();
            await loadMusic();
        } catch (error) {
            showMessage("musicMessage", error.message, "error");
        }
    });

    try {
        await loadMusic();
    } catch (error) {
        showMessage("musicMessage", error.message, "error");
    }
}
