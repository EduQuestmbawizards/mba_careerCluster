# MBAWizards · Graduate Admissions & Career Intelligence Platform

A dedicated **Graduate Admissions & Career Intelligence Platform** tailored for MBA & Master's aspirants, powered by OpenAI GPT-4o, Supabase PostgreSQL persistence, and official MBAWizards branding.

Official Portal: [https://www.mbawizards.co.in/](https://www.mbawizards.co.in/)

---

## 🚀 Key Features

1. **5-Step Fluid Intake Assessment**:
   - Comprehensive candidate profile audit across Education, Work Experience, Quantitative Skills, Degree Preferences, and Target B-Schools.
   - Required lead capture (Full Name, Phone/WhatsApp, Email, City) with automated SMTP notification to counselor admin with subject tag `mba- carer cluster`.

2. **5-Pillar Admissions Intelligence Engine**:
   - **Applicant Assessment**: Diagnostic audit of GPA caliber, pedigree, leadership velocity, and red flag mitigations.
   - **Course & Specialization Recommendation**: Prescribes whether the candidate should pursue a Full-Time MBA vs Specialised Master's (MiM / MSBA / MS Finance) vs Deferral based on profile strengths.
   - **GMAT vs CAT vs GRE Decision Engine**: Personalized exam verdict comparing format difficulty, section timings, scoring cutoffs, and target school alignment with direct links to MBAWizards test prep tracks.
   - **University & Programme Matching**: Tiered shortlists (Dream, Target, Safe) with live eligibility cutoffs, tuition & living costs, fellowship probabilities, and median post-grad compensation.
   - **Personalised Application Roadmap**: Test prep sprint calendar, personal narrative positioning, school-specific essay architecture, and behavioral interview preparation (STAR method).

3. **Supabase Database Persistence**:
   - Live synchronization with Supabase table `career_students_data`.
   - Full candidate snapshot stored inside `raw_form_data` (JSONB) and generated roadmaps preserved in `generated_html`.

---

## 📁 Repository Structure

```text
carrerCluster/
├── mbawizards-unicompass/         # Primary Graduate Admissions & Career Intelligence Platform
│   ├── app.py                     # Flask Server + GPT-4o Engine + Supabase Sync + SMTP Lead Email
│   ├── requirements.txt           # Python dependencies
│   ├── schema.sql                 # Supabase PostgreSQL Table Schema & RLS Policies
│   ├── static/images/             # MBAWizards Official Gold Logos (SVG & PNG)
│   └── templates/
│       └── index.html             # Fluid Full-Screen Metallic Gold & Obsidian Web Application
└── mbawizards-career-cluster/     # Specialized Career Diagnostic & Vocabulary Rotation Engine
```

---

## 🛠️ Local Development

1. Navigate to the platform directory:
   ```bash
   cd mbawizards-unicompass
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `.env` is populated with `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, and SMTP credentials.

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser at:
   ```text
   http://127.0.0.1:5050
   ```
