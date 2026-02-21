from dataclasses import dataclass, field
import re
from openai import OpenAI
import pdfplumber
import os

@dataclass
class ResumeAnalyzer:
    resume_path: str
    job_path: str
    resume_text: str = field(init=False, default="")
    job_text: str = field(init=False, default="")

    COMMON_SKILL_PHRASES = [
        "machine learning",
        "deep learning",
        "data science",
        "data analysis",
        "natural language processing",
        "computer vision",
        "web development",
        "backend development",
        "frontend development",
        "object oriented programming",
        "rest api",
        "sql database",
        "cloud computing",
        "data structures",
        "artificial intelligence"
    ]

    def extract_skill_phrases(self):
        job_phrases = []
        resume_phrases = []
        
        for phrase in self.COMMON_SKILL_PHRASES:
            if phrase in self.job_text:
                job_phrases.append(phrase)
            if phrase in self.resume_text:
                resume_phrases.append(phrase)

        return set(job_phrases), set(resume_phrases)

    def load_files(self):
        """Read resume and job description files"""
        try:
            if self.resume_path.endswith(".pdf"):
                self.resume_text = extract_text_from_pdf(self.resume_path).lower()
            else:
                with open(self.resume_path, "r", encoding="utf-8") as f:
                    self.resume_text = f.read().lower()
            
            if self.job_path.endswith(".pdf"):
                self.job_text = extract_text_from_pdf(self.job_path).lower()
            else:
                with open(self.job_path, "r", encoding="utf-8") as f:
                    self.job_text = f.read().lower()

        except FileNotFoundError as e:
            print(f"Error loading file: {e}")
    

    def calculate_basic_match(self):
        # Extract words using regex
        job_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", self.job_text))
        resume_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", self.resume_text))

        # Remove Common filter words
        stopwords = {
            "and", "the", "with", "for", "are", "you", "your", "from", "that", "this",
            "have", "has", "had", "will", "shall", "can", "could", "would", "should",
            "may", "might", "into", "about", "onto", "over", "under", "between",
            "within", "using", "use", "used", "through", "responsible", "rewuired",
            "including"
        }
        job_keywords = job_words - stopwords

        matched_words = job_keywords.intersection(resume_words)
        missing_words = job_keywords - resume_words

        # Phrases matching
        job_phrases, resume_phrases = self.extract_skill_phrases()
        matched_phrases = job_phrases.intersection(resume_phrases)
        missing_phrases = job_phrases - resume_phrases

        # Weighted scoring
        WORD_WEIGHT = 1
        PHRASE_WEIGHT = 3

        total_possible_score = (len(job_keywords) * WORD_WEIGHT) + (len(job_phrases) * PHRASE_WEIGHT)
        total_achieved_score = (len(matched_words) * WORD_WEIGHT) + (len(matched_phrases) * PHRASE_WEIGHT)

        total_items = len(job_keywords) + len(job_phrases)
        total_matched = len(matched_words) + len(matched_phrases)

        if total_possible_score == 0:
            return 0, set(), set()

        score = (total_achieved_score / total_possible_score) * 100

        all_matched = matched_words.union(matched_phrases)
        all_missing = missing_words.union(missing_phrases)
        return round(score, 2), all_matched, all_missing


    def generate_suggestions(self, missing_items):
        suggestions = []

        for skill in missing_items:
            suggestion = f"Consider adding experience or a project demonstrating '{skill}'."
            suggestions.append(suggestion)

        return suggestions

    def _get_client(self):
        client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))
        return client

    
    def improve_bullet_point(self, bullet_text):
        client = self._get_client()
        prompt = f"""Rewrite the following resume bullet point to be more impactful.
        Focus on measureable results, action verbs, and clarity.

        Bullet: {bullet_text}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional resume coach."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    
    def analyze_resume_with_ai(self):
        client = self._get_client()
        
        prompt = f"""
        You are a professional technical recruiter.

        Analyze the following resume against the given job description.

        Respond strictly in this format:

        OVERALL ACCESSMENT:
        (Short Paragraph)
        
        STRENGTHS:
        - Bullet points

        WEAKNESS:
        - Bullet points

        IMPROVEMENT SUGGESTIONS:
        - BUllet points

        RESUME:
        {self.resume_text}

        Job Description:: 
        {self.job_text}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer"},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()


    def print_summary(self):
        score, matched, missing = self.calculate_basic_match()

        print("=====RESUME ANALYSIS=====")        
        print(f"Match Score: {score}% \n")
        print("Matched Skills:")
        print(",".join(sorted(matched)))
        print("\nMissing Skills:")
        print(",".join(sorted(missing)))

        print("\n Action Suggestions.")
        suggestions = self.generate_suggestions(missing)
        for s in suggestions:
            print("-", s)
    
def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text

if __name__=="__main__":
    analyzer = ResumeAnalyzer("resume.txt", "job.txt")
    analyzer.load_files()

    while True:
        print("\n===== AI RESUME TOOL =====")
        print("1. Analyze Resume.")
        print("2. Analyze Bullet Point.")
        print("3. Exit")
        
        choice = input("Select option:")

        if choice == "1":
            analyzer.print_summary()
        
        elif choice == "2":
            bullet = input("\n Enter a resume bullet to improve.\n")
            improved = analyzer.improve_bullet_point(bullet)
            print("Improved Version:")
            print(improved)

        elif choice == "3":
            print("Good Bye!")
            break
        
        else:
            print("Invalid choice.")

