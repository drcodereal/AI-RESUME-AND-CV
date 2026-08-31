import os, re
from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash, send_file, abort, session
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import Resume, Analysis, User
from .analyzer import analyze_resume, improve_resume
from .extractors import extract_text
from .exports import resume_pdf, resume_docx

main=Blueprint("main",__name__); ALLOWED={"pdf","docx"}
FIELDS=["name","email","phone","role","summary","education","skills","experience","projects","certifications"]
EMAIL_RE = re.compile(r"^\S+@\S+\.\S+$")

def make_text(data):
    return f'''{data.get("name","")}\n{data.get("email","")} | {data.get("phone","")}\n\n{data.get("role","")}\n\nSUMMARY\n{data.get("summary","")}\n\nEDUCATION\n{data.get("education","")}\n\nSKILLS\n{data.get("skills","")}\n\nEXPERIENCE\n{data.get("experience","")}\n\nPROJECTS\n{data.get("projects","")}\n\nCERTIFICATIONS\n{data.get("certifications","")}'''

def safe_next(path):
    """Only ever redirect to an internal path - never off-site, never back to login/register."""
    if not path or not path.startswith("/") or path.startswith("//"):
        return None
    if path.startswith("/login") or path.startswith("/register"):
        return None
    return path

@main.route("/")
def index():
    if current_user.is_authenticated:
        resumes=Resume.query.filter_by(user_id=current_user.id).order_by(Resume.created_at.desc()).limit(5).all()
        analyses=Analysis.query.filter_by(user_id=current_user.id).order_by(Analysis.created_at.desc()).limit(5).all()
    else:
        resumes, analyses = [], []
    return render_template("index.html", resumes=resumes, analyses=analyses)

@main.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    next_path = safe_next(request.values.get("next"))
    error=None
    if request.method=="POST":
        email=request.form.get("email","").strip().lower()
        password=request.form.get("password","")
        user=User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True, duration=current_app.config["REMEMBER_COOKIE_DURATION"])
            session.permanent = True
            return redirect(next_path or url_for("main.index"))
        error="Incorrect email or password."
    return render_template("login.html", error=error, next=next_path, just_registered=request.args.get("registered"))

@main.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    next_path = safe_next(request.values.get("next"))
    error=None
    if request.method=="POST":
        name=request.form.get("name","").strip()
        email=request.form.get("email","").strip().lower()
        password=request.form.get("password","")
        confirm=request.form.get("confirm","")
        if not name or not email or not password or not confirm:
            error="Please fill in every field."
        elif not EMAIL_RE.match(email):
            error="Enter a valid email address."
        elif len(password) < 6:
            error="Password must be at least 6 characters."
        elif password != confirm:
            error="Passwords do not match."
        elif User.query.filter_by(email=email).first():
            error="An account with this email already exists."
        else:
            user=User(name=name, email=email)
            user.set_password(password)
            db.session.add(user); db.session.commit()
            login_user(user, remember=True, duration=current_app.config["REMEMBER_COOKIE_DURATION"])
            session.permanent = True
            return redirect(next_path or url_for("main.index"))
    return render_template("register.html", error=error, next=next_path)

@main.route("/logout", methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@main.route("/privacy")
def privacy(): return render_template("privacy.html")

@main.route("/terms")
def terms(): return render_template("terms.html")

@main.route("/generate",methods=["GET","POST"])
@login_required
def generate():
    if request.method=="POST":
        data={k:request.form.get(k,"").strip() for k in FIELDS}; template=request.form.get("template","classic")
        if not data["name"]: flash("Name is required."); return redirect(url_for("main.generate"))
        generated=make_text(data); resume=Resume(**data,template=template,generated_text=generated,user_id=current_user.id); db.session.add(resume); db.session.commit(); return redirect(url_for("main.preview",resume_id=resume.id))
    return render_template("generate.html")

@main.route("/resume/<int:resume_id>")
@login_required
def preview(resume_id):
    resume=Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id: abort(404)
    return render_template("preview.html",resume=resume)

@main.route("/analyze",methods=["GET","POST"])
@login_required
def analyze():
    if request.method=="POST":
        file=request.files.get("resume"); jd=request.form.get("job_description","").strip()
        if not file or not file.filename: flash("Please select a PDF or DOCX resume."); return redirect(url_for("main.analyze"))
        ext=file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else ''
        if ext not in ALLOWED: flash("Only PDF and DOCX files are supported."); return redirect(url_for("main.analyze"))
        filename=secure_filename(file.filename); path=os.path.join(current_app.config["UPLOAD_FOLDER"],filename); os.makedirs(current_app.config["UPLOAD_FOLDER"],exist_ok=True); file.save(path)
        text=extract_text(path); result=analyze_resume(text,jd); analysis=Analysis(user_id=current_user.id,filename=filename,score=result["score"],ats_score=result["ats_score"],job_match_score=(result["job_match"] or {}).get("match_score",0),extracted_text=text,strengths="\n".join(result["strengths"]),weaknesses="\n".join(result["weaknesses"]),suggestions="\n".join(result["suggestions"]),matched_keywords=", ".join((result["job_match"] or {}).get("matched",[])),missing_keywords=", ".join((result["job_match"] or {}).get("missing",[]))); db.session.add(analysis); db.session.commit(); return redirect(url_for("main.analysis_result",analysis_id=analysis.id))
    return render_template("analyze.html")

@main.route("/analysis/<int:analysis_id>")
@login_required
def analysis_result(analysis_id):
    analysis=Analysis.query.get_or_404(analysis_id)
    if analysis.user_id != current_user.id: abort(404)
    return render_template("analysis.html",analysis=analysis)

@main.route("/analyze-generated/<int:resume_id>")
@login_required
def analyze_generated(resume_id):
    resume=Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id: abort(404)
    result=analyze_resume(resume.generated_text or ""); analysis=Analysis(user_id=current_user.id,resume_id=resume.id,filename=f"generated_resume_{resume.id}",score=result["score"],ats_score=result["ats_score"],extracted_text=resume.generated_text,strengths="\n".join(result["strengths"]),weaknesses="\n".join(result["weaknesses"]),suggestions="\n".join(result["suggestions"])); db.session.add(analysis); db.session.commit(); return redirect(url_for("main.analysis_result",analysis_id=analysis.id))

@main.route("/improve/<int:resume_id>",methods=["POST"])
@login_required
def improve(resume_id):
    resume=Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id: abort(404)
    result=analyze_resume(resume.generated_text or "",request.form.get("job_description","")); data={k:getattr(resume,k) or "" for k in FIELDS}; data=improve_resume(data,result,request.form.get("job_description",""));
    for k in FIELDS: setattr(resume,k,data[k])
    resume.generated_text=make_text(data); db.session.commit(); flash("Resume improved using the analyzer feedback."); return redirect(url_for("main.preview",resume_id=resume.id))

@main.route("/resume/<int:resume_id>/download/<fmt>")
@login_required
def download_resume(resume_id,fmt):
    resume=Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id: abort(404)
    if fmt=="pdf": return send_file(resume_pdf(resume),as_attachment=True,download_name=f"resume_{resume.id}.pdf",mimetype="application/pdf")
    if fmt=="docx": return send_file(resume_docx(resume),as_attachment=True,download_name=f"resume_{resume.id}.docx",mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    flash("Unsupported format."); return redirect(url_for("main.preview",resume_id=resume.id))

@main.route("/history")
@login_required
def history():
    resumes=Resume.query.filter_by(user_id=current_user.id).order_by(Resume.created_at.desc()).all()
    analyses=Analysis.query.filter_by(user_id=current_user.id).order_by(Analysis.created_at.desc()).all()
    return render_template("history.html",resumes=resumes,analyses=analyses)
