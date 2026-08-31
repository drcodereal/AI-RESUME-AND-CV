import re
from collections import Counter

COMMON_KEYWORDS = [
    "python", "java", "javascript", "typescript", "react", "node.js", "node", "sql", "git", "docker",
    "machine learning", "data analysis", "communication", "leadership", "teamwork", "project management",
    "html", "css", "flask", "django", "aws", "azure", "power bi", "excel", "pandas", "numpy",
    "tensorflow", "pytorch", "rest api", "mongodb", "postgresql", "mysql", "linux", "figma"
]
ACTION_WORDS = ["developed", "built", "designed", "implemented", "managed", "created", "improved", "led", "optimized", "automated"]


def _sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text or "") if s.strip()]


def analyze_resume(text: str, job_description: str = ""):
    clean = re.sub(r"\s+", " ", text or "").strip()
    lower = clean.lower()
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.-]*\b", lower)
    count = len(words)
    sections = {
        "summary": bool(re.search(r"summary|objective|profile", lower)),
        "education": "education" in lower,
        "skills": "skills" in lower,
        "experience": bool(re.search(r"experience|employment|work history", lower)),
        "projects": "projects" in lower,
        "certifications": bool(re.search(r"certifications?|licenses?", lower)),
    }
    section_score = round(sum(sections.values()) / len(sections) * 100)
    keyword_hits = [k for k in COMMON_KEYWORDS if k in lower]
    keyword_score = min(100, len(keyword_hits) * 6)
    action_hits = [w for w in ACTION_WORDS if re.search(rf"\b{re.escape(w)}\b", lower)]
    action_score = min(100, len(action_hits) * 10)
    quant = len(re.findall(r"\b\d+(?:%|\+|k|m)?\b", lower))
    quant_score = min(100, quant * 15)
    length_score = 100 if 350 <= count <= 900 else 80 if 200 <= count <= 1100 else 55 if count >= 120 else 35
    ats_score = round(section_score*.35 + keyword_score*.25 + action_score*.15 + quant_score*.10 + length_score*.15)
    overall = round(ats_score*.70 + min(100, count/7)*.30)

    strengths=[]; weaknesses=[]; suggestions=[]
    if sections["skills"]: strengths.append("Skills section is present and can be parsed by ATS systems.")
    else: weaknesses.append("Skills section is missing."); suggestions.append("Add a focused technical and soft-skills section.")
    if sections["experience"]: strengths.append("Experience section is present.")
    else: weaknesses.append("Work experience section is missing."); suggestions.append("Add internships, freelance work, or practical experience where applicable.")
    if sections["projects"]: strengths.append("Projects section is present.")
    else: weaknesses.append("Projects section is missing."); suggestions.append("Add 2–4 relevant projects with technologies and measurable outcomes.")
    if action_hits: strengths.append("Action-oriented language detected: " + ", ".join(action_hits[:6]) + ".")
    else: weaknesses.append("Few strong action verbs were detected."); suggestions.append("Start achievement bullets with verbs such as Developed, Built, Implemented, Optimized, or Led.")
    if quant: strengths.append(f"Quantified evidence detected ({quant} numeric references).")
    else: weaknesses.append("Few measurable achievements were detected."); suggestions.append("Quantify impact with percentages, counts, time saved, revenue, users, or performance improvements.")
    if len(keyword_hits) >= 5: strengths.append("A healthy set of common professional/technical keywords is present.")
    else: weaknesses.append("Keyword coverage is limited."); suggestions.append("Add skills and keywords that genuinely match the target role.")
    if count < 200: suggestions.append("The resume is short; add stronger evidence, project details, and achievements.")
    if count > 1100: suggestions.append("The resume may be too long; remove repetitive or low-value content.")

    job_result = None
    if job_description.strip():
        job_lower=job_description.lower()
        job_terms=[]
        for k in COMMON_KEYWORDS:
            if k in job_lower: job_terms.append(k)
        # Also capture useful multi-letter words from the JD, excluding generic stop words.
        stop={"and","the","with","for","from","that","this","will","your","you","our","are","have","has","into","about","role","work","using","years","year","job","team"}
        tokens=[w for w in re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",job_lower) if w not in stop]
        freq=Counter(tokens)
        extra=[w for w,c in freq.most_common(35) if c>=1 and w not in job_terms]
        job_terms=(job_terms+extra)[:40]
        matched=[t for t in job_terms if t in lower]
        missing=[t for t in job_terms if t not in lower]
        match_score=round(len(matched)/len(job_terms)*100) if job_terms else 0
        job_result={"match_score":match_score,"matched":matched[:20],"missing":missing[:20],"keywords":job_terms}
        if match_score < 60: suggestions.append("Tailor this resume to the supplied job description by naturally adding missing, relevant keywords.")
        else: strengths.append(f"Job-description keyword match is {match_score}%.")

    return {"score":max(0,min(100,int(overall))),"ats_score":max(0,min(100,int(ats_score))),
            "strengths":strengths or ["Resume text was successfully extracted and analyzed."],
            "weaknesses":weaknesses or ["No major structural weakness detected by the current rules."],
            "suggestions":suggestions or ["Tailor the resume for each target job and quantify achievements."],
            "job_match":job_result, "word_count":count, "sections":sections, "keyword_hits":keyword_hits}


def improve_resume(data, analysis, job_description=""):
    summary=data.get("summary","").strip()
    if not summary:
        summary=f"Motivated {data.get('role','professional')} with hands-on experience in {data.get('skills','relevant technologies')}."
    summary=summary.rstrip('.') + "."
    if job_description and analysis.get("job_match"):
        missing=analysis["job_match"]["missing"][:6]
        if missing: summary += " Targeted strengths include " + ", ".join(missing) + "."
    return {**data, "summary":summary}
