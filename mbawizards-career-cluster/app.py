from flask import Flask, request, render_template_string
from openai import OpenAI
import os
import random
import re
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# ✅ OpenAI client initialization
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =====================================================================
# 1. DYNAMIC VOCABULARY ROTATION ENGINE
# =====================================================================
class VocabularyRotationEngine:
    BRANDING_POOL = [
        "Signature Work Development",
        "Strategic Profile Architecture",
        "Global Future Positioning",
        "Future-Ready Positioning",
        "Identity-Driven Applications",
        "Strategic Differentiation",
        "Precision Profile Engineering",
        "Academic & Professional Moat Architecture"
    ]
    
    OPENER_POOL = [
        "A diagnostic assessment of the candidate's strategic profile architecture reveals...",
        "Evaluating the candidate's trajectory through the lens of global future positioning highlights...",
        "Upon auditing the current metrics and positioning blueprint of the candidate, we observe...",
        "To establish a defensible strategic differentiation in elite admissions ecosystems, we must address...",
        "The candidate's profile architecture presents a unique nexus of capabilities, but requires precision profile engineering..."
    ]
    
    FUTURE_POOL = [
        "establishing a highly differentiated intellectual moat in the target ecosystem",
        "positioning the candidate as an indispensable strategic asset rather than a commodity applicant",
        "future-proofing the career trajectory against technological and algorithmic displacement",
        "orchestrating a narrative of high-leverage leadership and domain authority",
        "aligning academic credentials with high-impact, real-world utility in a changing labor market"
    ]
    
    CONSULTANT_POOL = [
        "This critical lever for profile optimization...",
        "Our strategic diagnosis underscores the necessity to...",
        "To secure a decisive competitive advantage in highly selective environments...",
        "The gap in current positioning is not merely quantitative, but narrative...",
        "Executing on these micro-differentiation pathways will pivot the candidate from..."
    ]
    
    AI_POOL = [
        "harnessing cognitive amplification and computational leverage",
        "orchestrating AI-augmented analytical workflows",
        "bridging niche domain expertise with advanced data-driven systems",
        "understanding the automation frontier in the target sector",
        "cultivating high-IQ cognitive skills that resist machine replication"
    ]
    
    @classmethod
    def get_rotation(cls):
        return {
            "branding": random.sample(cls.BRANDING_POOL, 4),
            "opener": random.choice(cls.OPENER_POOL),
            "future": random.sample(cls.FUTURE_POOL, 2),
            "consultant": random.sample(cls.CONSULTANT_POOL, 2),
            "ai": random.sample(cls.AI_POOL, 2)
        }


# =====================================================================
# 2. SIGNATURE WORK RECOMMENDATION DATABASE
# =====================================================================
SIGNATURE_WORK_TEMPLATES = {
    "Computer Science / IT": [
        "Architect and implement a custom compiler or lightweight virtual machine designed to optimize execution of resource-constrained IoT edge nodes.",
        "Develop an open-source decentralized identity protocol utilizing zero-knowledge proofs to authenticate academic credentials securely.",
        "Create an automated database query optimization engine utilizing reinforcement learning to minimize latency in highly distributed systems."
    ],
    "Artificial Intelligence / Data Science": [
        "Architect a domain-specific Small Language Model (SLM) trained on curated datasets for real-time compliance audits in healthcare/finance.",
        "Develop a generative AI pipeline for molecular docking simulation, reducing the drug discovery evaluation timeframe by 40%.",
        "Construct a predictive maintenance engine for municipal infrastructure using multi-modal satellite imagery and sensor networks."
    ],
    "Electrical / Electronics Engineering": [
        "Design and prototype a high-efficiency power management integrated circuit (PMIC) for wearables leveraging kinetic energy harvesting.",
        "Implement a hardware-level cryptographic accelerator on an FPGA to secure edge computing communications against side-channel attacks.",
        "Develop a closed-loop neural feedback interface prototype using microcontrollers and low-power EMG sensors."
    ],
    "Mechanical Engineering": [
        "Design a biomimetic soft-robotic gripper with adaptive force feedback sensors for delicate surgical tool manipulation.",
        "Perform finite element analysis (FEA) and computational fluid dynamics (CFD) optimization of a 3D-printable wind turbine blade geometry.",
        "Develop an automated digital twin simulation framework for optimizing energy distribution efficiency in a manufacturing line."
    ],
    "Biotechnology / Life Sciences": [
        "Synthesize genomic sequences of extremophilic bacteria to engineer heat-resistant enzymes for agricultural plastic biodegradation.",
        "Develop an organ-on-a-chip microfluidic device prototype for assessing drug toxicity on vascular cells.",
        "Conduct a computational biology study mapping CRISPR-Cas9 off-target mutations using custom machine learning sequence models."
    ],
    "Medicine / MBBS": [
        "Conduct a clinical diagnostics research study using deep learning models to identify early-stage diabetic retinopathy in low-resource clinics.",
        "Draft a comprehensive medical ethics policy proposal analyzing the accountability of AI diagnostic agents in clinical environments.",
        "Prototype an IoT-enabled non-invasive continuous glucose monitor with real-time biometric telemetry encrypted for cloud endpoints."
    ],
    "Business Administration / MBA": [
        "Formulate a market-entry strategy report for a European clean-energy startup entering Southeast Asia, utilizing game-theory pricing simulations.",
        "Conduct an operations audit and digital transformation blueprint for a mid-market logistics firm, evaluating automation-induced labor shifts.",
        "Develop a quantitative business model assessing the risk, regulatory compliance, and unit economics of launching a fractional real estate platform."
    ],
    "Finance / Economics": [
        "Build a multi-factor quantitative trading algorithm simulating market responses to macroeconomic announcements using historical volatility data.",
        "Develop a macro-economic policy whitepaper simulating the systemic risk and liquidity effects of central bank digital currencies (CBDCs).",
        "Create an automated DeFi portfolio optimization engine utilizing risk-parity models to construct automated yield-bearing index tokens."
    ],
    "Law": [
        "Author a policy whitepaper defining liability frameworks for autonomous vehicle collisions, drawing comparisons across US, EU, and UK common law.",
        "Perform a comparative analysis of data privacy regulations (GDPR vs. CCPA) regarding data-scraping consent for LLM pre-training.",
        "Develop a smart-contract dispute resolution protocol combining automated arbitration logic with decentralized oracle consensus."
    ],
    "Architecture / Design": [
        "Design an eco-resilient community housing hub utilizing generative design algorithms to minimize heat island effects and maximize solar gain.",
        "Develop a parametric branding system that dynamically updates brand assets based on real-time environmental data inputs.",
        "Prototype an immersive VR educational environment evaluating spatial psychology and learning retention rates under varying lighting models."
    ]
}

DEFAULT_SIGNATURE_WORK_TEMPLATES = [
    "Develop a research-driven policy whitepaper addressing regulatory, technological, or systemic challenges in the target field.",
    "Formulate an analytical modeling system utilizing computational tools or domain-specific data to solve a major workflow inefficiency.",
    "Construct an open-source technical or creative portfolio demonstrating deep theoretical understanding applied to an industry-standard problem."
]


# =====================================================================
# 3. DYNAMIC COMMUNICATION STYLE ARCHETYPES
# =====================================================================
COMMUNICATION_STYLE_PROMPTS = {
    "Premium Consultant (Default)": {
        "description": "McKinsey/BCG consultant style. Structured, analytical, MECE, metric-driven, formal, and diagnostic.",
        "instructions": (
            "Write with clinical precision. Use structured headers, bulleted lists, and clear strategic frameworks. "
            "Adopt the voice of a senior diagnostics-first partner. Avoid exclamation marks or emotional appeals. "
            "Frame every observation as a strategic diagnosis (e.g., 'The profile's structural gap lies in the misalignment between...') "
            "and focus on leverage points and return on investment."
        )
    },
    "Harvard/Stanford Intellectual": {
        "description": "Prestigious academic style. High vocabulary, dense analytical prose, emphasizing research, intellectual curiosity, and deep domain theory.",
        "instructions": (
            "Write with deep intellectual gravity and scholarly authority. Use precise academic vocabulary and complex sentence structures. "
            "Focus on the 'why' of the discipline, emphasizing the candidate's potential for original research, contribution to literature, "
            "and scholarly leadership. Frame academic pursuits as an intellectual mission, referencing advanced methodologies."
        )
    },
    "Strategic Mentor": {
        "description": "Empathetic yet rigorous mentor. Warm, guidance-focused, encouraging, yet highly demanding of excellence and personal growth.",
        "instructions": (
            "Adopt the supportive yet firm voice of a veteran advisor. Use encouraging yet direct phrasing. "
            "Empathetically address profile limitations and pivot them into opportunities for personal and professional growth. "
            "Emphasize values, purpose, integrity, and long-term societal impact. Use collaborative framing (e.g., 'We must focus our efforts on...')."
        )
    },
    "Tech Founder": {
        "description": "Disruptive founder style. Action-oriented, tech-focused, emphasis on building products, launching MVPs, and scale.",
        "instructions": (
            "Write with high-velocity, product-centric, and tech-focused language. Emphasize shipping code, launching MVPs, building systems, "
            "scalability, and disruptive innovation. Use short, punchy sentences. "
            "Frame tasks as sprints, milestones, or product roadmaps. Focus on real-world adoption, metrics, and technological leverage."
        )
    },
    "Competitive FOMO": {
        "description": "Urgency-driven and highly selective. Highlights the scarcity of top-tier roles and what is required to beat the top 1% globally.",
        "instructions": (
            "Instill a strong sense of urgency, high-stakes competition, and elite exclusivity. Highlight the intense selectivity of top-tier universities "
            "and global career environments. Focus on what it takes to outperform the top 1% of international candidates. "
            "Use phrases like 'In a landscape where only 3% are admitted...', 'Every minor gap in your profile will be scrutinized...', "
            "'To secure a seat in this hyper-competitive cohort, your positioning must...'. Keep pressure high, but channel it into strategic action."
        )
    },
    "Gen-Z Future-Proof": {
        "description": "Tech-native and highly dynamic. Bold, forward-looking, emphasizing side hustles, AI workflows, and portfolios over credentials.",
        "instructions": (
            "Write in a modern, tech-native, and energetic voice. Focus on dismantling traditional credentialism in favor of building an "
            "unstoppable personal brand, side projects, and proof of work. Emphasize modern tools, remote leverage, "
            "AI augmentation, and rapid pivoting. Use active, direct, and conversational but highly intelligent phrasing."
        )
    }
}


# =====================================================================
# 4. PREMIUM EMBEDDED HTML TEMPLATES
# =====================================================================
FORM_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>EduQuest - Strategic Profile Architecture</title>
  
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet" />

  <style>
    :root {
      --bg-base: #060913;
      --bg-card: rgba(11, 16, 28, 0.65);
      --gold-primary: #c9a84c;
      --gold-hover: #e0b84e;
      --gold-glow: rgba(201, 168, 76, 0.15);
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --border-color: rgba(201, 168, 76, 0.15);
      --error-color: #ef4444;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    @keyframes gradientAnimation {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: linear-gradient(-45deg, #05070c, #0b101d, #0d1222, #070911);
      background-size: 400% 400%;
      animation: gradientAnimation 15s ease infinite;
      color: var(--text-main);
      min-height: 100vh;
      padding: 60px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    /* ---- Page Header ---- */
    .page-header {
      text-align: center;
      margin-bottom: 40px;
      max-width: 800px;
    }

    .page-header .badge {
      display: inline-block;
      background: rgba(201, 168, 76, 0.08);
      color: var(--gold-primary);
      border: 1px solid var(--border-color);
      padding: 6px 16px;
      border-radius: 30px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 16px;
      box-shadow: 0 0 15px rgba(201, 168, 76, 0.05);
    }

    .page-header h1 {
      font-family: 'Cinzel', serif;
      font-size: 38px;
      font-weight: 700;
      letter-spacing: 1px;
      color: #fff;
      margin-bottom: 12px;
      text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }

    .page-header h1 span {
      color: var(--gold-primary);
    }

    .page-header p {
      font-size: 15px;
      color: var(--text-muted);
      line-height: 1.6;
    }

    /* ---- Form Card ---- */
    .form-card {
      background: var(--bg-card);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      max-width: 900px;
      width: 100%;
      border-radius: 20px;
      padding: 44px 50px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
      border: 1px solid var(--border-color);
      position: relative;
      overflow: hidden;
    }

    .form-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, #8a6f27, var(--gold-primary), #8a6f27);
    }

    /* ---- Section Title ---- */
    .section-title {
      font-family: 'Cinzel', serif;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--gold-primary);
      border-bottom: 1px solid rgba(201, 168, 76, 0.1);
      padding-bottom: 10px;
      margin-bottom: 24px;
      margin-top: 36px;
    }

    .section-title:first-of-type {
      margin-top: 0;
    }

    /* ---- Grids ---- */
    .two-col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }

    .three-col {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 20px;
    }

    /* ---- Field ---- */
    .field {
      margin-bottom: 20px;
    }

    .field label {
      display: block;
      font-size: 13px;
      font-weight: 600;
      color: #e5e7eb;
      margin-bottom: 8px;
      letter-spacing: 0.5px;
    }

    .field label .optional {
      font-weight: 400;
      color: #6b7280;
      font-size: 11px;
      margin-left: 4px;
    }

    .field label .required {
      color: var(--gold-primary);
      margin-left: 2px;
    }

    .field input,
    .field select,
    .field textarea {
      width: 100%;
      padding: 12px 16px;
      border: 1.5px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 14px;
      color: #fff;
      background: rgba(11, 16, 28, 0.4);
      outline: none;
      transition: all 0.3s ease;
    }

    .field input:focus,
    .field select:focus,
    .field textarea:focus {
      border-color: var(--gold-primary);
      box-shadow: 0 0 15px var(--gold-glow);
      background: rgba(11, 16, 28, 0.8);
    }

    .field input::placeholder,
    .field textarea::placeholder {
      color: #555c6d;
    }

    .field textarea {
      resize: vertical;
      min-height: 100px;
    }

    /* ---- Education Level Pills ---- */
    .edu-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
    }

    .edu-pills input[type="radio"] {
      display: none;
    }

    .edu-pills label {
      padding: 10px 20px;
      border: 1.5px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      background: rgba(11, 16, 28, 0.3);
      transition: all 0.3s ease;
    }

    .edu-pills label:hover {
      border-color: rgba(201, 168, 76, 0.5);
      color: #fff;
    }

    .edu-pills input[type="radio"]:checked + label {
      background: rgba(201, 168, 76, 0.1);
      border-color: var(--gold-primary);
      color: var(--gold-primary);
      box-shadow: 0 0 15px var(--gold-glow);
    }

    /* ---- Hidden field (used by JS) ---- */
    .hidden {
      display: none;
    }

    /* ---- Validation error ---- */
    .error-msg {
      display: none;
      font-size: 12px;
      color: var(--error-color);
      margin-top: 6px;
      font-weight: 500;
    }

    .field.has-error input,
    .field.has-error select,
    .field.has-error textarea {
      border-color: var(--error-color) !important;
      background: rgba(239, 68, 68, 0.05);
    }

    .field.has-error .error-msg {
      display: block;
    }

    /* ---- Consent ---- */
    .consent {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 28px;
      margin-top: 12px;
    }

    .consent input[type="checkbox"] {
      margin-top: 4px;
      accent-color: var(--gold-primary);
      width: 17px;
      height: 17px;
      flex-shrink: 0;
      cursor: pointer;
    }

    .consent span {
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.6;
    }

    /* ---- Submit Button ---- */
    .submit-btn {
      width: 100%;
      padding: 16px;
      background: linear-gradient(135deg, #8a6f27, var(--gold-primary));
      color: #060913;
      border: none;
      border-radius: 10px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      letter-spacing: 1px;
      text-transform: uppercase;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
      transition: all 0.3s ease;
    }

    .submit-btn:hover {
      background: linear-gradient(135deg, var(--gold-primary), var(--gold-hover));
      transform: translateY(-2px);
      box-shadow: 0 6px 25px rgba(201, 168, 76, 0.3);
    }

    .submit-btn:active {
      transform: translateY(0);
    }

    /* ---- Footer Contact ---- */
    .footer-contact {
      text-align: center;
      margin-top: 24px;
      font-size: 12px;
      color: #4b5563;
      line-height: 1.8;
      letter-spacing: 0.5px;
    }

    /* ---- Fullscreen Loader ---- */
    .loader-overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(5, 7, 12, 0.95);
      z-index: 10000;
      justify-content: center;
      align-items: center;
      flex-direction: column;
    }

    .loader-spinner {
      position: relative;
      width: 100px;
      height: 100px;
      margin-bottom: 30px;
    }

    .loader-circle {
      width: 100%;
      height: 100%;
      border: 3px stroke transparent;
      border-top: 3px solid var(--gold-primary);
      border-radius: 50%;
      animation: spin 1.5s linear infinite;
    }

    .loader-inner-circle {
      position: absolute;
      top: 15px;
      left: 15px;
      width: 70px;
      height: 70px;
      border: 3px stroke transparent;
      border-bottom: 3px solid #8a6f27;
      border-radius: 50%;
      animation: spin-reverse 2s linear infinite;
    }

    .loader-text-branding {
      font-family: 'Cinzel', serif;
      font-size: 24px;
      letter-spacing: 3px;
      color: #fff;
      margin-bottom: 8px;
    }

    .loader-subtext {
      color: var(--gold-primary);
      font-size: 13px;
      letter-spacing: 1px;
      text-transform: uppercase;
      font-weight: 600;
      margin-bottom: 24px;
    }

    .loader-message {
      color: var(--text-muted);
      font-size: 14px;
      text-align: center;
      max-width: 400px;
      line-height: 1.6;
      height: 40px;
      transition: opacity 0.5s ease;
    }

    @keyframes spin {
      100% { transform: rotate(360deg); }
    }

    @keyframes spin-reverse {
      100% { transform: rotate(-360deg); }
    }

    /* ---- Responsive ---- */
    @media (max-width: 768px) {
      .form-card {
        padding: 30px 24px;
      }
      .two-col, .three-col {
        grid-template-columns: 1fr;
      }
      .page-header h1 {
        font-size: 28px;
      }
    }
  </style>
</head>
<body>

  <!-- Page Header -->
  <div class="page-header">
    <div class="badge">✦ EduQuest Strategic Intelligence ✦</div>
    <h1>Strategic <span>Profile</span> Architect</h1>
    <p>Submit your raw metrics. Receive an elite admissions intelligence roadmap engineered to differentiate your profile against the global top 1%.</p>
  </div>

  <!-- Fullscreen Loader -->
  <div class="loader-overlay" id="loaderOverlay">
    <div class="loader-spinner">
      <div class="loader-circle"></div>
      <div class="loader-inner-circle"></div>
    </div>
    <div class="loader-text-branding">EDUQUEST</div>
    <div class="loader-subtext">Strategic Diagnostics Engine</div>
    <div class="loader-message" id="loaderMessage">Initializing profile metrics diagnostic...</div>
  </div>

  <!-- Form Card -->
  <div class="form-card" id="formCard">
    <form id="mainForm" action="/generate" method="POST">

      <!-- ── Strategic Architecture Setup ── -->
      <div class="section-title">Strategic Architecture Setup</div>

      <div class="two-col">
        <div class="field">
          <label>Coaching Archetype &amp; Tone <span class="required">*</span></label>
          <select name="coaching_style" required>
            <option value="Premium Consultant (Default)" selected>Premium Consultant (McKinsey Style)</option>
            <option value="Harvard/Stanford Intellectual">Harvard/Stanford Intellectual (Academic Rigor)</option>
            <option value="Strategic Mentor">Strategic Mentor (Empathetic &amp; Demanding)</option>
            <option value="Tech Founder">Tech Founder (Disruptive &amp; Practical)</option>
            <option value="Competitive FOMO">Competitive FOMO (Elite Selectivity Focus)</option>
            <option value="Gen-Z Future-Proof">Gen-Z Future-Proof (Modern Leverage)</option>
          </select>
          <span class="error-msg">Coaching Archetype is required.</span>
        </div>
        <div class="field">
          <label>Dream University <span class="required">*</span></label>
          <input type="text" name="dream_university" placeholder="e.g. MIT, Stanford, Oxford, NUS" required />
          <span class="error-msg">Dream university is required.</span>
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>Target Country <span class="required">*</span></label>
          <select name="target_country" required>
            <option value="" disabled selected>Select country</option>
            <option>United States (USA)</option>
            <option>United Kingdom (UK)</option>
            <option>Canada</option>
            <option>Australia</option>
            <option>Germany</option>
            <option>Netherlands</option>
            <option>Singapore</option>
            <option>Ireland</option>
            <option>New Zealand</option>
            <option>France</option>
            <option>Japan</option>
            <option>Other</option>
          </select>
          <span class="error-msg">Please select target country.</span>
        </div>
        <div class="field">
          <label>Target Field of Study <span class="required">*</span></label>
          <select name="target_field" required>
            <option value="" disabled selected>Select field</option>
            <option>Computer Science / IT</option>
            <option>Artificial Intelligence / Data Science</option>
            <option>Electrical / Electronics Engineering</option>
            <option>Mechanical Engineering</option>
            <option>Biotechnology / Life Sciences</option>
            <option>Medicine / MBBS</option>
            <option>Business Administration / MBA</option>
            <option>Finance / Economics</option>
            <option>Law</option>
            <option>Architecture / Design</option>
            <option>Other</option>
          </select>
          <span class="error-msg">Please select target field.</span>
        </div>
      </div>

      <!-- ── Candidate Information ── -->
      <div class="section-title">Candidate Profile &amp; Credentials</div>

      <div class="two-col">
        <div class="field">
          <label>Full Name <span class="required">*</span></label>
          <input type="text" name="full_name" placeholder="e.g. Arjun Sharma" required />
          <span class="error-msg">Full Name is required.</span>
        </div>
        <div class="field">
          <label>Age <span class="required">*</span></label>
          <input type="number" name="age" placeholder="e.g. 18" min="10" max="60" required />
          <span class="error-msg">Please enter a valid age.</span>
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>Phone Number <span class="required">*</span></label>
          <input type="tel" name="phone" placeholder="e.g. +91 98765 43210" required />
          <span class="error-msg">Phone number is required.</span>
        </div>
        <div class="field">
          <label>Email Address <span class="required">*</span></label>
          <input type="email" name="email" placeholder="e.g. arjun@domain.com" required />
          <span class="error-msg">Valid email is required.</span>
        </div>
      </div>

      <div class="three-col">
        <div class="field">
          <label>City <span class="required">*</span></label>
          <input type="text" name="city" placeholder="e.g. New Delhi" required />
          <span class="error-msg">City is required.</span>
        </div>
        <div class="field">
          <label>Country of Residence <span class="required">*</span></label>
          <input type="text" name="country" placeholder="e.g. India" required />
          <span class="error-msg">Residence is required.</span>
        </div>
        <div class="field">
          <label>Nationality <span class="required">*</span></label>
          <input type="text" name="nationality" placeholder="e.g. Indian" required />
          <span class="error-msg">Nationality is required.</span>
        </div>
      </div>

      <!-- ── Academic Background ── -->
      <div class="section-title">Academic &amp; Professional Foundation</div>

      <div class="field">
        <label>Highest Qualification <span class="required">*</span></label>
        <div class="edu-pills" id="eduPills">
          <input type="radio" name="edu_level" id="lvl10" value="10th" required />
          <label for="lvl10">10th</label>

          <input type="radio" name="edu_level" id="lvl12" value="12th" />
          <label for="lvl12">12th</label>

          <input type="radio" name="edu_level" id="lvlDip" value="Diploma" />
          <label for="lvlDip">Diploma</label>

          <input type="radio" name="edu_level" id="lvlBach" value="Bachelor's" />
          <label for="lvlBach">Bachelor's</label>

          <input type="radio" name="edu_level" id="lvlMast" value="Master's" />
          <label for="lvlMast">Master's</label>
        </div>
        <span class="error-msg" id="eduPillsError">Please select your highest qualification.</span>
      </div>

      <div class="two-col">
        <!-- Field of Study — only show for Diploma / Bachelor's / Master's -->
        <div class="field hidden" id="fieldOfStudyWrapper">
          <label>Field of Study <span class="required">*</span></label>
          <input type="text" name="field_of_study" id="fieldOfStudy" placeholder="e.g. Computer Science" />
          <span class="error-msg">Field of study is required.</span>
        </div>

        <!-- Year of Graduation — only show for Bachelor's / Master's -->
        <div class="field hidden" id="gradYearWrapper">
          <label>Year of Graduation <span class="required">*</span></label>
          <select name="grad_year" id="gradYear">
            <option value="" disabled selected>Select year</option>
          </select>
          <span class="error-msg">Please select year of graduation.</span>
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>CGPA / Percentage / Grade <span class="required">*</span></label>
          <input type="text" name="cgpa" placeholder="e.g. 8.9 CGPA or 89%" required />
          <span class="error-msg">Academic grade is required.</span>
        </div>
        <div class="field">
          <label>Academic Gap Years</label>
          <select name="gap_years">
            <option value="0">No gap</option>
            <option value="1">1 year</option>
            <option value="2">2 years</option>
            <option value="3">3 years</option>
            <option value="4+">4+ years</option>
          </select>
        </div>
      </div>

      <!-- Test Scores -->
      <div class="three-col">
        <div class="field">
          <label>SAT / ACT Score <span class="optional">optional</span></label>
          <input type="text" name="sat_score" placeholder="e.g. 1510 SAT" />
        </div>
        <div class="field">
          <label>GRE / GMAT Score <span class="optional">optional</span></label>
          <input type="text" name="gmat_score" placeholder="e.g. 325 GRE" />
        </div>
        <div class="field">
          <label>IELTS / TOEFL Score <span class="optional">optional</span></label>
          <input type="text" name="ielts_score" placeholder="e.g. 8.0 IELTS" />
        </div>
      </div>

      <div class="field">
        <label>Professional / Internship Work Experience <span class="optional">(if any)</span></label>
        <textarea name="work_experience" placeholder="Detail your roles, durations, and key computational/business outcomes..."></textarea>
      </div>

      <div class="field">
        <label>Key Co-Curricular Assets &amp; Achievements <span class="optional">(if any)</span></label>
        <textarea name="achievements" placeholder="Olympiads, hackathons, publications, research projects, leadership positions..."></textarea>
      </div>

      <!-- Consent -->
      <div class="consent">
        <input type="checkbox" name="consent" id="consent" required />
        <span>
          I authorize the EduQuest Strategic Intelligence Engine to process my profile metrics. 
          My data will be encrypted and treated in accordance with elite privacy and confidentiality protocols.
        </span>
      </div>

      <!-- Submit -->
      <button type="submit" class="submit-btn">Run Diagnostics &amp; Position Profile →</button>

      <!-- Contact -->
      <div class="footer-contact">
        EduQuest Group Global Headquarters &nbsp;|&nbsp; 📧 contact@eduquest.org.in &nbsp;|&nbsp; 📞 +91 99580 41888
      </div>

    </form>
  </div>

  <script>
    // Fill Graduation Year
    const gradSelect = document.getElementById('gradYear');
    const currentYear = new Date().getFullYear();
    for (let y = currentYear - 15; y <= currentYear + 6; y++) {
      const opt = document.createElement('option');
      opt.value = y;
      opt.textContent = y;
      if (y === currentYear) opt.selected = true;
      gradSelect.appendChild(opt);
    }

    // Dynamic Field Toggling
    const radios = document.querySelectorAll('input[name="edu_level"]');
    const fieldOfStudyWrapper = document.getElementById('fieldOfStudyWrapper');
    const fieldOfStudyInput = document.getElementById('fieldOfStudy');
    const gradYearWrapper = document.getElementById('gradYearWrapper');
    const gradYearSelect = document.getElementById('gradYear');

    const showFieldFor = ['Diploma', "Bachelor's", "Master's"];
    const showGradFor  = ["Bachelor's", "Master's"];

    function handleEduChange() {
      const selected = document.querySelector('input[name="edu_level"]:checked');
      if (!selected) return;

      const val = selected.value;

      if (showFieldFor.includes(val)) {
        fieldOfStudyWrapper.classList.remove('hidden');
        fieldOfStudyInput.required = true;
      } else {
        fieldOfStudyWrapper.classList.add('hidden');
        fieldOfStudyInput.required = false;
        fieldOfStudyInput.value = '';
      }

      if (showGradFor.includes(val)) {
        gradYearWrapper.classList.remove('hidden');
        gradYearSelect.required = true;
      } else {
        gradYearWrapper.classList.add('hidden');
        gradYearSelect.required = false;
      }
    }

    radios.forEach(radio => radio.addEventListener('change', handleEduChange));

    // Form Submission & Loader
    document.getElementById('mainForm').addEventListener('submit', function(e) {
      document.getElementById('loaderOverlay').style.display = 'flex';
      
      const messages = [
        "Analyzing strategic profile architecture...",
        "Retrieving domain signature work templates...",
        "Evaluating global competitiveness matrices...",
        "Applying dynamic communication style layers...",
        "Evaluating AI vulnerability metrics...",
        "Synthesizing precision profile moats...",
        "Architecting competitive admissions positioning..."
      ];
      let index = 0;
      const msgEl = document.getElementById('loaderMessage');
      setInterval(() => {
        index = (index + 1) % messages.length;
        msgEl.textContent = messages[index];
      }, 2500);
    });
  </script>

</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EduQuest - Strategic Positioning Briefing</title>
  
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --bg-base: #060913;
      --bg-card: rgba(11, 16, 28, 0.65);
      --gold-primary: #c9a84c;
      --gold-hover: #e0b84e;
      --gold-glow: rgba(201, 168, 76, 0.15);
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --border-color: rgba(201, 168, 76, 0.15);
      --sidebar-width: 320px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: 'Plus Jakarta Sans', sans-serif;
      min-height: 100vh;
      display: flex;
      background-image: radial-gradient(circle at 10% 20%, rgba(201, 168, 76, 0.04) 0%, transparent 40%),
                        radial-gradient(circle at 90% 80%, rgba(138, 111, 39, 0.04) 0%, transparent 40%);
    }

    /* ---- Outer Layout ---- */
    .layout-wrapper {
      display: flex;
      width: 100%;
      max-width: 1400px;
      margin: 0 auto;
      padding: 40px 20px;
      gap: 30px;
    }

    /* ---- Sidebar Panel ---- */
    .sidebar {
      width: var(--sidebar-width);
      flex-shrink: 0;
      position: sticky;
      top: 40px;
      height: calc(100vh - 80px);
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 28px 24px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
      overflow-y: auto;
    }

    .sidebar::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, #8a6f27, var(--gold-primary));
    }

    .brand-header {
      text-align: center;
      margin-bottom: 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      padding-bottom: 16px;
    }

    .brand-header h2 {
      font-family: 'Cinzel', serif;
      font-size: 20px;
      letter-spacing: 2px;
      color: #fff;
      margin-bottom: 4px;
    }

    .brand-header p {
      font-size: 10px;
      color: var(--gold-primary);
      text-transform: uppercase;
      letter-spacing: 1.5px;
      font-weight: 700;
    }

    /* Candidate Profile Overview */
    .candidate-card {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 24px;
    }

    .candidate-card h3 {
      font-size: 15px;
      color: #fff;
      margin-bottom: 8px;
      border-bottom: 1px solid rgba(201, 168, 76, 0.2);
      padding-bottom: 4px;
    }

    .meta-item {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      margin-bottom: 6px;
    }

    .meta-item .label {
      color: var(--text-muted);
    }

    .meta-item .val {
      font-weight: 600;
      color: #fff;
      text-align: right;
    }

    /* Score Ring Container */
    .score-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
      margin-bottom: 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      padding-bottom: 20px;
    }

    .score-box {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .score-title {
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-top: 8px;
      font-weight: 600;
    }

    .progress-ring {
      position: relative;
      width: 100px;
      height: 100px;
    }

    .progress-ring svg {
      width: 100px;
      height: 100px;
    }

    .progress-ring circle {
      cx: 50;
      cy: 50;
      r: 44;
      fill: transparent;
      stroke-width: 6;
    }

    .progress-ring .ring-bg {
      stroke: rgba(255, 255, 255, 0.03);
    }

    .progress-ring .ring-val {
      stroke: var(--gold-primary);
      stroke-linecap: round;
      transform: rotate(-90deg);
      transform-origin: 50px 50px;
      transition: stroke-dashoffset 1s ease-out;
    }

    .progress-ring .score-text {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-family: 'Cinzel', serif;
      font-size: 20px;
      font-weight: 700;
      color: #fff;
    }

    /* Action Buttons */
    .action-btn {
      width: 100%;
      padding: 12px;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      background: transparent;
      color: var(--gold-primary);
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 12px;
      transition: all 0.3s ease;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
    }

    .action-btn:hover {
      background: rgba(201, 168, 76, 0.08);
      border-color: var(--gold-hover);
      color: #fff;
    }

    .btn-gold {
      background: linear-gradient(135deg, #8a6f27, var(--gold-primary));
      color: #060913;
      border: none;
    }

    .btn-gold:hover {
      background: linear-gradient(135deg, var(--gold-primary), var(--gold-hover));
      box-shadow: 0 4px 15px rgba(201, 168, 76, 0.2);
      color: #060913;
    }

    /* ---- Main Content Column ---- */
    .content-area {
      flex: 1;
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 44px 50px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
      position: relative;
    }

    .content-area::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--gold-primary), #8a6f27);
    }

    /* ---- Report Content Styling (Generated by LLM) ---- */
    .report-section {
      margin-bottom: 40px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      padding-bottom: 30px;
    }

    .report-section:last-of-type {
      margin-bottom: 0;
      border-bottom: none;
      padding-bottom: 0;
    }

    .report-section h2 {
      font-family: 'Cinzel', serif;
      font-size: 20px;
      color: var(--gold-primary);
      margin-bottom: 18px;
      letter-spacing: 1px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .report-section h2::before {
      content: '';
      display: inline-block;
      width: 4px;
      height: 18px;
      background: var(--gold-primary);
    }

    .report-section h3 {
      font-size: 15px;
      color: #fff;
      margin-top: 20px;
      margin-bottom: 10px;
      font-weight: 600;
    }

    .report-section p {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.7;
      margin-bottom: 14px;
      text-align: justify;
    }

    .report-section ul {
      margin-left: 20px;
      margin-bottom: 14px;
    }

    .report-section li {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.7;
      margin-bottom: 8px;
    }

    /* Positioning Statement Highlight */
    .positioning-statement {
      background: rgba(201, 168, 76, 0.03);
      border-left: 3px solid var(--gold-primary);
      border-right: 1px solid rgba(201, 168, 76, 0.1);
      border-top: 1px solid rgba(201, 168, 76, 0.1);
      border-bottom: 1px solid rgba(201, 168, 76, 0.1);
      padding: 24px;
      border-radius: 0 12px 12px 0;
      margin: 20px 0;
      box-shadow: inset 0 0 10px rgba(0,0,0,0.2);
    }

    .positioning-statement p {
      font-family: 'Cinzel', serif;
      font-size: 15px;
      color: #fff;
      font-style: italic;
      line-height: 1.7;
      margin-bottom: 0;
    }

    /* Diagnostic weakness card */
    .weakness-card {
      background: rgba(239, 68, 68, 0.02);
      border: 1px solid rgba(239, 68, 68, 0.15);
      border-radius: 8px;
      padding: 18px;
      margin-bottom: 16px;
    }

    .weakness-card h4 {
      font-size: 14px;
      color: #ef4444;
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .weakness-card h4::before {
      content: '▲';
      font-size: 10px;
    }

    /* Signature project card */
    .signature-project {
      background: rgba(201, 168, 76, 0.02);
      border: 1px solid rgba(201, 168, 76, 0.15);
      border-radius: 10px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }

    .signature-project h4 {
      font-family: 'Cinzel', serif;
      font-size: 14px;
      color: var(--gold-primary);
      margin-bottom: 8px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }

    /* Premium Table styling */
    .table-premium {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 13px;
      background: rgba(255, 255, 255, 0.01);
      border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .table-premium th {
      background: rgba(201, 168, 76, 0.05);
      color: var(--gold-primary);
      text-transform: uppercase;
      letter-spacing: 1px;
      font-weight: 600;
      padding: 12px 14px;
      border-bottom: 1.5px solid var(--border-color);
      text-align: left;
    }

    .table-premium td {
      padding: 12px 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      color: var(--text-muted);
    }

    .table-premium tr:last-child td {
      border-bottom: none;
    }

    .table-premium tr:hover td {
      background: rgba(255, 255, 255, 0.015);
      color: #fff;
    }

    .differentiation-badge {
      display: inline-block;
      background: rgba(201, 168, 76, 0.08);
      border: 1px solid var(--gold-primary);
      color: var(--gold-primary);
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      margin-bottom: 8px;
    }

    /* Hide references in report text */
    .competitiveness-score-ref, .ai-readiness-score-ref {
      display: none;
    }

    /* ---- Responsive Design ---- */
    @media (max-width: 900px) {
      body {
        display: block;
      }
      .layout-wrapper {
        flex-direction: column;
        padding: 20px 10px;
      }
      .sidebar {
        width: 100%;
        position: relative;
        top: 0;
        height: auto;
        margin-bottom: 20px;
      }
      .content-area {
        padding: 24px 20px;
      }
    }

    /* ---- Print Stylesheet ---- */
    @media print {
      body {
        background: #fff !important;
        color: #000 !important;
        background-image: none !important;
        display: block !important;
      }
      .layout-wrapper {
        padding: 0 !important;
        display: block !important;
        max-width: 100% !important;
      }
      .sidebar, .action-btn {
        display: none !important;
      }
      .content-area {
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        background: transparent !important;
      }
      .report-section {
        page-break-inside: avoid;
        border-bottom: 1px solid #ddd !important;
      }
      .report-section h2 {
        color: #000 !important;
      }
      .report-section h2::before {
        background: #000 !important;
      }
      .positioning-statement {
        background: #f9f9f9 !important;
        border-color: #000 !important;
        color: #000 !important;
      }
      .positioning-statement p {
        color: #000 !important;
      }
      .signature-project {
        border-color: #999 !important;
        background: transparent !important;
      }
      .table-premium th {
        background: #eee !important;
        color: #000 !important;
        border-color: #000 !important;
      }
      .table-premium td {
        color: #000 !important;
        border-color: #ddd !important;
      }
    }
  </style>
</head>
<body>

  <div class="layout-wrapper">
    <!-- Sidebar Left Column -->
    <div class="sidebar">
      <div class="brand-header">
        <h2>EduQuest</h2>
        <p>Strategic Intelligence</p>
      </div>

      <!-- Candidate Metadata -->
      <div class="candidate-card">
        <h3>Profile Metadata</h3>
        <div class="meta-item">
          <span class="label">Candidate:</span>
          <span class="val">{{ full_name }}</span>
        </div>
        <div class="meta-item">
          <span class="label">Target:</span>
          <span class="val">{{ target_field }}</span>
        </div>
        <div class="meta-item">
          <span class="label">Institution:</span>
          <span class="val">{{ dream_university }}</span>
        </div>
        <div class="meta-item">
          <span class="label">Archetype:</span>
          <span class="val">{{ coaching_style }}</span>
        </div>
      </div>

      <!-- Live CSS Gauges -->
      <div class="score-container">
        <!-- Competitiveness Circle -->
        <div class="score-box">
          <div class="progress-ring">
            <svg>
              <circle class="ring-bg" />
              <circle class="ring-val" id="comp-ring" />
            </svg>
            <div class="score-text" id="comp-text">--%</div>
          </div>
          <div class="score-title">Global Competitiveness</div>
        </div>

        <!-- AI Readiness Circle -->
        <div class="score-box">
          <div class="progress-ring">
            <svg>
              <circle class="ring-bg" />
              <circle class="ring-val" id="ai-ring" />
            </svg>
            <div class="score-text" id="ai-text">--%</div>
          </div>
          <div class="score-title">AI Resilience Index</div>
        </div>
      </div>

      <!-- Actions -->
      <button class="action-btn btn-gold" onclick="window.print()">
        📄 Print Intelligence Briefing
      </button>
      
      <button class="action-btn" onclick="window.location.href='https://wa.me/919958041888'">
        💬 Connect with Lead Strategist
      </button>
      
      <button class="action-btn" onclick="window.location.href='/'">
        ← Analyze Another Profile
      </button>
      
      <div style="font-size:10px; color:var(--text-muted); text-align:center; margin-top:auto; line-height: 1.5;">
        Briefing ID: EQ-{{ briefing_id }}<br>
        Date: 2026-05-19
      </div>
    </div>

    <!-- Main Briefing Content Column -->
    <div class="content-area">
      {{ result|safe }}
    </div>
  </div>

  <script>
    // Animate Circular Gauges based on HTML response references
    document.addEventListener('DOMContentLoaded', () => {
      const compRef = document.querySelector('.competitiveness-score-ref');
      const aiRef = document.querySelector('.ai-readiness-score-ref');

      let compVal = 82; // Defaults if parsing fails
      let aiVal = 78;

      if (compRef) {
        compVal = parseInt(compRef.getAttribute('data-score')) || compVal;
      }
      if (aiRef) {
        aiVal = parseInt(aiRef.getAttribute('data-score')) || aiVal;
      }

      animateRing('comp-ring', 'comp-text', compVal);
      animateRing('ai-ring', 'ai-text', aiVal);
    });

    function animateRing(ringId, textId, targetScore) {
      const ring = document.getElementById(ringId);
      const text = document.getElementById(textId);
      if (!ring || !text) return;

      const radius = ring.r.baseVal.value;
      const circumference = 2 * Math.PI * radius;
      ring.style.strokeDasharray = circumference;
      
      // Start hidden
      ring.style.strokeDashoffset = circumference;
      
      setTimeout(() => {
        const offset = circumference - (targetScore / 100) * circumference;
        ring.style.transition = 'stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1)';
        ring.style.strokeDashoffset = offset;

        // Counter text animation
        let count = 0;
        const interval = setInterval(() => {
          if (count >= targetScore) {
            text.textContent = targetScore + '%';
            clearInterval(interval);
          } else {
            count++;
            text.textContent = count + '%';
          }
        }, 1500 / targetScore);
      }, 300);
    }
  </script>
</body>
</html>
"""

ERROR_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>EduQuest - Diagnostic Exception</title>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Plus+Jakarta+Sans:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      background: #060913;
      color: #f3f4f6;
      font-family: 'Plus Jakarta Sans', sans-serif;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 0;
    }
    .error-card {
      background: rgba(11, 16, 28, 0.65);
      border: 1px solid rgba(239, 68, 68, 0.2);
      max-width: 500px;
      padding: 40px;
      border-radius: 16px;
      text-align: center;
      box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    h1 {
      font-family: 'Cinzel', serif;
      color: #ef4444;
      font-size: 22px;
      margin-bottom: 16px;
      letter-spacing: 1px;
    }
    p {
      color: #9ca3af;
      font-size: 14px;
      line-height: 1.6;
      margin-bottom: 24px;
    }
    .btn {
      display: inline-block;
      background: #c9a84c;
      color: #060913;
      text-decoration: none;
      padding: 12px 24px;
      border-radius: 6px;
      font-weight: 700;
      text-transform: uppercase;
      font-size: 12px;
      letter-spacing: 0.5px;
      transition: background 0.3s;
    }
    .btn:hover {
      background: #e0b84e;
    }
  </style>
</head>
<body>
  <div class="error-card">
    <h1>⚠️ Strategic Diagnostics Exception</h1>
    <p>
      An error occurred while compiling your Strategic Profile Architecture report. 
      This is typically due to an API timeout or an intermittent connectivity problem with our positioning services.
    </p>
    <p style="font-size: 13px;">
      If issues persist, please reach out directly to our positioning desk:<br>
      📧 <strong>contact@eduquest.org.in</strong> &nbsp;|&nbsp; 📞 <strong>+91 99580 41888</strong>
    </p>
    <a href="/" class="btn">Re-initialize Diagnostics</a>
  </div>
</body>
</html>
"""


# =====================================================================
# 5. BACKEND FLASK ROUTING & CORE ENGINE
# =====================================================================
@app.route("/")
def home():
    return render_template_string(FORM_TEMPLATE)


@app.route("/generate", methods=["POST"])
def generate():
    # 1. Retrieve all student profile parameters
    form_data = request.form.to_dict()

    full_name = form_data.get("full_name", "Anonymous Candidate")
    target_field = form_data.get("target_field", "Selected Field")
    dream_university = form_data.get("dream_university", "Target Institution")
    coaching_style = form_data.get("coaching_style", "Premium Consultant (Default)")
    
    # Generate unique Briefing ID for authenticity
    briefing_id = str(random.randint(10243, 99876))

    # 2. Dynamic Communication Style lookup
    style_info = COMMUNICATION_STYLE_PROMPTS.get(coaching_style, COMMUNICATION_STYLE_PROMPTS["Premium Consultant (Default)"])

    # 3. Vocabulary Rotation extraction
    rotation = VocabularyRotationEngine.get_rotation()

    # 4. Signature Work Recommendations templates
    sig_templates = SIGNATURE_WORK_TEMPLATES.get(target_field, DEFAULT_SIGNATURE_WORK_TEMPLATES)
    sig_text = "\n".join([f"- PROJECT TYPE BRIEF: {t}" for t in sig_templates])

    # Convert remaining form inputs to structured readable blocks
    profile_summary = "\n".join(
        [f"- {key.replace('_', ' ').title()}: {value}" for key, value in form_data.items() if value]
    )

    # 5. Build prompt incorporating all engines and layers
    system_instructions = f"""
You are EduQuest AI — an elite global education strategist, university admissions consultant, and future positioning strategist.
Your voice is a mix of a McKinsey Senior Partner and an Ivy League Admissions Dean. 

ARCHETYPE TONE:
Apply the following communication style:
- Style Title: {coaching_style}
- Styling Instructions: {style_info["instructions"]}

YOUR CRITICAL GUIDELINE:
Do NOT output generic study abroad reports. You must employ a Human Strategic Reasoning Layer.
Your writing should be highly diagnostic, structured, analytical, and psychologically persuasive.
Avoid repetitive GPT phrase habits (e.g. "delve into", "journey", "embarking", "testament to", "it is important to remember", "furthermore").
Instead of weak recommendations (like "You should improve your profile"), write with authority:
"Your current positioning reflects strong analytical potential but limited differentiation through research-driven narrative depth."

COMPULSORY BRANDING INTEGRATION:
Repeatedly and naturally weave these EduQuest core branding concepts throughout the paragraphs:
- {rotation['branding'][0]}
- {rotation['branding'][1]}
- {rotation['branding'][2]}
- {rotation['branding'][3]}

COMPULSORY PROFILE INTRODUCTORY OPENER:
You MUST open the profile analysis section using exactly this phrase:
"{rotation['opener']}"

REQUIRED VOCABULARY INTEGRATION:
You must include these future positioning lines:
- {rotation['future'][0]}
- {rotation['future'][1]}

You must use these consulting diagnostic phrases:
- {rotation['consultant'][0]}
- {rotation['consultant'][1]}

You must use these AI transformation phrases:
- {rotation['ai'][0]}
- {rotation['ai'][1]}
"""

    user_prompt = f"""
Analyze the following student profile and generate their admissions intelligence report:

=========================================
STUDENT METRICS:
=========================================
{profile_summary}

=========================================
SIGNATURE WORK DATA BASE CONTEXT:
=========================================
Incorporate these project ideas when constructing the Signature Work section:
{sig_text}

=========================================
REQUIRED OUTPUT FORMAT & SECTIONS:
=========================================
You must return clean, production-ready HTML code inside the response (Do not wrap it in markdown backticks like ```html, just output raw HTML directly).
Generate the following exactly 9 HTML sections:

1. <div class="report-section" id="section-positioning">
     <h2>1. Profile Positioning Statement</h2>
     <!-- Combine their credentials, field, target country, and dream university into a single, high-stakes statement of strategic intent. Wrap the main statement in an HTML tag: <div class="positioning-statement"><p>...</p></div> -->
   </div>

2. <div class="report-section" id="section-advantages">
     <h2>2. Why You Stand Out</h2>
     <!-- Outline 2-3 specific competitive advantages using high-IQ consulting language. Detail how these align with the target field. -->
   </div>

3. <div class="report-section" id="section-weaknesses">
     <h2>3. Strategic Weakness Analysis</h2>
     <!-- Identify major profile gaps (such as CGPA limitations, lack of publication, gaps, or lack of international standing) and re-frame them. Use <div class="weakness-card"><h4>[GAP]</h4><p>[Strategic reframing & mitigation]</p></div> structures. -->
   </div>

4. <div class="report-section" id="section-competitiveness">
     <h2>4. Global Competitiveness Score</h2>
     <!-- Evaluate admit chances relative to the top 1% global applicant pool for their dream university. You MUST output this score ref tag: <span class="competitiveness-score-ref" data-score="[MUST be a raw integer score between 60 and 99]">[Score]%</span> followed by an analytical paragraph of the score rationale. -->
   </div>

5. <div class="report-section" id="section-ai-readiness">
     <h2>5. AI Readiness Index</h2>
     <!-- Evaluate the threat of AI automation in their chosen career field and their readiness to augment their workflow with computational tools. You MUST output this score ref tag: <span class="ai-readiness-score-ref" data-score="[MUST be a raw integer score between 60 and 99]">[Score]%</span> followed by an analysis of future-proofing techniques. -->
   </div>

6. <div class="report-section" id="section-signature-work">
     <h2>6. Signature Work Recommendations</h2>
     <!-- Suggest 3 hyper-targeted, high-fidelity project blueprints based on the database context. Make sure they highlight 'Signature Work Development' and 'Precision Profile Engineering'. Wrap each project in <div class="signature-project"><h4>[Project Title]</h4><p>[Project Brief & execution strategy]</p></div> -->
   </div>

7. <div class="report-section" id="section-future-positioning">
     <h2>7. Future Positioning Analysis</h2>
     <!-- Focus on the long-term career outlook, market growth, high-compensation niches, and tech/academic intersections in their target field. -->
   </div>

8. <div class="report-section" id="section-differentiation">
     <h2>8. Strategic Differentiation Opportunities</h2>
     <!-- Provide clear micro-differentiation strategies. Use a <div class="differentiation-badge">[Tag]</div> followed by detailed actionable items. -->
   </div>

9. <div class="report-section" id="section-transformation">
     <h2>9. AI & Industry Transformation Insights</h2>
     <!-- Explain the imminent technological shocks in the target field, the shift in labor economics, and how the student can position themselves as a high-leverage node. -->
   </div>
"""

    try:
        # Request completion from OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.75
        )

        output_content = response.choices[0].message.content.strip()

        # Clean markdown code blocks if the model returned them
        if output_content.startswith("```html"):
            output_content = output_content[7:]
        elif output_content.startswith("```"):
            output_content = output_content[3:]
        if output_content.endswith("```"):
            output_content = output_content[:-3]
        output_content = output_content.strip()

        # Validate that the generated report contains the minimum required sections
        if "report-section" not in output_content or "<h2>" not in output_content:
            raise ValueError("LLM response did not contain valid structured report sections.")

        return render_template_string(
            RESULT_TEMPLATE,
            result=output_content,
            full_name=full_name,
            target_field=target_field,
            dream_university=dream_university,
            coaching_style=coaching_style,
            briefing_id=briefing_id
        )

    except Exception as e:
        print("DIAGNOSTIC ERROR:", str(e))
        return render_template_string(ERROR_TEMPLATE)


# =====================================================================
# 6. APP EXECUTION ENTRYPOINT
# =====================================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)