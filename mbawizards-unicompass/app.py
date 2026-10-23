from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os
import json
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Determine base and frontend directories
base_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.abspath(os.path.join(base_dir, "..", "frontend"))
if not os.path.exists(frontend_dir):
    frontend_dir = os.path.abspath(os.path.join(base_dir, "frontend"))
if not os.path.exists(frontend_dir):
    frontend_dir = base_dir

static_path = os.path.join(frontend_dir, "static")
app = Flask(__name__, static_folder=static_path if os.path.exists(static_path) else None, template_folder=frontend_dir)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
supabase: Client = None

if supabase_url and supabase_key and "your_supabase" not in supabase_url:
    try:
        supabase = create_client(supabase_url, supabase_key)
        print("MBAWizards UniCompass: Supabase connected successfully!")
    except Exception as e:
        print("Failed to initialize Supabase client:", e)

# In-memory store fallback
student_profiles = {}


def send_lead_email_async(data: dict):
    """Send new lead notification email to admin via SMTP."""
    try:
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 465))
        smtp_user = os.getenv("SMTP_USER", "rupali.eduquest@gmail.com")
        smtp_pass = os.getenv("SMTP_PASS") or os.getenv("SMTP_PASSWORD")
        admin_email = os.getenv("ADMIN_EMAIL", "rupali.eduquest@gmail.com")

        if not smtp_user or not smtp_pass:
            print("SMTP credentials missing, skipping lead email.")
            return

        subject = "mba- carer cluster"

        full_name = data.get("fullName", "N/A")
        email = data.get("email", "N/A")
        phone = data.get("phone", "N/A")
        city = data.get("city", "N/A")
        country = data.get("country", "N/A")
        nationality = data.get("nationality", "N/A")
        edu_stage = data.get("educationLevel", "N/A")
        fos = data.get("fieldOfStudy", "N/A")
        tier = data.get("collegeTier", "N/A")
        cgpa = data.get("cgpa", "N/A")
        grad_year = data.get("graduationYear", "N/A")
        work_exp = data.get("workExperience", "N/A")
        current_role = data.get("currentRole", "N/A")
        current_ind = data.get("currentIndustry", "N/A")
        key_skills = data.get("keySkills", "N/A")
        target_role = data.get("targetRole", "N/A")
        degree_pref = data.get("degreePreference", "N/A")
        exam_guidance = data.get("examGuidance", "N/A")
        gmat = data.get("gmatScore", "N/A")
        cat = data.get("catScore", "N/A")
        gre = data.get("greScore", "N/A")
        ielts = data.get("ieltsScore", "N/A")
        target_country = data.get("targetCountry", "N/A")
        dream_univ = data.get("dreamUniversity", "N/A")
        funding = data.get("fundingNeed", "N/A")
        notes = data.get("notes", "N/A")
        submitted_at = data.get("submitted_at", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))

        # HTML Email Template
        html_content = f"""
        <html>
        <head>
          <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 20px; }}
            .container {{ width: 100%; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.06); }}
            .header {{ background: linear-gradient(135deg, #090d16 0%, #1e293b 100%); color: #d4af37; padding: 24px 28px; border-bottom: 3px solid #d4af37; }}
            .header h2 {{ margin: 0 0 6px; font-size: 22px; color: #ffffff; letter-spacing: 0.5px; }}
            .header p {{ margin: 0; font-size: 13px; color: #cbd5e1; }}
            .content {{ padding: 28px; }}
            .lead-pill {{ display: inline-block; background: #fef3c7; color: #92400e; font-weight: 700; font-size: 11px; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; margin-bottom: 18px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }}
            th, td {{ padding: 12px 14px; text-align: left; border-bottom: 1px solid #f1f5f9; }}
            th {{ background: #f8fafc; color: #64748b; font-weight: 600; width: 35%; text-transform: uppercase; font-size: 12px; }}
            td {{ color: #0f172a; font-weight: 500; }}
            .highlight {{ color: #b45309; font-weight: 700; }}
            .footer {{ background: #f8fafc; padding: 16px 28px; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h2>MBAWizards UniCompass · New Lead Notification</h2>
              <p>Subject Tag: <strong>{subject}</strong></p>
            </div>
            <div class="content">
              <span class="lead-pill">✦ Verified High-Intent Candidate Lead</span>
              <table>
                <tr><th>Full Name (Required)</th><td class="highlight">{full_name}</td></tr>
                <tr><th>Phone / WhatsApp (Required)</th><td class="highlight"><a href="tel:{phone}" style="color:#b45309; text-decoration:none;">{phone}</a></td></tr>
                <tr><th>Email Address (Required)</th><td class="highlight"><a href="mailto:{email}" style="color:#b45309; text-decoration:none;">{email}</a></td></tr>
                <tr><th>City (Required)</th><td class="highlight">{city}</td></tr>
                <tr><th>Country & Nationality</th><td>{country} · {nationality}</td></tr>
                <tr><th>Education Level</th><td>{edu_stage} ({tier})</td></tr>
                <tr><th>Undergrad Major & CGPA</th><td>{fos} — CGPA: {cgpa} (Grad: {grad_year})</td></tr>
                <tr><th>Work Experience</th><td><strong>{work_exp}</strong> as <em>{current_role}</em> ({current_ind})</td></tr>
                <tr><th>Key Skills</th><td>{key_skills}</td></tr>
                <tr><th>Target Functional Role</th><td>{target_role}</td></tr>
                <tr><th>Target Degree Track</th><td><strong>{degree_pref}</strong></td></tr>
                <tr><th>Exam Strategy Preference</th><td>{exam_guidance}</td></tr>
                <tr><th>Exam Scores (if taken)</th><td>GMAT: {gmat} | CAT: {cat} | GRE: {gre} | IELTS/TOEFL: {ielts}</td></tr>
                <tr><th>Target Geography</th><td>{target_country}</td></tr>
                <tr><th>Dream B-Schools</th><td><strong>{dream_univ}</strong></td></tr>
                <tr><th>Scholarship Need</th><td>{funding}</td></tr>
                <tr><th>Candidate Notes / Challenges</th><td>{notes}</td></tr>
                <tr><th>Timestamp</th><td>{submitted_at}</td></tr>
              </table>
            </div>
            <div class="footer">
              This automated lead was generated from MBAWizards UniCompass Platform for admin: {admin_email}
            </div>
          </div>
        </body>
        </html>
        """

        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"MBAWizards Leads <{smtp_user}>"
        msg["To"] = admin_email

        msg.attach(MIMEText(html_content, "html"))

        # Send via SMTP_SSL
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=12) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [admin_email], msg.as_string())
            print(f"SMTP: Successfully sent lead email to {admin_email} with subject '{subject}'")

    except Exception as e:
        print("SMTP Error while sending lead email:", e)


@app.route("/")
def home():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(frontend_dir, "index.html")
    templates_index = os.path.join(base_dir, "templates", "index.html")
    if os.path.exists(templates_index):
        return render_template("index.html")
    return jsonify({"status": "ok", "service": "MBAWizards UniCompass API", "version": "1.0"})


@app.route("/api/health")
def health_check():
    return jsonify({"status": "ok", "service": "MBAWizards UniCompass API"})


@app.route("/submit-profile", methods=["POST", "OPTIONS"])
def submit_profile():
    """Receive, store intake form data to Supabase & leads.jsonl, and send admin email via SMTP."""
    data = request.get_json(silent=True) or {}

    # Timestamp and store
    data["submitted_at"] = datetime.utcnow().isoformat()
    email = data.get("email", "").strip().lower()

    if email:
        student_profiles[email] = data

        # Supabase Integration: Save to career_students_data
        if supabase:
            try:
                student_data = {
                    "full_name": data.get("fullName", "").strip(),
                    "email": email,
                    "phone": data.get("phone", "").strip() or None,
                    "city": data.get("city", "").strip() or None,
                    "country": data.get("country", "").strip() or None,
                    "nationality": data.get("nationality", "").strip() or None,
                    "education_level": data.get("educationLevel", "").strip() or None,
                    "field_of_study": data.get("fieldOfStudy", "").strip() or None,
                    "target_university": data.get("dreamUniversity", "").strip() or None,
                    "target_country": data.get("targetCountry", "").strip() or None,
                    "target_field": data.get("degreePreference", "").strip() or data.get("targetRole", "").strip() or None,
                    "career_interest": data.get("careerInterest", "").strip() or data.get("targetIndustry", "").strip() or None,
                    "raw_form_data": data
                }

                # Upsert into career_students_data
                supabase.table("career_students_data").upsert(
                    student_data,
                    on_conflict="email"
                ).execute()
                print(f"Supabase: Saved candidate profile for {email}")
            except Exception as e:
                print("Supabase profile save error:", e)

    # Optional local JSONL backup
    try:
        with open("leads.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
    except Exception as e:
        print("Lead log error:", e)

    # Send lead notification to admin email via SMTP asynchronously
    threading.Thread(target=send_lead_email_async, args=(data,), daemon=True).start()

    return jsonify({"status": "ok"})


def build_profile_context(profile: dict) -> str:
    """Transform candidate intake profile into an executive briefing block for the AI."""
    if not profile:
        return ""

    lines = ["CANDIDATE INTELLIGENCE BRIEFING:"]

    def add(label, key):
        val = profile.get(key, "")
        if isinstance(val, str):
            val = val.strip()
        else:
            val = str(val).strip()
        if val and val not in ("0", ""):
            lines.append(f"  • {label}: {val}")

    add("Full Name", "fullName")
    add("Age", "age")
    add("Email", "email")
    add("Phone / WhatsApp", "phone")
    add("Current Location", "city")
    add("Country of Residence", "country")
    add("Nationality", "nationality")

    # Pillar 1: Education
    add("Education Stage", "educationLevel")
    add("Undergraduate Degree & Major", "fieldOfStudy")
    add("Undergrad College / University Tier", "collegeTier")
    add("CGPA / Percentage", "cgpa")
    add("Graduation Year", "graduationYear")
    add("Academic Honors / Publications", "academicHonors")

    # Pillar 1: Experience & Skills
    add("Full-Time Work Experience", "workExperience")
    add("Current Job Title & Organization", "currentRole")
    add("Current Industry Sector", "currentIndustry")
    add("Key Technical & Business Skills", "keySkills")
    add("Leadership / Extracurricular Spike", "leadershipExp")

    # Pillar 1 & 2: Interests, Course & Degree Guidance
    add("Target Post-Grad Functional Role", "targetRole")
    add("Target Industry / Domain", "careerInterest")
    add("Degree / Program Stated Preference", "degreePreference")
    add("Course Recommendation Need", "courseGuidance")
    add("Exam Strategy Guidance Need", "examGuidance")

    # Test Scores (GMAT, CAT, GRE, EA, IELTS, TOEFL)
    scores = []
    for label, key in [
        ("GMAT / GMAT Focus", "gmatScore"),
        ("CAT (Percentile)", "catScore"),
        ("GRE", "greScore"),
        ("Executive Assessment (EA)", "eaScore"),
        ("IELTS", "ieltsScore"),
        ("TOEFL", "toeflScore"),
        ("Duolingo / PTE", "pteScore")
    ]:
        v = str(profile.get(key, "")).strip()
        if v:
            scores.append(f"{label}: {v}")
    if scores:
        lines.append("  • Candidate Standardized Scores (if taken): " + ", ".join(scores))

    # Pillar 3 & 4: Goals & Matching
    add("Target Countries / Regions", "targetCountry")
    add("Dream Business Schools / Programs", "dreamUniversity")
    add("Scholarship / Funding Need", "fundingNeed")
    add("Target Intake", "targetIntake")
    add("Positioning Challenges / Notes", "notes")

    return "\n".join(lines) if len(lines) > 1 else ""


@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    data = request.get_json(silent=True) or {}
    user_input = (data.get("query") or "").strip()
    profile = data.get("profile") or {}

    useless = {"hi", "hello", "hey", "how are you", "hii", "yo"}
    if not user_input or user_input.lower() in useless or len(user_input) < 5:
        return jsonify({
            "result": """
            <div class="result-placeholder">
                <h2>Please Enter Your Graduate Goal</h2>
                <p>Try inputs like:<br>
                • Which course and specialization should I pursue based on my profile?<br>
                • GMAT vs CAT vs GRE: Which exam should I take for top business schools?<br>
                • Harvard Business School vs Stanford GSB for Tech Leadership</p>
            </div>
            """
        })

    profile_context = build_profile_context(profile)

    prompt = f"""
You are the Senior Partner & Lead Admissions Strategist at MBAWizards (Official Portal: https://www.mbawizards.co.in/) — an elite global consultancy helping high-performing candidates gain admission to the world's top business schools and specialized graduate master's programs.

Your task is to generate a comprehensive, highly rigorous, and strategic **Graduate Admissions & Career Intelligence Report** in HTML format for the candidate's query:
Candidate Goal/Query: {user_input}

{profile_context}

======================================================================
COMPREHENSIVE INTELLIGENCE MANDATE: 5 CORE PILLARS
======================================================================

You MUST structure the report around these essential pillars:

1. APPLICANT ASSESSMENT:
   - Education: Evaluate GPA, degree pedigree, and quantitative/analytical readiness.
   - Experience: Assess years of work experience, title progression, brand equity of employers, and leadership scope.
   - Skills: Audit technical, analytical, financial, and strategic competencies.
   - Interests: Assess clarity and feasibility of short-term (1-3 yrs) and long-term (5-10 yrs) post-degree goals.
   - Gaps & Vulnerabilities: Unflinchingly identify critical blindspots (e.g., low GPA, limited international exposure, lack of direct team management) and provide immediate tactical mitigations.

2. PRESCRIBED COURSE & SPECIALIZATION RECOMMENDATION (What course should the student take?):
   - You must NOT just take their stated preference for granted. You must actively RECOMMEND the optimal degree and specialization:
     * Full-Time 2-Year MBA vs European 1-Year MBA vs Tech MBA
     * Specialized Master's: Master's in Management (MiM), MS in Business Analytics / Data Science (MSBA), MS in Finance (MSF), or MS Computer Science / Engineering Management
     * Or Deferral / Work Experience extension
   - Explain explicitly:
     * Primary Recommended Course & Specialization
     * Why this course fits their exact academic background, GPA, and skill set
     * Expected post-grad roles and starting compensation packages ($110k-$220k+ / ₹25L-₹50L+)
     * Secondary / Alternative course recommendation

3. EXAM DECISION ENGINE: GMAT vs CAT vs GRE (Which exam should the student take?):
   - Provide an authoritative, personalized diagnostic on standardized tests:
     * **GMAT (Focus Edition)**: Best for Global MBA (US M7, European INSEAD/LBS, Asian NUS/NTU) & Indian Executive/PGP (ISB, IIM 1-Year MBA). Focus: Data Insights, Quant, Verbal. Target: 655-715+.
       -> Recommend MBAWizards GMAT Coaching with direct link: https://www.mbawizards.co.in/gmat-coaching and https://www.mbawizards.co.in/gmat-preparation
     * **CAT (Common Admission Test)**: Best for 2-Year Indian IIMs (Ahmedabad, Bangalore, Calcutta, Lucknow, etc.) & FMS, SPJIMR. Focus: High-speed DILR, Quant, VARC under tight sectional timers. Target: 98.5-99.8%ile.
       -> Recommend MBAWizards CAT Coaching with direct link: https://www.mbawizards.co.in/cat
     * **GRE (General Test)**: Best for Specialized Master's (MSBA, MS Finance, Engineering Management, US Ivy Master's degrees) and dual degrees. Focus: Advanced vocabulary, verbal reasoning, algebra/geometry. Target: 322-332+.
       -> Recommend MBAWizards GRE Coaching with direct link: https://www.mbawizards.co.in/gre-coaching-classes
     * **Dual Track (GMAT + CAT)**: For candidates targeting both Indian IIMs and Global/ISB options.
       -> Recommend: https://www.mbawizards.co.in/gmat-cat-coaching
     * **Executive Assessment (EA)**: For experienced professionals (EMBA / Part-Time / select Full-Time like Columbia/INSEAD/Duke). Target: 154+.
   - Give the student an explicit **Personalized Exam Verdict**: Which exact test they should register for, why it maximizes their admission odds, target cutoffs, and a recommended prep sprint (months & focus areas).

4. UNIVERSITY AND PROGRAMME MATCHING:
   - Present a tiered shortlist tailored to the candidate's profile:
     * 🌟 Dream / Reach (Top 1-5% global selectivity, e.g. M7, INSEAD, LBS, IIM A/B/C)
     * 🎯 Target / Competitive (Strong alignment with candidate metrics, e.g. Kellogg, Booth, Yale, HEC Paris, ISB)
     * 🛡️ Safe / High-Value (High admission probability + strong scholarship likelihood)
   - For each tier, explicitly detail:
     * Eligibility & Test Requirements (GMAT Focus / CAT / GRE cutoffs, work exp thresholds)
     * Estimated Costs (Tuition + living expenses)
     * Scholarships & Fellowships (Merit scholarships, diversity grants, assistantships)
     * Career Outcomes (Median starting package, top hiring industries, employment rate within 3 months, STEM designation & post-study visa rights)

5. PERSONALISED APPLICATION ROADMAP:
   - Profile Positioning & Narrative Moat: How to frame the candidate's unique "Spike" (what makes them memorable among thousands of consultants/engineers/financiers).
   - Essays & SOP Architecture: Strategic hooks, storytelling arcs, addressing school-specific essay criteria.
   - Interviews Preparation: Behavioral interview tactics (STAR method), blind alumni vs admissions board interview dynamics.
   - Application Calendar: Round 1 vs Round 2 strategy, recommendation letter briefing, and submission milestones.
   - Recommend MBAWizards Admissions Consulting Packages: https://www.mbawizards.co.in/premium-university-consulting-packages

======================================================================
BRANDING & RESOURCE LINKS INTEGRATION
======================================================================
- Brand Voice: MBAWizards UniCompass (Official Website: https://www.mbawizards.co.in/).
- You MUST embed the official MBAWizards landing page links inside the HTML buttons/anchors as specified:
  * GMAT Prep: <a href="https://www.mbawizards.co.in/gmat-coaching" target="_blank" class="resource-link-btn">Explore MBAWizards GMAT Focus Coaching ↗</a>
  * CAT Prep: <a href="https://www.mbawizards.co.in/cat" target="_blank" class="resource-link-btn">Explore MBAWizards CAT 99+ %ile Mentorship ↗</a>
  * GRE Prep: <a href="https://www.mbawizards.co.in/gre-coaching-classes" target="_blank" class="resource-link-btn">Explore MBAWizards GRE Coaching Classes ↗</a>
  * GMAT+CAT Track: <a href="https://www.mbawizards.co.in/gmat-cat-coaching" target="_blank" class="resource-link-btn">Explore GMAT + CAT Dual Track ↗</a>
  * Consulting: <a href="https://www.mbawizards.co.in/premium-university-consulting-packages" target="_blank" class="resource-link-btn">MBAWizards Admissions Consulting Packages ↗</a>
  * Book Demo / Advisory: <a href="https://www.mbawizards.co.in/contact-us" target="_blank" class="resource-link-btn">Book 1-on-1 Profile Strategy Session ↗</a>
- Persona: Mix of a McKinsey Senior Partner and an Ivy League Admissions Committee Dean.
- Tone: Prestigious, authoritative, diagnostic, intellectually rigorous, and actionable. Avoid generic motivational fluff.
- Personalization: Address the candidate by name if available, and reference their exact GPA, years of experience, current role, and target goals throughout the document.

======================================================================
STRICT HTML OUTPUT STRUCTURE (Follow exactly):
======================================================================

<div class="roadmap-container">

  <div class="report-header-banner">
    <span class="report-tag">MBAWizards UniCompass · Intelligence Dossier</span>
    <h2>Strategic Admissions Roadmap: {user_input}</h2>
    <p class="report-lead">Diagnostic evaluation, course prescription, GMAT/CAT/GRE exam strategy, university matching, and milestone execution blueprint.</p>
  </div>

  <!-- SECTION 1: APPLICANT PROFILE ASSESSMENT -->
  <div class="report-block" id="block-assessment">
    <h3>1. 📊 Applicant Profile Assessment</h3>
    <div class="assessment-grid">
      <div class="metric-card">
        <strong>Academic & Quantitative Rigor</strong>
        <p>[Assess candidate's GPA, degree rigor, and analytical foundation]</p>
      </div>
      <div class="metric-card">
        <strong>Professional Experience & Leadership</strong>
        <p>[Assess work experience depth, leadership trajectory, and organizational impact]</p>
      </div>
      <div class="metric-card">
        <strong>Skills & Functional Moat</strong>
        <p>[Audit technical, managerial, and domain-specific capabilities]</p>
      </div>
      <div class="metric-card">
        <strong>Post-Grad Career Alignment</strong>
        <p>[Evaluate realism, ambition, and industry demand for their stated goals]</p>
      </div>
    </div>
    <div class="gap-analysis-box">
      <h4>🚨 Critical Profile Gaps & Strategic Mitigations</h4>
      <ul>
        <li><strong>Identified Gap:</strong> [Specific gap] → <strong>MBAWizards Mitigation:</strong> [Exact action to take]</li>
        <li><strong>Identified Gap:</strong> [Specific gap] → <strong>MBAWizards Mitigation:</strong> [Exact action to take]</li>
      </ul>
    </div>
  </div>

  <!-- SECTION 2: PRESCRIBED COURSE & SPECIALIZATION RECOMMENDATION -->
  <div class="report-block" id="block-course-rec">
    <h3>2. 🎯 Prescribed Course & Specialization Recommendation</h3>
    <p class="section-intro">Based on your academic background, quantitative foundation, and career aspirations, here is your high-leverage program prescription:</p>
    
    <div class="course-prescription-card">
      <div class="prescribed-badge">★ Primary Course Recommendation</div>
      <h4>[Recommended Degree & Specialization, e.g. Full-Time MBA in Tech & Operations Management / MS in Business Analytics]</h4>
      <p><strong>Why This Fits Your Profile:</strong> [Explain why this exact course matches their undergraduate background, CGPA, work experience, and career trajectory]</p>
      <div class="course-metrics-row">
        <span>💼 <strong>Target Post-Grad Roles:</strong> [e.g. Senior Product Manager, Strategy Consultant, Quant Analyst]</span>
        <span>💰 <strong>Avg Global Compensation:</strong> [e.g. $165,000 - $210,000 / ₹28L - ₹45L]</span>
        <span>⏱️ <strong>Typical Program Duration:</strong> [e.g. 1 Year / 2 Years]</span>
      </div>
    </div>

    <div class="secondary-course-card">
      <div class="secondary-badge">Alternative / Backup Course Pathway</div>
      <h5>[Alternative Program, e.g. Specialised Master's in Management (MiM) or MS Finance]</h5>
      <p>[Explain under what conditions the candidate should pivot to this alternative program]</p>
    </div>
  </div>

  <!-- SECTION 3: EXAM DECISION ENGINE: GMAT vs CAT vs GRE -->
  <div class="report-block" id="block-exam-strategy">
    <h3>3. 📝 Exam Decision Engine: GMAT vs CAT vs GRE</h3>
    <div class="exam-verdict-banner">
      <span class="verdict-label">MBAWizards Exam Verdict For You:</span>
      <strong>[Primary Recommended Exam: e.g. GMAT Focus Edition / CAT / GRE]</strong>
      <p>[Explain specifically why this exam plays to the candidate's strengths, target geographies, and target schools]</p>
    </div>

    <div class="strategy-comparison-table-wrap">
      <table class="strategy-table">
        <thead>
          <tr>
            <th>Standardized Exam</th>
            <th>Primary Program & Country Fit</th>
            <th>Syllabus & Scoring Focus</th>
            <th>Your Target Benchmark</th>
            <th>MBAWizards Prep Resource</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>GMAT Focus Edition</strong></td>
            <td>Global MBA (US M7, Europe, Singapore) & Indian Executive/ISB</td>
            <td>Data Insights, Problem Solving, Critical Reasoning (No Geometry, No Essay)</td>
            <td><strong>[Target, e.g. 665 - 715+ (93rd-99th %ile)]</strong></td>
            <td><a href="https://www.mbawizards.co.in/gmat-coaching" target="_blank" class="resource-link-btn">GMAT Prep ↗</a></td>
          </tr>
          <tr>
            <td><strong>CAT (IIMs)</strong></td>
            <td>Top Indian B-Schools (IIM A/B/C, FMS, SPJIMR)</td>
            <td>Intense speed math, Data Interpretation & Logical Reasoning (DILR), VARC</td>
            <td><strong>[Target, e.g. 98.5 - 99.8%ile]</strong></td>
            <td><a href="https://www.mbawizards.co.in/cat" target="_blank" class="resource-link-btn">CAT Coaching ↗</a></td>
          </tr>
          <tr>
            <td><strong>GRE (General)</strong></td>
            <td>Specialized Master's (MSBA, MSF), Dual Degrees, Top US/European Universities</td>
            <td>Advanced Vocabulary, Quantitative Reasoning (includes Geometry), Analytical Writing</td>
            <td><strong>[Target, e.g. 324 - 332+]</strong></td>
            <td><a href="https://www.mbawizards.co.in/gre-coaching-classes" target="_blank" class="resource-link-btn">GRE Classes ↗</a></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="exam-timeline-box">
      <h4>⚡ Recommended Exam Sprint & Timeline</h4>
      <p>[Provide a high-yield study plan: months needed, mock test pacing, and scoring strategy]</p>
      <div class="exam-links-cluster" style="margin-top:12px; display:flex; flex-wrap:wrap; gap:10px;">
        <a href="https://www.mbawizards.co.in/gmat-coaching" target="_blank" class="resource-link-btn">🎯 GMAT Focus Coaching at MBAWizards</a>
        <a href="https://www.mbawizards.co.in/cat" target="_blank" class="resource-link-btn">🏆 CAT Mentorship at MBAWizards</a>
        <a href="https://www.mbawizards.co.in/gre-coaching-classes" target="_blank" class="resource-link-btn">📘 GRE Classes at MBAWizards</a>
        <a href="https://www.mbawizards.co.in/gmat-cat-coaching" target="_blank" class="resource-link-btn">⚖️ GMAT + CAT Dual Track</a>
      </div>
    </div>
  </div>

  <!-- SECTION 4: UNIVERSITY AND PROGRAMME MATCHING -->
  <div class="report-block" id="block-matching">
    <h3>4. 🏛️ University & Programme Matching</h3>
    <p class="section-intro">Curated school matching evaluated against eligibility, tuition costs, scholarships, and career placement outcomes.</p>

    <div class="school-tier reach-tier">
      <h4>🌟 Ambitious / Dream Tier (Selective Reach)</h4>
      <div class="school-card">
        <div class="school-name"><strong>[University / Business School Name 1]</strong> — [Program Name]</div>
        <ul class="school-details-list">
          <li><strong>Eligibility & Cutoffs:</strong> [GMAT/CAT/GRE target, avg work exp, GPA cutoffs]</li>
          <li><strong>Costs:</strong> [Tuition fees + estimated living costs in USD / local currency]</li>
          <li><strong>Scholarships:</strong> [Key fellowship, merit grants, and financial aid strategies]</li>
          <li><strong>Career Outcomes:</strong> [Median post-grad package, top recruiters, OPT / work visa policy]</li>
        </ul>
      </div>
    </div>

    <div class="school-tier target-tier">
      <h4>🎯 Target Tier (Competitive Alignment)</h4>
      <div class="school-card">
        <div class="school-name"><strong>[University / Business School Name 2]</strong> — [Program Name]</div>
        <ul class="school-details-list">
          <li><strong>Eligibility & Cutoffs:</strong> [Score range, avg work exp, GPA cutoffs]</li>
          <li><strong>Costs:</strong> [Tuition fees + estimated living costs]</li>
          <li><strong>Scholarships:</strong> [Scholarship potential and competition level]</li>
          <li><strong>Career Outcomes:</strong> [Median salary, employment rate, top hiring domains]</li>
        </ul>
      </div>
    </div>

    <div class="school-tier safe-tier">
      <h4>🛡️ Safe / High-Value Tier (Strong Admit & Funding Odds)</h4>
      <div class="school-card">
        <div class="school-name"><strong>[University / Business School Name 3]</strong> — [Program Name]</div>
        <ul class="school-details-list">
          <li><strong>Eligibility & Cutoffs:</strong> [Score ranges & profile alignment]</li>
          <li><strong>Costs:</strong> [Tuition & living budget]</li>
          <li><strong>Scholarships:</strong> [High scholarship probability / merit awards]</li>
          <li><strong>Career Outcomes:</strong> [Regional and global placement outcomes]</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- SECTION 5: PERSONALISED APPLICATION ROADMAP -->
  <div class="report-block" id="block-roadmap">
    <h3>5. 🚀 Personalised Application Roadmap</h3>

    <div class="roadmap-grid">
      <div class="rm-item">
        <h4>1. Standardized Tests Sprint</h4>
        <p><strong>Primary Exam:</strong> [Recommended exam]</p>
        <p><strong>Preparation Sprint:</strong> [Timeline to achieve target score]</p>
      </div>

      <div class="rm-item">
        <h4>2. Profile Positioning & Narrative Moat</h4>
        <p>[Explain how candidate should position their background to stand out among thousands of applicants]</p>
      </div>

      <div class="rm-item">
        <h4>3. Essays & Statement of Purpose Strategy</h4>
        <p>[Deconstruct essay themes: Personal catalyst, professional achievements, why this specific program now, and vision]</p>
      </div>

      <div class="rm-item">
        <h4>4. Admissions Interview Strategy</h4>
        <p>[Tactics for behavioral (STAR method), video interview rounds, and alumni interaction]</p>
      </div>
    </div>

    <div class="calendar-timeline">
      <h4>📅 Application Execution Milestones (Round 1 & Round 2)</h4>
      <div class="timeline-step">
        <span class="step-time">Months 1-2</span>
        <span class="step-desc">Test prep sprint (GMAT/CAT/GRE), school shortlist finalization, recommender outreach & briefing.</span>
      </div>
      <div class="timeline-step">
        <span class="step-time">Months 3-4</span>
        <span class="step-desc">Resume reconstruction to global MBA format, drafting school-specific essay stories, mock reviews.</span>
      </div>
      <div class="timeline-step">
        <span class="step-time">Month 5</span>
        <span class="step-desc">Application submission, video essay recordings, and mock interview intensives with MBAWizards.</span>
      </div>
    </div>

    <div style="margin-top:20px; text-align:center;">
      <a href="https://www.mbawizards.co.in/premium-university-consulting-packages" target="_blank" class="resource-link-btn" style="padding:12px 24px; font-size:14px;">
        🏛️ Explore MBAWizards M7 &amp; Global B-School Consulting Packages ↗
      </a>
    </div>
  </div>

  <!-- SECTION 6: MBAWIZARDS EXECUTIVE ADVISORY CTA -->
  <div class="report-advisory-cta">
    <div class="cta-inner">
      <span class="cta-badge">MBAWizards Executive Advisory</span>
      <h3>Turn Your Admissions Ambitions Into Top-Tier Offers</h3>
      <p>Elite business school applications are engineered, not left to chance. Schedule a dedicated 1-on-1 profile evaluation with our former M7 &amp; top IIM admissions advisors.</p>
      
      <div class="cta-landing-links" style="display:flex; flex-wrap:wrap; justify-content:center; gap:10px; margin:16px 0;">
        <a href="https://www.mbawizards.co.in/gmat-coaching" target="_blank" class="resource-link-btn">GMAT Coaching ↗</a>
        <a href="https://www.mbawizards.co.in/cat" target="_blank" class="resource-link-btn">CAT Coaching ↗</a>
        <a href="https://www.mbawizards.co.in/gre-coaching-classes" target="_blank" class="resource-link-btn">GRE Classes ↗</a>
        <a href="https://www.mbawizards.co.in/gmat-cat-coaching" target="_blank" class="resource-link-btn">GMAT + CAT Track ↗</a>
        <a href="https://www.mbawizards.co.in/education-loan" target="_blank" class="resource-link-btn">Education Loans ↗</a>
        <a href="https://www.mbawizards.co.in/contact-us" target="_blank" class="resource-link-btn" style="background:var(--gold); color:#0b0e14; font-weight:700;">Book Free Demo ↗</a>
      </div>

      <div class="cta-contact-links">
        <span>📧 <strong>admissions@mbawizards.com</strong></span>
        <span>📞 <strong>+91 99580 41888</strong></span>
        <span>🌐 <a href="https://www.mbawizards.co.in" target="_blank" style="color:#fff; text-decoration:none;"><strong>www.mbawizards.co.in</strong></a></span>
      </div>
    </div>
  </div>

</div>

RULES:
- Return ONLY valid HTML.
- Do NOT wrap in markdown code backticks like ```html.
- Fill all placeholders with hyper-specific, intelligent advice based on the candidate's exact profile.
- Maintain top-tier consulting excellence throughout.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Senior Partner & Lead Admissions Committee Strategist at MBAWizards. Generate exhaustive, diagnostic, top-tier admissions intelligence."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        output = response.choices[0].message.content.strip()

        # Clean markdown code block wrap if returned
        if output.startswith("```"):
            lines = output.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            output = "\n".join(lines).strip()

        if not output or ("<div" not in output and "<h3>" not in output):
            raise ValueError("Invalid output format")

        # Supabase Integration: Update career_students_data with generated roadmap
        if supabase:
            try:
                email = profile.get("email", "").strip().lower()
                if email:
                    target_univ = profile.get("dreamUniversity", "").strip() or None
                    target_cntry = profile.get("targetCountry", "").strip() or None
                    target_fld = profile.get("degreePreference", "").strip() or profile.get("targetRole", "").strip() or None

                    update_data = {
                        "email": email,
                        "full_name": profile.get("fullName", "").strip() or None,
                        "phone": profile.get("phone", "").strip() or None,
                        "city": profile.get("city", "").strip() or None,
                        "country": profile.get("country", "").strip() or None,
                        "nationality": profile.get("nationality", "").strip() or None,
                        "education_level": profile.get("educationLevel", "").strip() or None,
                        "field_of_study": profile.get("fieldOfStudy", "").strip() or None,
                        "target_university": target_univ,
                        "target_country": target_cntry,
                        "target_field": target_fld,
                        "career_interest": profile.get("careerInterest", "").strip() or None,
                        "generated_html": output,
                        "generated_response": output,
                        "raw_form_data": profile
                    }

                    supabase.table("career_students_data").upsert(
                        update_data,
                        on_conflict="email"
                    ).execute()
                    print(f"Supabase: Saved generated roadmap for {email}")
            except Exception as db_err:
                print("Supabase report save error:", db_err)

        return jsonify({"result": output})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "result": """
            <div style="padding:24px; background:#fff; border-radius:12px; border:1px solid #e2e8f0; text-align:center;">
                <h3 style="color:#b91c1c; margin-bottom:8px;">Roadmap Generation Interrupted</h3>
                <p style="color:#64748b; font-size:14px; margin-bottom:16px;">We encountered a temporary processing delay. Please try again or connect directly with our advisory team.</p>
                <div style="font-size:13px; color:#334155;">
                    📧 <strong>admissions@mbawizards.com</strong> &nbsp;|&nbsp; 📞 <strong>+91 99580 41888</strong> &nbsp;|&nbsp; 🌐 <strong><a href="https://www.mbawizards.co.in" target="_blank">www.mbawizards.co.in</a></strong>
                </div>
            </div>
            """
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f">> MBAWizards UniCompass running on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)