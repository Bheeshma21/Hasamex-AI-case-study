import re
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def clean_text(text: str) -> str:
    """Fix common encoding artifacts and normalize whitespace."""
    replacements = {
        "â€“": "–",
        "â€”": "—",
        "â€™": "'",
        "â€œ": '"',
        "â€": '"',
    }

    for bad, good in replacements.items():
        text = text.replace(bad, good)

    return text.strip()


def parse_transcript(file_path):
    """
    Parse a Hasamex transcript into structured timestamped segments.
    """

    file_path = Path(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        text = clean_text(file.read())

    lines = [clean_text(line) for line in text.splitlines()]

    # -------- Transcript metadata --------
    expert = ""
    role = ""
    market = ""

    if lines:
        # Example:
        # Expert 1 – Dr. Jean Martin
        first_line = lines[0]

        if "–" in first_line:
            expert = first_line.split("–", 1)[1].strip()
        elif "-" in first_line:
            expert = first_line.split("-", 1)[1].strip()

    for line in lines:
        if line.startswith("Role:"):
            role = line.replace("Role:", "", 1).strip()

        elif line.startswith("Market:"):
            market = line.replace("Market:", "", 1).strip()

    # -------- Timestamped dialogue --------
    timestamp_pattern = re.compile(r"^\d{2}:\d{2}$")

    segments = []
    current_timestamp = None

    for line in lines:

        if not line:
            continue

        if timestamp_pattern.match(line):
            current_timestamp = line
            continue

        if current_timestamp and ":" in line:

            speaker, content = line.split(":", 1)

            speaker = speaker.strip()
            content = content.strip()

            if content:
                segments.append(
                    {
                        "expert": expert,
                        "role": role,
                        "market": market,
                        "timestamp": current_timestamp,
                        "speaker": speaker,
                        "text": content,
                        "source_file": file_path.name,
                    }
                )

    return {
        "expert": expert,
        "role": role,
        "market": market,
        "source_file": file_path.name,
        "segments": segments,
    }


def load_all_transcripts():
    """Load all transcript files from the data directory."""

    transcript_files = sorted(DATA_DIR.glob("Transcript_*.txt"))

    transcripts = []

    for file_path in transcript_files:
        transcripts.append(parse_transcript(file_path))

    return transcripts


def load_interview_guide():
    """Extract numbered questions from the interview guide."""

    guide_path = DATA_DIR / "Interview_Guide.txt"

    with open(guide_path, "r", encoding="utf-8") as file:
        text = clean_text(file.read())

    questions = []

    for line in text.splitlines():
        line = clean_text(line)

        match = re.match(r"^\d+\.\s+(.*)", line)

        if match:
            questions.append(match.group(1).strip())

    return questions


if __name__ == "__main__":

    transcripts = load_all_transcripts()
    questions = load_interview_guide()

    print("\nHASAMEX TRANSCRIPT PARSER TEST")
    print("=" * 60)

    print(f"\nTranscripts loaded: {len(transcripts)}")
    print(f"Interview questions: {len(questions)}")

    for transcript in transcripts:

        print("\n" + "-" * 60)
        print(f"Expert: {transcript['expert']}")
        print(f"Role: {transcript['role']}")
        print(f"Market: {transcript['market']}")
        print(f"Segments: {len(transcript['segments'])}")

        for segment in transcript["segments"][:2]:
            print(
                f"\n[{segment['timestamp']}] "
                f"{segment['speaker']}: {segment['text']}"
            )

    print("\n" + "=" * 60)
    print("INTERVIEW GUIDE")

    for number, question in enumerate(questions, start=1):
        print(f"{number}. {question}")