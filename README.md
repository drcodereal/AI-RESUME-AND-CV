# 🤖 AI Resume Generator & Analyzer — v2

> Build your resume. Analyze it. Improve it. Get ready for the job.

Finding a job is already difficult. Your resume shouldn't make it harder.

I built **AI Resume Generator & Analyzer** as a practical tool to help people create better resumes, understand what's wrong with them, and improve them before applying for jobs.

Instead of only generating a resume, the application lets you **create, preview, analyze, compare, improve, and export** your resume from one place.

The current version focuses mainly on the **core resume generation and analysis features**. Authentication and user accounts are planned for a later phase.

---

## ✨ What Can It Do?

### 📝 Create a Resume

You can build a resume by entering your:

* Personal information
* Education
* Skills
* Work experience
* Projects
* Certifications
* Other relevant details

The application takes this information and turns it into a structured, professional-looking resume.

### 👀 Preview Before Exporting

You don't have to download your resume blindly.

The preview feature lets you check the generated resume first, so you can catch missing information, formatting issues, or mistakes before exporting it.

### 📊 Analyze Your Resume

The analyzer looks at different parts of your resume and gives you useful feedback, including:

* Overall resume score
* ATS score
* Resume structure
* Keywords
* Strengths
* Weaknesses
* Improvement suggestions

The idea is to give you more than just a number.

You should be able to understand **why your resume got that score and what you can do to improve it.**

### 📂 Analyze an Existing Resume

Already have a resume?

You can upload an existing:

* PDF
* DOCX

The application extracts the text from the file and analyzes it, so you don't have to recreate your resume from scratch.

### 🎯 Match Your Resume With a Job Description

A good resume isn't necessarily the same for every job.

You can provide a Job Description and compare it with your resume to find:

* Matching keywords
* Missing keywords
* Relevant skills
* Areas that may need improvement

This can help you customize your resume for different job applications.

### 💡 Improve Your Resume

After analyzing your resume, the application provides suggestions based on the issues it finds.

The basic idea is simple:

**Analyze → Understand → Improve → Analyze Again**

You can keep improving your resume instead of stopping after the first analysis.

### 📄 Export Your Resume

Once you're happy with your resume, you can export it as:

* PDF
* DOCX

So the final document is ready to use for actual job applications.

### 🗂️ Resume & Analysis History

The application keeps track of resume and analysis-related data, making it easier to access previous work instead of starting over every time.

### 💾 SQLite Database

The project currently uses **SQLite** for storing application data.

I chose SQLite because it keeps the project simple and lightweight. There's no need to configure a separate database server just to run the application locally.

---

## 🔄 How It Works

The main workflow looks like this:

```text
Create Resume
      ↓
Preview Resume
      ↓
Analyze Resume
      ↓
Get Overall & ATS Score
      ↓
Review Strengths & Weaknesses
      ↓
Match With Job Description
      ↓
Find Missing Keywords
      ↓
Improve Resume
      ↓
Export PDF / DOCX
```

You can also skip the creation step and start directly by uploading an existing **PDF or DOCX resume**.

---

## 🧠 How Does the Analyzer Work?

One important thing about the current version:

**It doesn't depend on an external AI API.**

The analysis is currently handled locally using a Python-based **rule and keyword engine**.

It looks at things such as:

* Resume sections
* Keywords
* Skills
* Action verbs
* Job-description keywords
* Resume length
* Content structure
* Other resume-quality signals

These signals are combined to produce the scores and feedback shown to the user.

This approach makes the current version:

* Lightweight
* Easy to run locally
* Free from API-key requirements
* Easy to test
* Easy to modify

I plan to explore proper **LLM/AI integration** in future versions for things like smarter rewriting, contextual suggestions, and more advanced resume generation.

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy

### Frontend

* HTML
* CSS
* JavaScript

### Database

* SQLite

### Document Processing

* PyMuPDF
* python-docx

### Document Generation

* ReportLab
* python-docx

---

## 📁 Project Structure

The project is divided into different parts so that the backend logic, frontend, resume processing, and database functionality aren't all mixed together.

```text
AI-Resume/
│
├── app/
│   ├── routes/
│   ├── models/
│   ├── services/
│   ├── templates/
│   └── static/
│
├── uploads/
├── requirements.txt
├── run.py
└── README.md
```

> The structure shown above represents the intended organization of the application. The actual repository may contain additional files and modules as development continues.

---

## 🚀 Run It Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <project-folder>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate it

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the application

```bash
python run.py
```

### 6. Open it in your browser

```text
http://127.0.0.1:5000
```

---

## 📌 Current Status

### Version 2 — Core Resume System

The main goal of v2 is to get the core resume workflow working properly before adding more advanced features.

### ✅ Implemented

* [x] Resume generation
* [x] Resume preview
* [x] Resume analysis
* [x] PDF/DOCX upload
* [x] Text extraction
* [x] Overall resume scoring
* [x] ATS scoring
* [x] Strengths & weaknesses
* [x] Improvement suggestions
* [x] Job Description keyword matching
* [x] Resume improvement workflow
* [x] PDF export
* [x] DOCX export
* [x] Resume/analysis history
* [x] SQLite database

### 🔜 Planned

* [ ] Login / Register
* [ ] User accounts
* [ ] Secure user-specific resume history
* [ ] Advanced AI/LLM integration
* [ ] More resume templates
* [ ] Better resume rewriting
* [ ] More advanced ATS analysis

---

## 🔮 What's Next?

The bigger idea behind this project is to eventually turn it into a more complete **AI-powered career assistant**.

Some features I'm considering for future versions include:

* AI-powered resume rewriting
* Job-specific resume generation
* Cover letter generation
* LinkedIn profile optimization
* Interview preparation
* Skill-gap analysis
* Job application tracking
* More professional resume templates
* Personalized career suggestions

These are part of the roadmap and **aren't being presented as features of the current version**.

---

## 🎯 Why I Built This

I wanted to build something more useful than another basic CRUD project.

This project gave me a chance to work with several areas together:

**Web development + Python + databases + document processing + resume analysis + AI-oriented features.**

A resume is also something people actually need. That made it an interesting problem to work on because there are plenty of things that can be improved beyond simply generating a document.

I'm also treating this project as an ongoing learning experience. With each version, I'm trying to improve the code, UI, analysis logic, and overall user experience.

---

## ⚠️ Current Limitations

There are a few things to keep in mind with the current version.

The analyzer is based mainly on **rules and keyword matching**, so it doesn't understand resume content like a modern large language model would.

Because of that, the scores and suggestions should be treated as **helpful guidance, not a guaranteed ATS prediction**.

Authentication and proper user accounts are also not part of v2 yet. They're intentionally planned for a later development phase.

---

## 📜 License

This project was created for **learning, experimentation, and development purposes**.

---

## 👨‍💻 Developer

Built with Python, Flask, JavaScript, and a lot of experimenting.

### AI Resume Generator & Analyzer — v2

> **Build it. Analyze it. Improve it. Get ready for the job.**
