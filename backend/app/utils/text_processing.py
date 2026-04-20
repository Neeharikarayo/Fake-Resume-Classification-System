import re

COMMON_SKILLS = [
    "python", "java", "javascript", "c++", "c#", "ruby", "php", "sql", "nosql",
    "html", "css", "react", "angular", "vue", "node", "django", "flask",
    "spring", "machine learning", "deep learning", "nlp", "computer vision",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "ci/cd", "jenkins",
    "agile", "scrum", "project management", "leadership", "communication",
    "linux", "bash", "powershell", "excel", "powerbi", "tableau", "cfa", "cpa",
    "marketing", "sales", "seo", "sem", "content creation", "design", "ui/ux",
    "photoshop", "illustrator", "figma", "sketch", "invision", "autocad",
    "solidworks", "matlab", "r", "sas", "spss", "stata", "econometrics",
    "financial modeling", "accounting", "audit", "tax", "legal", "hr",
    "recruiting", "training", "customer service", "operations", "logistics",
    "supply chain", "manufacturing", "nursing", "patient care", "emr", "epic",
    "cerner", "meditech", "allscripts", "cpr", "bls", "acls", "pals", "nrp",
    "teaching", "curriculum development", "lesson planning", "classroom management",
    "special education", "esl", "bilingual", "translation", "interpretation",
    "tensorflow", "keras", "pytorch", "scikit-learn", "pandas", "numpy",
    "matplotlib", "seaborn", "hadoop", "spark", "kafka", "elasticsearch"
]

def clean_text(text: str) -> str:
    """Clean resume text identifying patterns."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skill_count(text: str) -> int:
    text_lower = text.lower()
    count = 0
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            count += 1
    return count

def extract_word_count(text: str) -> int:
    return len(text.split())

def extract_experience_years(text: str) -> int:
    text_lower = text.lower()
    patterns = [
        r'(\d+)\+?\s*(?:-\s*\d+\s*)?years?(?:\s+of)?\s+experience',
        r'(\d+)\+?\s*(?:-\s*\d+\s*)?yrs?(?:\s+of)?\s+exp',
        r'experience.*?:.*?(?:over\s+)?(\d+)\s+years?',
        r'(?:over\s+)?(\d+)\s+years', # broad catch
        r'(\d+)\s+yrs'
    ]
    max_years = 0
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            try:
                years = int(match)
                if years > max_years and years < 50:
                    max_years = years
            except ValueError:
                pass
    return max_years
