class TranscriptManager:

    def __init__(self):
        self.history = []

    def add(self, speaker, text):
        self.history.append({
            "speaker": speaker,
            "text": text
        })

    def get_full_text(self):
        return "\n".join(
            f"{h['speaker']}: {h['text']}" for h in self.history
        )
