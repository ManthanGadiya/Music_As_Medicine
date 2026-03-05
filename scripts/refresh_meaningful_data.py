from datetime import UTC, date, datetime, time, timedelta

from app.database import get_connection


PARTICIPANT_PROFILES = [
    ("Aarav Sharma", 9, "Male", "special_child", "Autism Spectrum Disorder", "Sensory sensitivity and delayed speech."),
    ("Anaya Patel", 11, "Female", "special_child", "ADHD", "Attention regulation challenges in classroom settings."),
    ("Vihaan Reddy", 8, "Male", "special_child", "Autism Spectrum Disorder", "Difficulty with social interaction and transitions."),
    ("Ira Nair", 10, "Female", "special_child", "Learning Disability", "Reading and processing delays."),
    ("Kabir Singh", 12, "Male", "neurotypical", None, "Mild performance anxiety before exams."),
    ("Meera Joshi", 7, "Female", "special_child", "Speech Delay", "Limited expressive vocabulary."),
    ("Arjun Mehta", 13, "Male", "neurotypical", None, "Stress due to competitive academics."),
    ("Siya Verma", 9, "Female", "special_child", "ADHD", "Restlessness and low sustained attention."),
    ("Reyansh Gupta", 10, "Male", "special_child", "Autism Spectrum Disorder", "Low eye contact and repetitive behavior."),
    ("Diya Iyer", 8, "Female", "special_child", "Sensory Processing Disorder", "Overwhelm in noisy environments."),
    ("Rohan Kapoor", 14, "Male", "neurotypical", None, "Low motivation and mood fluctuations."),
    ("Myra Das", 11, "Female", "special_child", "ADHD", "Impulsivity and emotional dysregulation."),
    ("Neil Thomas", 12, "Male", "special_child", "Autism Spectrum Disorder", "Prefers routine and struggles with change."),
]

THERAPISTS = [
    ("Dr. Nisha Rao", "Lead Therapist", "M.A. Music Therapy", "therapist@mail.com"),
    ("Aditi Menon", "Therapist", "B.M.T. Clinical Music Therapy", "therapist2@mail.com"),
    ("Karan Bhatia", "Therapist", "M.Sc. Psychology + Music Therapy", "therapist3@mail.com"),
    ("Pooja Sethi", "Therapist", "PG Diploma in Music Therapy", "therapist4@mail.com"),
    ("Rahul Nambiar", "Therapist", "B.A. Music + Child Counseling", "therapist5@mail.com"),
    ("Sneha Kulkarni", "Therapist", "M.A. Special Education", "therapist6@mail.com"),
    ("Vikram Joshi", "Therapist", "Certified Neurologic Music Therapist", "therapist7@mail.com"),
    ("Tanya Ghosh", "Therapist", "M.Phil. Clinical Psychology", "therapist8@mail.com"),
    ("Pranav Arora", "Therapist", "Advanced Diploma Music Therapy", "therapist9@mail.com"),
    ("Ishita Sen", "Therapist", "B.Ed. Special Needs + Music", "therapist10@mail.com"),
]

MUSIC_TRACKS = [
    ("Calm Piano Breathing", "instrumental", "piano", 58.0, "low", 600, "/music/calm_piano_breathing.mp3"),
    ("Morning Flute Focus", "meditation", "flute", 62.0, "mid", 540, "/music/morning_flute_focus.mp3"),
    ("Gentle Strings Relaxation", "instrumental", "violin", 56.0, "low", 720, "/music/gentle_strings_relaxation.mp3"),
    ("Soft Nature Ambience", "ambient", "nature", 48.0, "low", 900, "/music/soft_nature_ambience.mp3"),
    ("Rhythm Regulation Drums", "rhythmic", "drums", 74.0, "mid", 420, "/music/rhythm_regulation_drums.mp3"),
    ("Evening Harp Calm", "instrumental", "harp", 52.0, "low", 660, "/music/evening_harp_calm.mp3"),
    ("Binaural Alpha Focus", "therapy", "synth", 60.0, "mid", 480, "/music/binaural_alpha_focus.mp3"),
    ("Mindful Guitar Flow", "instrumental", "guitar", 64.0, "mid", 510, "/music/mindful_guitar_flow.mp3"),
    ("Ocean Pulse Meditation", "meditation", "nature", 50.0, "low", 780, "/music/ocean_pulse_meditation.mp3"),
    ("Balanced Breath Chimes", "therapy", "chimes", 55.0, "high", 450, "/music/balanced_breath_chimes.mp3"),
    ("Guided Relaxation Piano", "instrumental", "piano", 57.0, "low", 630, "/music/guided_relaxation_piano.mp3"),
]

BEHAVIOR_CHOICES = [
    "Reduced restlessness",
    "Improved emotional calm",
    "Better self-regulation",
    "Increased willingness to participate",
]

ATTENTION_CHOICES = [
    "Sustained attention improved",
    "Able to follow instructions better",
    "Improved task engagement",
    "Less distractibility observed",
]

SOCIAL_CHOICES = [
    "More eye contact and interaction",
    "Responded positively to therapist cues",
    "Initiated communication during session",
    "Smiled and participated with peers",
]


def refresh_meaningful_data() -> None:
    with get_connection() as connection:
        participant_ids = [row[0] for row in connection.execute("SELECT participant_id FROM Participants ORDER BY participant_id")]
        therapist_ids = [row[0] for row in connection.execute("SELECT therapist_id FROM Therapists ORDER BY therapist_id")]
        music_ids = [row[0] for row in connection.execute("SELECT music_id FROM Music ORDER BY music_id")]

        for idx, pid in enumerate(participant_ids):
            profile = PARTICIPANT_PROFILES[idx % len(PARTICIPANT_PROFILES)]
            connection.execute(
                """
                UPDATE Participants
                SET name = ?, age = ?, gender = ?, category = ?, special_need_type = ?, medical_history = ?, created_at = ?
                WHERE participant_id = ?
                """,
                (*profile, datetime.now(UTC).isoformat(), pid),
            )

        for idx, tid in enumerate(therapist_ids):
            therapist = THERAPISTS[idx % len(THERAPISTS)]
            connection.execute(
                """
                UPDATE Therapists
                SET name = ?, role = ?, qualification = ?, contact_email = ?
                WHERE therapist_id = ?
                """,
                (*therapist, tid),
            )

        for idx, mid in enumerate(music_ids):
            track = MUSIC_TRACKS[idx % len(MUSIC_TRACKS)]
            connection.execute(
                """
                UPDATE Music
                SET title = ?, genre = ?, instrument = ?, tempo = ?, frequency_range = ?, duration_sec = ?, file_path = ?
                WHERE music_id = ?
                """,
                (*track, mid),
            )

        # Rebuild session and assessment data so each participant has exactly 4 complete sessions.
        connection.execute("DELETE FROM PreSessionAssessment")
        connection.execute("DELETE FROM PostSessionFeedback")
        connection.execute("DELETE FROM Sessions")

        session_date_start = date(2026, 1, 6)

        for p_idx, pid in enumerate(participant_ids):
            base_pre_mood = 3 + (p_idx % 3)
            for round_idx in range(4):
                therapist_id = therapist_ids[(p_idx + round_idx) % len(therapist_ids)]
                music_id = music_ids[(p_idx * 2 + round_idx) % len(music_ids)]
                session_date = session_date_start + timedelta(days=(p_idx * 4) + (round_idx * 7))
                start_time = time(hour=10 + (round_idx % 3), minute=0)
                duration = 25 + (round_idx * 5)
                pre_mood = min(10, base_pre_mood + round_idx)
                post_mood = min(10, pre_mood + 2)
                stress = max(1, 8 - round_idx - (p_idx % 2))
                attention = min(10, 4 + round_idx + (p_idx % 3))

                session_cursor = connection.execute(
                    """
                    INSERT INTO Sessions (participant_id, therapist_id, music_id, session_date, start_time, duration_min, session_notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        pid,
                        therapist_id,
                        music_id,
                        session_date.isoformat(),
                        start_time.isoformat(),
                        duration,
                        f"Session {round_idx + 1}: focused on rhythm and guided breathing exercises.",
                    ),
                )
                session_id = session_cursor.lastrowid

                connection.execute(
                    """
                    INSERT INTO PreSessionAssessment (session_id, mood_level, stress_level, attention_level, notes)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        session_id,
                        pre_mood,
                        stress,
                        attention,
                        "Participant arrived with mild anxiety; baseline recorded before intervention.",
                    ),
                )

                connection.execute(
                    """
                    INSERT INTO PostSessionFeedback (session_id, mood_level, behavior_change, attention_change, social_response, comments)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        session_id,
                        post_mood,
                        BEHAVIOR_CHOICES[(p_idx + round_idx) % len(BEHAVIOR_CHOICES)],
                        ATTENTION_CHOICES[(p_idx + round_idx) % len(ATTENTION_CHOICES)],
                        SOCIAL_CHOICES[(p_idx + round_idx) % len(SOCIAL_CHOICES)],
                        "Therapeutic response was positive; continue similar music pattern next session.",
                    ),
                )


if __name__ == "__main__":
    refresh_meaningful_data()
    print("Database records refreshed with meaningful data and 4 sessions per participant.")
