import re

class ResumeParser:

    def parse(self, resume_text):
        sections = re.split(r'\n[A-Z ]+\n', resume_text)

        return {
            "raw_text": resume_text,
            "sections": sections
        }
