#!/usr/bin/env python3
"""
================================================================================
        ✨ SKILLSPARK PRO — AI Resume Analyzer (Desktop Edition)
        Professional Blue & White Theme | Python 3.10+ | Tkinter
================================================================================
  Dependencies (both optional — app works without them):
      pip install pypdf          (PDF reading)
      pip install reportlab      (PDF export)
================================================================================
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re
import os
from datetime import datetime

# ─── Optional libraries ───────────────────────────────────────────────────────
try:
    from pypdf import PdfReader
    PDF_READ_OK = True
except ImportError:
    try:
        import PyPDF2
        PDF_READ_OK = True
        _legacy_pdf = True
    except ImportError:
        PDF_READ_OK = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    PDF_EXPORT_OK = True
except ImportError:
    PDF_EXPORT_OK = False

# ─── Colour Palette (Professional Blue & White) ───────────────────────────────
BG_WHITE     = "#FFFFFF"
BG_LIGHT     = "#F0F4FF"
BG_PANEL     = "#EEF2FB"
BLUE_DARK    = "#1A3A6B"
BLUE_MID     = "#2563EB"
BLUE_LIGHT   = "#DBEAFE"
BLUE_ACCENT  = "#3B82F6"
TEXT_DARK    = "#0F172A"
TEXT_MID     = "#334155"
TEXT_LIGHT   = "#64748B"
SUCCESS      = "#16A34A"
WARNING      = "#D97706"
DANGER       = "#DC2626"
BORDER       = "#CBD5E1"
GOLD         = "#F59E0B"

# ─── Skill & Section Databases ────────────────────────────────────────────────
TECH_SKILLS = {
    'python': '🐍 Python',          'java': '☕ Java',
    'javascript': '📜 JavaScript',   'typescript': '🔷 TypeScript',
    'c++': '⚙️ C++',                 'c#': '🔵 C#',
    'html': '🌐 HTML',               'css': '🎨 CSS',
    'sql': '🗄️ SQL',                 'mysql': '🐬 MySQL',
    'postgresql': '🐘 PostgreSQL',   'mongodb': '🍃 MongoDB',
    'react': '⚛️ React',             'angular': '🅰️ Angular',
    'vue': '💚 Vue.js',              'node': '🟢 Node.js',
    'django': '🎸 Django',           'flask': '🧪 Flask',
    'fastapi': '⚡ FastAPI',         'spring': '🌱 Spring',
    'git': '📝 Git',                 'github': '🐙 GitHub',
    'docker': '🐳 Docker',           'kubernetes': '☸️ Kubernetes',
    'aws': '☁️ AWS',                 'azure': '🔷 Azure',
    'gcp': '🌤️ GCP',                 'linux': '🐧 Linux',
    'tensorflow': '🧠 TensorFlow',   'pytorch': '🔥 PyTorch',
    'machine learning': '🤖 Machine Learning',
    'deep learning': '🧬 Deep Learning',
    'data analysis': '📊 Data Analysis',
    'pandas': '🐼 Pandas',           'numpy': '🔢 NumPy',
    'power bi': '📊 Power BI',       'tableau': '📈 Tableau',
    'rest api': '🔌 REST API',       'graphql': '◈ GraphQL',
    'excel': '📗 Excel',             'r': '📉 R',
}

SOFT_SKILLS = {
    'communication': '💬 Communication',
    'teamwork': '🤝 Teamwork',
    'leadership': '👑 Leadership',
    'problem solving': '🧩 Problem Solving',
    'creativity': '🎨 Creativity',
    'time management': '⏰ Time Management',
    'adaptability': '🔄 Adaptability',
    'critical thinking': '🧠 Critical Thinking',
    'collaboration': '🤝 Collaboration',
    'attention to detail': '🔍 Attention to Detail',
    'project management': '📋 Project Management',
    'presentation': '🎤 Presentation',
    'analytical': '📐 Analytical',
    'multitasking': '⚡ Multitasking',
    'interpersonal': '🌐 Interpersonal',
}

REQUIRED_SECTIONS = {
    'experience': 'Work Experience',
    'education': 'Education',
    'skills': 'Skills',
    'projects': 'Projects',
    'summary': 'Summary/Objective',
    'certifications': 'Certifications',
    'achievements': 'Achievements',
    'internship': 'Internship',
}

JOB_ROLES = {
    'Full-Stack Developer':    {'python','javascript','react','node','sql','git','html','css'},
    'Data Scientist':          {'python','machine learning','pandas','numpy','sql','tensorflow','data analysis'},
    'Frontend Developer':      {'javascript','react','angular','vue','html','css','typescript','git'},
    'Backend Developer':       {'python','java','node','django','flask','sql','docker','git'},
    'DevOps Engineer':         {'docker','kubernetes','aws','linux','git','azure','gcp'},
    'Machine Learning Engineer':{'python','tensorflow','pytorch','machine learning','deep learning','pandas'},
    'Android Developer':       {'java','kotlin','git','android'},
    'Cloud Architect':         {'aws','azure','gcp','docker','kubernetes','linux'},
    'Data Analyst':            {'sql','python','excel','power bi','tableau','data analysis','pandas'},
    'Mobile Developer':        {'javascript','react','typescript','git'},
}

# ─── Resume Scoring Engine ────────────────────────────────────────────────────
def analyze_resume(text):
    text_lower = text.lower()
    words      = len(text.split())

    tech_found = [(k, v) for k, v in TECH_SKILLS.items() if k in text_lower]
    soft_found = [(k, v) for k, v in SOFT_SKILLS.items() if k in text_lower]
    sections_found = {k: v for k, v in REQUIRED_SECTIONS.items() if k in text_lower}

    score = 0
    breakdown = {}

    # Technical skills (max 30)
    t_score = min(30, len(tech_found) * 3)
    breakdown['Technical Skills'] = (t_score, 30)
    score += t_score

    # Soft skills (max 15)
    s_score = min(15, len(soft_found) * 3)
    breakdown['Soft Skills'] = (s_score, 15)
    score += s_score

    # Sections (max 20)
    sec_score = min(20, len(sections_found) * 3)
    breakdown['Resume Sections'] = (sec_score, 20)
    score += sec_score

    # Word count (max 10)
    if 250 <= words <= 700:
        w_score = 10
    elif words >= 150:
        w_score = 6
    elif words >= 80:
        w_score = 3
    else:
        w_score = 0
    breakdown['Content Length'] = (w_score, 10)
    score += w_score

    # Contact info (max 15)
    has_email    = bool(re.search(r'[\w\.\-\+]+@[\w\.\-]+\.\w{2,}', text))
    has_phone    = bool(re.search(r'(\+?\d[\d\s\-\(\)]{8,}\d)', text))
    has_linkedin = 'linkedin' in text_lower
    has_github   = 'github' in text_lower
    has_portfolio= any(x in text_lower for x in ['portfolio', 'website', 'www.', 'http'])

    c_score = 0
    if has_email:     c_score += 5
    if has_phone:     c_score += 4
    if has_linkedin:  c_score += 3
    if has_github:    c_score += 2
    if has_portfolio: c_score += 1
    c_score = min(15, c_score)
    breakdown['Contact Info'] = (c_score, 15)
    score += c_score

    # Action verbs (max 10)
    action_verbs = ['developed', 'designed', 'implemented', 'led', 'managed', 'created',
                    'built', 'optimized', 'improved', 'achieved', 'delivered', 'launched',
                    'increased', 'reduced', 'analyzed', 'collaborated', 'trained', 'mentored']
    verb_count = sum(1 for v in action_verbs if v in text_lower)
    a_score = min(10, verb_count * 2)
    breakdown['Action Verbs'] = (a_score, 10)
    score += a_score

    score = min(100, score)

    if score >= 85:   level, color = "🏆 EXCELLENT",          SUCCESS
    elif score >= 70: level, color = "🌟 VERY GOOD",           BLUE_MID
    elif score >= 50: level, color = "📈 GOOD — Keep Improving", WARNING
    elif score >= 30: level, color = "💪 AVERAGE — Needs Work",  GOLD
    else:             level, color = "🔴 NEEDS IMPROVEMENT",     DANGER

    # Job role matching
    user_skills = {k for k, _ in tech_found}
    role_matches = []
    for role, required in JOB_ROLES.items():
        match_count = len(user_skills & required)
        if match_count >= 2:
            pct = round((match_count / len(required)) * 100)
            role_matches.append((role, pct, match_count, len(required)))
    role_matches.sort(key=lambda x: x[1], reverse=True)

    suggestions = []
    if len(tech_found) < 5:
        suggestions.append("✨ Add more technical skills relevant to your target role.")
    if len(soft_found) < 3:
        suggestions.append("💫 Include soft skills: Communication, Leadership, Problem Solving.")
    missing_sec = [v for k, v in REQUIRED_SECTIONS.items() if k not in sections_found]
    if missing_sec:
        suggestions.append(f"📑 Missing sections: {', '.join(missing_sec[:4])}.")
    if words < 200:
        suggestions.append("📝 Expand content — aim for 250–600 words for best ATS score.")
    if not has_email:
        suggestions.append("📧 Add a professional email address.")
    if not has_phone:
        suggestions.append("📱 Add your phone number.")
    if not has_linkedin:
        suggestions.append("🔗 Add your LinkedIn profile URL.")
    if not has_github:
        suggestions.append("💻 Add your GitHub profile URL.")
    if verb_count < 4:
        suggestions.append("🚀 Use strong action verbs: Developed, Built, Designed, Optimized.")
    if not suggestions:
        suggestions.append("🎉 Great resume! Keep it updated with your latest projects.")

    return {
        'score': score, 'level': level, 'level_color': color,
        'tech_skills': tech_found, 'soft_skills': soft_found,
        'sections': sections_found, 'suggestions': suggestions,
        'word_count': words, 'breakdown': breakdown,
        'has_email': has_email, 'has_phone': has_phone,
        'has_linkedin': has_linkedin, 'has_github': has_github,
        'has_portfolio': has_portfolio, 'action_verbs': verb_count,
        'role_matches': role_matches[:5],
    }

# ─── SkillSpark Bot Q&A Database ──────────────────────────────────────────────
BOT_QA = {
    "📄 Resume Basics": [
        ("What is the ideal resume length?",
         "Keep it ONE page if you have under 10 years of experience. Two pages maximum for senior roles. Recruiters spend only 7–10 seconds scanning, so every word must earn its place. Remove filler phrases like 'responsible for' and replace with quantified achievements."),
        ("Which font is best for a resume?",
         "Best choices: Calibri (11pt), Georgia (10.5pt), Garamond (11pt), or Cambria (11pt). Use 14–16pt for your name, 12–13pt for section headings, 10–11pt for body text. Avoid decorative fonts — clarity beats creativity on a resume."),
        ("How to write a powerful professional summary?",
         "3 sentences maximum: (1) Your role + years of experience. (2) Your top 2–3 skills or technologies. (3) A key achievement with a number. Example: 'Full-stack developer with 3 years building scalable web apps in Python and React. Delivered 15+ projects on time. Reduced server costs by 40% through architecture optimisation.'"),
        ("Should I include a photo on my resume?",
         "In India and most Asian/European countries, a professional photo is acceptable. In the US, UK, and Canada, skip it to avoid unconscious bias. If you do include one, use a professional headshot with a plain background, not a selfie."),
        ("How far back should work experience go?",
         "10–15 years maximum. Older roles add clutter and date you. Exception: if an older role is highly prestigious or directly relevant. For freshers, include all internships, projects, and volunteer work."),
        ("How to explain employment gaps honestly?",
         "Be brief and direct. Label it: 'Career Break – Freelance Projects', 'Self-Study: Completed 3 online certifications', or 'Family Caregiving'. Never leave unexplained gaps — fill them with any skill-building activity."),
        ("What is the difference between CV and Resume?",
         "A Resume is 1–2 pages, tailored for a specific job, focused on skills and achievements. A CV (Curriculum Vitae) is comprehensive (3–10+ pages), used in academia and research, listing all publications, awards, and academic work. For most jobs, send a resume."),
        ("Should I include my GPA?",
         "Yes, if you're a recent graduate and your GPA is 7.5/10 or above (or 3.5/4.0). Remove it after 2–3 years of work experience. If your GPA is low, focus on projects, certifications, and skills instead."),
        ("How to list multiple roles at the same company?",
         "Write the company name once with the overall date range. Below it, list each role separately with its own date range and bullet points. This clearly shows career progression and promotions — a strong positive signal to recruiters."),
        ("What are action verbs and why do they matter?",
         "Action verbs start your bullet points with power. Instead of 'Was responsible for managing a team', write 'Led a team of 6 developers'. Strong verbs: Developed, Designed, Optimised, Delivered, Reduced, Increased, Launched, Automated, Collaborated, Mentored. Quantify whenever possible."),
    ],
    "🤖 ATS Optimization": [
        ("What is ATS and how does it work?",
         "ATS (Applicant Tracking System) is software that scans resumes before a human sees them. It parses your text for keywords from the job description, then ranks candidates. Over 75% of companies use ATS. If your resume isn't ATS-friendly, it gets filtered out automatically."),
        ("How to make my resume ATS-friendly?",
         "Use standard section headings (Experience, Education, Skills). Submit as .docx or text-based .pdf. No tables, columns, graphics, or text boxes — ATS cannot read them. Use keywords directly from the job description. Include both abbreviations and full forms (e.g., 'ML / Machine Learning')."),
        ("What formatting kills ATS parsing?",
         "These break ATS parsing: multi-column layouts, text inside tables, headers and footers, text boxes, images or logos, fancy dividers, special characters in headings, and non-standard fonts. Use clean single-column layout with standard bullet points."),
        ("How to find the right keywords for a job?",
         "Copy the job description into a word cloud tool or read it carefully. Identify skills, tools, technologies, and role-specific phrases. Use those exact words in your resume naturally. For example if the JD says 'REST APIs', use that exact phrase, not just 'API development'."),
        ("Is PDF or Word document better for submission?",
         "Use .docx for most applications — older ATS systems parse it more reliably. Use text-based PDF (not scanned) for companies that prefer it. Never submit a scanned PDF — ATS cannot extract text from images."),
        ("What is keyword density and does it matter?",
         "Don't stuff keywords unnaturally — ATS systems detect that too. Aim to include each important keyword 1–3 times across your resume. The goal is natural integration: in your skills section, summary, and relevant bullet points."),
    ],
    "💌 Cover Letters": [
        ("Do I always need a cover letter?",
         "Write one unless the job application specifically says 'no cover letter needed'. A tailored cover letter increases your chances by up to 50% — most candidates skip it, so it instantly differentiates you. Keep it to one page, 3–4 paragraphs."),
        ("What is the ideal cover letter structure?",
         "Paragraph 1: Hook — why this specific company excites you. Paragraph 2: Your top 2 relevant achievements with numbers. Paragraph 3: How your skills directly solve their stated needs. Paragraph 4: Clear call to action — request an interview. Sign off professionally."),
        ("How to start a cover letter if I don't know the hiring manager's name?",
         "Try to find the name on LinkedIn or the company website first — personalisation matters. If you cannot find it, use: 'Dear Hiring Manager' or 'Dear [Department] Team'. Avoid 'To Whom It May Concern' — it sounds outdated."),
        ("How to customise a cover letter for each job?",
         "Change three things for every application: (1) Company name and why you want to work there specifically. (2) The exact role title from the job description. (3) Reference 1–2 specific requirements from their JD and connect them to your experience. This takes 10 minutes and doubles your response rate."),
        ("What are the biggest cover letter mistakes?",
         "1) Starting with 'I am writing to apply for...' — boring opener. 2) Repeating your resume word for word. 3) Focusing on what the job gives you, not what you bring. 4) Generic letters with no company-specific content. 5) Exceeding one page. 6) Spelling or grammar errors."),
    ],
    "🎤 Interview Prep": [
        ("How to answer 'Tell me about yourself'?",
         "Use the Present–Past–Future formula: Start with your current role (30 sec), mention 1–2 relevant past achievements (30 sec), then connect to why you're excited about this opportunity (30 sec). Total: 90 seconds maximum. Practise until it sounds natural, not memorised."),
        ("How to answer 'What are your strengths'?",
         "Give 2–3 strengths that are directly relevant to the role. Back each with a specific example. Example: 'My strongest skill is problem-solving. In my last project, I identified a database bottleneck that was slowing response times by 3 seconds — I optimised the queries and brought it down to 200ms.'"),
        ("How to answer 'What are your weaknesses'?",
         "Choose a real weakness that isn't a core job requirement, then show what you're actively doing to improve. Example: 'I used to struggle with public speaking. I joined a weekly presentation club at college and now lead technical demos for our team. I'm still working on it but I've improved significantly.'"),
        ("How to answer 'Why do you want to work here'?",
         "Research the company before the interview. Mention something specific: a product you admire, a company value that resonates, a recent achievement. Then connect their needs to your skills. Generic 'It's a great company' answers immediately reduce your chances."),
        ("What is the STAR method for interview answers?",
         "STAR stands for: Situation (context/background), Task (your responsibility), Action (what you specifically did), Result (measurable outcome). Use this for any 'Tell me about a time when...' question. Always end with a quantified result: 'reduced errors by 25%', 'delivered 2 weeks ahead of schedule'."),
        ("How to handle a question you don't know the answer to?",
         "Never fake an answer. Say: 'That's a great question. I haven't worked with that specific technology, but here's how I'd approach learning it...' or 'I don't have that data off the top of my head, but I can walk you through how I'd find and analyse it.' Honesty + problem-solving mindset impresses more than bluffing."),
        ("How to prepare for technical interviews?",
         "Practice data structures and algorithms on LeetCode or HackerRank (Easy to Medium level first). Review system design basics for senior roles. Know your projects deeply — expect detailed questions on any technology you've listed. Prepare 3–5 strong project stories using STAR format."),
        ("What questions should I ask the interviewer?",
         "Always prepare 3–4 questions: 'What does success look like in the first 90 days?' / 'What are the biggest technical challenges the team is facing?' / 'How does the team handle code reviews and learning?' / 'What does growth look like for this role?' Never ask about salary in the first interview."),
    ],
    "🔧 Skill Building": [
        ("What are the most in-demand technical skills in 2024?",
         "Top technical skills: Python, SQL, JavaScript/TypeScript, React, AWS/Cloud, Docker & Kubernetes, Machine Learning basics, REST API development, Git, and Data Analysis. For non-tech roles: Excel/Power BI, project management tools, and CRM software. Combine 2–3 of these with domain knowledge for maximum employability."),
        ("How to learn new skills fast for a job application?",
         "Use the 80/20 rule: 20% of any skill gets you 80% of the work done. For programming: build one real project instead of completing 10 courses. For tools: find the company's specific use case and practice that. A functional GitHub project demonstrates more than a certificate."),
        ("Should I get certifications, and which ones?",
         "Yes — certifications add credibility and pass ATS filters. High-value ones: AWS Certified Solutions Architect, Google Data Analytics Certificate, Meta Front-End Developer Certificate, Microsoft Azure Fundamentals, PMP (for managers), Cisco CCNA (for networking). Always add them to your resume with issue date."),
        ("How to showcase projects on a resume?",
         "Each project entry should have: Project name, the tech stack used, your specific role, and a quantified outcome. Example: 'E-Commerce Website | React, Node.js, MongoDB | Built full-stack app with 500+ products, integrated Razorpay payment gateway, deployed on AWS EC2.' Add a GitHub link always."),
        ("How to build a portfolio with no work experience?",
         "1) Build 3–5 original projects solving real problems. 2) Contribute to open source on GitHub. 3) Participate in hackathons. 4) Write technical articles on Medium or Dev.to. 5) Create a personal portfolio website. Quality of 3 strong projects beats quantity of 10 incomplete ones."),
    ],
    "🔍 Job Search & Networking": [
        ("Where are the best places to find jobs in India?",
         "LinkedIn (best for tech/corporate), Naukri.com (largest Indian job board), Internshala (internships + fresher roles), AngelList/Wellfound (startups), Indeed India, company career pages directly, and alumni networks from your college. For government jobs: sarkariresult.com. Always apply directly on company websites too."),
        ("How to use LinkedIn effectively for job searching?",
         "Complete your profile to 100% (All-Star status gets 40x more views). Add a professional photo — profiles with photos get 21x more views. Write a compelling 'About' section using keywords. Post or share content in your field weekly. Connect with recruiters and send personalised notes, not default connection requests."),
        ("How to ask for a referral professionally?",
         "Step 1: Connect and build rapport first — comment on their posts, share common ground. Step 2: Ask for a 15-minute informational chat, not a referral directly. Step 3: After the chat, if it went well, ask: 'Would you be comfortable referring me for the [role] opening at your company?' Make it easy — send them your resume and the exact job link."),
        ("How to follow up after a job application?",
         "Wait 5–7 business days after applying. Send a brief email to the hiring manager or HR contact: 'I applied for [Role] on [Date] and wanted to express my continued interest. I'm confident my [specific skill] aligns well with your team's needs. I'd welcome the opportunity to discuss further.' Keep it under 100 words."),
        ("What is the best time to apply for jobs?",
         "Tuesday through Thursday mornings (9–11 AM) have the highest response rates. Apply within the first 48 hours of a job posting — many companies review applications on a rolling basis and early applicants get more attention. Set up job alerts on LinkedIn and Naukri to be notified instantly."),
        ("How to negotiate salary confidently?",
         "Research market rates on Glassdoor, AmbitionBox, and LinkedIn Salary before negotiating. Never give a number first — ask 'What is the budgeted range for this role?' When you do negotiate: 'Based on my research and experience, I was expecting a range of X–Y. Is there flexibility?' Always negotiate — 70% of employers expect it."),
    ],
    "🎓 Freshers Guide": [
        ("How to write a resume with no work experience?",
         "Sections to include: Education (with relevant coursework), Technical Skills, Projects (3–5 strong ones), Internships (even 1–2 months counts), Certifications, Achievements & Competitions, and Extra-curriculars showing leadership. Lead with a strong objective statement. Your projects ARE your experience — describe them in detail."),
        ("What do companies look for in fresh graduates?",
         "Ranked in order: (1) Technical fundamentals in your domain. (2) Problem-solving approach — can you think through a challenge? (3) Communication skills — can you explain your work clearly? (4) Learning attitude — are you curious and coachable? (5) Cultural fit. You don't need to know everything, but show eagerness to learn."),
        ("How to prepare for campus placements?",
         "Start 6 months early: (1) Practice aptitude tests — Quantitative, Logical, and Verbal. (2) Learn DSA basics for tech companies. (3) Prepare 3–5 strong project stories. (4) Research every company before their drive. (5) Mock interviews with friends. (6) Keep your CGPA above the cutoff. First placement is stepping stone — don't be too selective."),
        ("Should I do internships during college?",
         "Absolutely yes — even unpaid or remote internships. Internship experience differentiates you from 90% of freshers. Start from 2nd year. Platforms: Internshala, LinkedIn, LetsIntern, company career pages, college placement cell. Convert every internship into a measurable bullet point on your resume."),
        ("How to write a fresher objective statement?",
         "Formula: 'Motivated [your field] graduate from [college] with strong skills in [2–3 skills]. Seeking a [role] position at a [type of company] to apply and grow my expertise in [specific area].' Keep it to 2 sentences. Customise for every application — mention the company name if possible."),
    ],
}

# ─── PDF Export ───────────────────────────────────────────────────────────────
def export_to_pdf(result, filename, output_path):
    if not PDF_EXPORT_OK:
        return False, "reportlab not installed. Run: pip install reportlab"
    try:
        doc = SimpleDocTemplate(output_path, pagesize=A4,
                                leftMargin=2*cm, rightMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=20,
                                     textColor=colors.HexColor(BLUE_DARK),
                                     alignment=TA_CENTER, spaceAfter=6)
        sub_style   = ParagraphStyle('Sub', fontName='Helvetica', fontSize=10,
                                     textColor=colors.HexColor(TEXT_LIGHT),
                                     alignment=TA_CENTER, spaceAfter=4)
        heading_style = ParagraphStyle('Heading', fontName='Helvetica-Bold', fontSize=13,
                                       textColor=colors.HexColor(BLUE_DARK),
                                       spaceBefore=12, spaceAfter=4)
        body_style  = ParagraphStyle('Body', fontName='Helvetica', fontSize=10,
                                     textColor=colors.HexColor(TEXT_DARK),
                                     leading=16, spaceAfter=3)
        bullet_style = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=10,
                                      textColor=colors.HexColor(TEXT_MID),
                                      leftIndent=14, leading=15, spaceAfter=2)

        story.append(Paragraph("✨ SkillSpark Resume Analysis Report", title_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", sub_style))
        story.append(Paragraph(f"File: {filename}", sub_style))
        story.append(HRFlowable(width="100%", thickness=2,
                                 color=colors.HexColor(BLUE_MID), spaceAfter=12))

        # Score
        score_color = colors.HexColor(SUCCESS) if result['score'] >= 70 else \
                      colors.HexColor(WARNING) if result['score'] >= 40 else \
                      colors.HexColor(DANGER)
        score_style = ParagraphStyle('Score', fontName='Helvetica-Bold', fontSize=32,
                                     textColor=score_color, alignment=TA_CENTER, spaceAfter=4)
        story.append(Paragraph(f"{result['score']}/100", score_style))
        story.append(Paragraph(result['level'], ParagraphStyle('Level', fontName='Helvetica-Bold',
                                fontSize=14, textColor=score_color, alignment=TA_CENTER, spaceAfter=12)))

        # Score breakdown table
        story.append(Paragraph("Score Breakdown", heading_style))
        table_data = [['Category', 'Score', 'Max']]
        for cat, (got, mx) in result['breakdown'].items():
            table_data.append([cat, str(got), str(mx)])
        t = Table(table_data, colWidths=[10*cm, 3*cm, 3*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor(BLUE_DARK)),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,-1), 10),
            ('ROWBACKGROUNDS', (0,1), (-1,-1),
             [colors.HexColor('#EEF2FB'), colors.HexColor('#FFFFFF')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor(BORDER)),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t)
        story.append(Spacer(1, 12))

        # Technical Skills
        if result['tech_skills']:
            story.append(Paragraph("Technical Skills Detected", heading_style))
            story.append(HRFlowable(width="100%", thickness=1,
                                     color=colors.HexColor(BORDER), spaceAfter=6))
            for _, display in result['tech_skills']:
                story.append(Paragraph(f"• {display}", bullet_style))
            story.append(Spacer(1, 6))

        # Soft Skills
        if result['soft_skills']:
            story.append(Paragraph("Soft Skills Detected", heading_style))
            story.append(HRFlowable(width="100%", thickness=1,
                                     color=colors.HexColor(BORDER), spaceAfter=6))
            for _, display in result['soft_skills']:
                story.append(Paragraph(f"• {display}", bullet_style))
            story.append(Spacer(1, 6))

        # Job Role Matches
        if result['role_matches']:
            story.append(Paragraph("Top Job Role Matches", heading_style))
            story.append(HRFlowable(width="100%", thickness=1,
                                     color=colors.HexColor(BORDER), spaceAfter=6))
            for role, pct, matched, total in result['role_matches']:
                story.append(Paragraph(
                    f"• {role} — {pct}% match ({matched}/{total} skills found)", bullet_style))
            story.append(Spacer(1, 6))

        # Suggestions
        story.append(Paragraph("Improvement Suggestions", heading_style))
        story.append(HRFlowable(width="100%", thickness=1,
                                 color=colors.HexColor(BORDER), spaceAfter=6))
        for s in result['suggestions']:
            story.append(Paragraph(f"• {s}", bullet_style))

        story.append(Spacer(1, 16))
        story.append(HRFlowable(width="100%", thickness=1,
                                 color=colors.HexColor(BORDER), spaceAfter=6))
        story.append(Paragraph("Generated by SkillSpark Pro — AI Resume Analyzer",
                                ParagraphStyle('Footer', fontName='Helvetica', fontSize=9,
                                               textColor=colors.HexColor(TEXT_LIGHT),
                                               alignment=TA_CENTER)))

        doc.build(story)
        return True, output_path
    except Exception as e:
        return False, str(e)

# ─── Main Application ─────────────────────────────────────────────────────────
class SkillSparkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ SkillSpark Pro — AI Resume Analyzer")
        self.root.geometry("1440x860")
        self.root.configure(bg=BG_LIGHT)
        self.root.minsize(1100, 700)

        self.current_text     = ""
        self.current_filename = ""
        self.last_result      = None
        self.notebook         = None
        self.current_qa       = []

        self._setup_styles()
        self._build_ui()
        self._center_window()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TNotebook', background=BG_WHITE, borderwidth=0)
        style.configure('TNotebook.Tab', background=BG_PANEL, foreground=TEXT_MID,
                        padding=[16, 8], font=('Segoe UI', 10, 'bold'), borderwidth=0)
        style.map('TNotebook.Tab',
                  background=[('selected', BLUE_MID)],
                  foreground=[('selected', BG_WHITE)])

        style.configure('Blue.TCombobox', fieldbackground=BG_WHITE,
                        background=BG_WHITE, foreground=TEXT_DARK,
                        selectbackground=BLUE_LIGHT, selectforeground=TEXT_DARK)

        style.configure('TScrollbar', background=BG_PANEL,
                        troughcolor=BG_LIGHT, borderwidth=0, arrowsize=12)

    def _center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth()  // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f'+{x}+{y}')

    def _build_ui(self):
        # ── Header ─────────────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg=BLUE_DARK, height=72)
        header.pack(fill='x')
        header.pack_propagate(False)

        logo_frame = tk.Frame(header, bg=BLUE_DARK)
        logo_frame.pack(side='left', padx=24, pady=12)
        tk.Label(logo_frame, text="✨ SkillSpark Pro",
                 font=('Segoe UI', 22, 'bold'), bg=BLUE_DARK, fg=BG_WHITE).pack(side='left')
        tk.Label(logo_frame, text="  AI Resume Analyzer",
                 font=('Segoe UI', 11), bg=BLUE_DARK, fg='#93C5FD').pack(side='left', pady=4)

        # PDF badge
        badge_text = "📄 PDF Supported" if PDF_READ_OK else "📄 TXT Only (install pypdf)"
        badge_color = '#86EFAC' if PDF_READ_OK else '#FCA5A5'
        tk.Label(header, text=badge_text, font=('Segoe UI', 9, 'bold'),
                 bg=BLUE_DARK, fg=badge_color).pack(side='right', padx=24)

        # ── Main Body ──────────────────────────────────────────────────────────
        body = tk.Frame(self.root, bg=BG_LIGHT)
        body.pack(fill='both', expand=True)

        # Left Panel
        left_outer = tk.Frame(body, bg=BG_LIGHT)
        left_outer.pack(side='left', fill='both', expand=True, padx=(16, 8), pady=16)

        self.notebook = ttk.Notebook(left_outer)
        self.notebook.pack(fill='both', expand=True)

        upload_tab  = tk.Frame(self.notebook, bg=BG_WHITE)
        paste_tab   = tk.Frame(self.notebook, bg=BG_WHITE)
        results_tab = tk.Frame(self.notebook, bg=BG_WHITE)

        self.notebook.add(upload_tab,  text="  📁  Upload Resume  ")
        self.notebook.add(paste_tab,   text="  📝  Paste Text  ")
        self.notebook.add(results_tab, text="  📊  Results  ")

        self._build_upload_tab(upload_tab)
        self._build_paste_tab(paste_tab)
        self._build_results_tab(results_tab)

        # Divider
        tk.Frame(body, bg=BORDER, width=1).pack(side='left', fill='y', pady=16)

        # Right Panel
        right_outer = tk.Frame(body, bg=BG_LIGHT)
        right_outer.pack(side='right', fill='both', expand=True, padx=(8, 16), pady=16)
        self._build_bot_panel(right_outer)

        # ── Status Bar ─────────────────────────────────────────────────────────
        statusbar = tk.Frame(self.root, bg=BLUE_DARK, height=28)
        statusbar.pack(fill='x', side='bottom')
        statusbar.pack_propagate(False)
        self.status_var = tk.StringVar(value="✅  Ready — Upload or paste your resume to begin analysis.")
        tk.Label(statusbar, textvariable=self.status_var, bg=BLUE_DARK,
                 fg='#93C5FD', font=('Segoe UI', 9), anchor='w').pack(
                 side='left', padx=16, pady=4)
        tk.Label(statusbar, text="SkillSpark Pro v2.0",
                 bg=BLUE_DARK, fg='#475569', font=('Segoe UI', 8)).pack(
                 side='right', padx=16)

    # ── Upload Tab ─────────────────────────────────────────────────────────────
    def _build_upload_tab(self, parent):
        f = tk.Frame(parent, bg=BG_WHITE)
        f.pack(fill='both', expand=True, padx=30, pady=30)

        tk.Label(f, text="Upload Your Resume",
                 font=('Segoe UI', 16, 'bold'), bg=BG_WHITE, fg=BLUE_DARK).pack(anchor='w')
        tk.Label(f, text="Supports PDF and TXT file formats",
                 font=('Segoe UI', 10), bg=BG_WHITE, fg=TEXT_LIGHT).pack(anchor='w', pady=(2,20))

        # Drop zone (simulated)
        zone = tk.Frame(f, bg=BLUE_LIGHT, relief='flat', bd=0)
        zone.pack(fill='x', pady=(0,20), ipady=30)
        tk.Label(zone, text="📄", font=('Segoe UI', 36), bg=BLUE_LIGHT).pack(pady=(10,4))
        tk.Label(zone, text="Click the button below to select your resume",
                 font=('Segoe UI', 11), bg=BLUE_LIGHT, fg=BLUE_DARK).pack()
        tk.Label(zone, text="PDF or TXT accepted",
                 font=('Segoe UI', 9), bg=BLUE_LIGHT, fg=TEXT_LIGHT).pack(pady=(2,10))

        self.upload_btn = tk.Button(f, text="  🔍  Choose File  ",
                                    command=self._upload,
                                    bg=BLUE_MID, fg=BG_WHITE,
                                    font=('Segoe UI', 11, 'bold'),
                                    relief='flat', cursor='hand2',
                                    padx=20, pady=10, activebackground=BLUE_DARK,
                                    activeforeground=BG_WHITE)
        self.upload_btn.pack(pady=(0, 14))

        self.file_label = tk.Label(f, text="No file selected",
                                   font=('Segoe UI', 10), bg=BG_WHITE, fg=TEXT_LIGHT)
        self.file_label.pack()

    # ── Paste Tab ──────────────────────────────────────────────────────────────
    def _build_paste_tab(self, parent):
        f = tk.Frame(parent, bg=BG_WHITE)
        f.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(f, text="Paste Resume Text",
                 font=('Segoe UI', 14, 'bold'), bg=BG_WHITE, fg=BLUE_DARK).pack(anchor='w')
        tk.Label(f, text="Copy and paste your resume content below",
                 font=('Segoe UI', 9), bg=BG_WHITE, fg=TEXT_LIGHT).pack(anchor='w', pady=(2,10))

        self.paste_area = scrolledtext.ScrolledText(f, wrap=tk.WORD,
                                                    bg=BG_PANEL, fg=TEXT_DARK,
                                                    font=('Consolas', 10),
                                                    relief='flat', bd=0,
                                                    insertbackground=BLUE_MID,
                                                    padx=12, pady=10)
        self.paste_area.pack(fill='both', expand=True)
        self.paste_area.insert(tk.END, "Paste your resume text here...\n\nInclude sections like:\n• Contact Information\n• Professional Summary\n• Work Experience\n• Education\n• Skills\n• Projects\n• Certifications")
        self.paste_area.bind('<FocusIn>', self._clear_placeholder)

        btn_frame = tk.Frame(f, bg=BG_WHITE)
        btn_frame.pack(fill='x', pady=(12, 0))

        tk.Button(btn_frame, text="  🚀  Analyze Resume  ",
                  command=self._analyze_pasted,
                  bg=SUCCESS, fg=BG_WHITE, font=('Segoe UI', 11, 'bold'),
                  relief='flat', cursor='hand2', padx=16, pady=8,
                  activebackground='#15803D', activeforeground=BG_WHITE).pack(side='left', padx=(0,8))

        tk.Button(btn_frame, text="  🗑️  Clear  ",
                  command=self._clear_paste,
                  bg=BG_PANEL, fg=TEXT_MID, font=('Segoe UI', 10),
                  relief='flat', cursor='hand2', padx=12, pady=8).pack(side='left')

    def _clear_placeholder(self, event):
        content = self.paste_area.get(1.0, tk.END).strip()
        if content.startswith("Paste your resume text here"):
            self.paste_area.delete(1.0, tk.END)

    def _clear_paste(self):
        self.paste_area.delete(1.0, tk.END)
        self.paste_area.insert(tk.END, "Paste your resume text here...\n\nInclude sections like:\n• Contact Information\n• Professional Summary\n• Work Experience\n• Education\n• Skills\n• Projects\n• Certifications")

    # ── Results Tab ────────────────────────────────────────────────────────────
    def _build_results_tab(self, parent):
        f = tk.Frame(parent, bg=BG_WHITE)
        f.pack(fill='both', expand=True, padx=0, pady=0)

        # Score canvas (top bar)
        self.score_canvas = tk.Canvas(f, height=120, bg=BLUE_DARK, highlightthickness=0)
        self.score_canvas.pack(fill='x')
        self._draw_score_placeholder()

        # Results scrollable text
        self.results_text = scrolledtext.ScrolledText(f, wrap=tk.WORD,
                                                      bg=BG_WHITE, fg=TEXT_DARK,
                                                      font=('Consolas', 10),
                                                      relief='flat', bd=0,
                                                      padx=20, pady=15)
        self.results_text.pack(fill='both', expand=True)
        self.results_text.insert(tk.END,
            "📊  Your analysis results will appear here after uploading or pasting your resume.\n\n"
            "The report will include:\n"
            "  • Overall score out of 100\n"
            "  • Score breakdown by category\n"
            "  • Detected technical and soft skills\n"
            "  • Matched job roles\n"
            "  • Personalised improvement suggestions\n"
        )
        self.results_text.config(state='disabled')

        # Bottom buttons
        btn_bar = tk.Frame(f, bg=BG_PANEL)
        btn_bar.pack(fill='x', padx=0, pady=0)

        tk.Button(btn_bar, text="📋  Copy Report",
                  command=self._copy_results,
                  bg=BLUE_MID, fg=BG_WHITE, font=('Segoe UI', 10, 'bold'),
                  relief='flat', cursor='hand2', padx=16, pady=7,
                  activebackground=BLUE_DARK).pack(side='left', padx=12, pady=8)

        export_color = SUCCESS if PDF_EXPORT_OK else '#94A3B8'
        export_text  = "📄  Export as PDF" if PDF_EXPORT_OK else "📄  Export (install reportlab)"
        tk.Button(btn_bar, text=export_text,
                  command=self._export_pdf,
                  bg=export_color, fg=BG_WHITE, font=('Segoe UI', 10, 'bold'),
                  relief='flat', cursor='hand2', padx=16, pady=7).pack(side='left', padx=4, pady=8)

    def _draw_score_placeholder(self):
        self.score_canvas.delete('all')
        self.score_canvas.create_text(
            400, 60, text="Upload or paste your resume to see your score",
            font=('Segoe UI', 12), fill='#93C5FD')

    def _draw_score_banner(self, result):
        self.score_canvas.delete('all')
        c = self.score_canvas
        w = c.winfo_width() or 700

        score = result['score']
        bar_w = int((score / 100) * (w - 40))
        c.create_rectangle(20, 80, w-20, 96, fill='#1E3A5F', outline='')
        bar_color = SUCCESS if score >= 70 else WARNING if score >= 40 else DANGER
        c.create_rectangle(20, 80, 20+bar_w, 96, fill=bar_color, outline='')

        c.create_text(w//2, 26, text=f"{score}/100",
                      font=('Segoe UI', 30, 'bold'), fill=BG_WHITE)
        c.create_text(w//2, 60, text=result['level'],
                      font=('Segoe UI', 12, 'bold'), fill='#93C5FD')

    # ── Bot Panel ──────────────────────────────────────────────────────────────
    def _build_bot_panel(self, parent):
        card = tk.Frame(parent, bg=BG_WHITE, relief='flat')
        card.pack(fill='both', expand=True)

        # Bot header
        bot_header = tk.Frame(card, bg=BLUE_DARK, height=52)
        bot_header.pack(fill='x')
        bot_header.pack_propagate(False)
        tk.Label(bot_header, text="🤖  SkillSpark Bot",
                 font=('Segoe UI', 14, 'bold'), bg=BLUE_DARK, fg=BG_WHITE).pack(
                 side='left', padx=16, pady=12)
        tk.Label(bot_header, text="Career Q&A Assistant",
                 font=('Segoe UI', 9), bg=BLUE_DARK, fg='#93C5FD').pack(
                 side='left', pady=14)

        body = tk.Frame(card, bg=BG_WHITE)
        body.pack(fill='both', expand=True, padx=16, pady=12)

        # Search bar
        search_frame = tk.Frame(body, bg=BG_PANEL, relief='flat')
        search_frame.pack(fill='x', pady=(0, 10))
        tk.Label(search_frame, text="🔍", bg=BG_PANEL, font=('Segoe UI', 11)).pack(
            side='left', padx=(8, 4), pady=6)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                     bg=BG_PANEL, fg=TEXT_DARK,
                                     font=('Segoe UI', 10), relief='flat',
                                     insertbackground=BLUE_MID)
        self.search_entry.pack(side='left', fill='x', expand=True, pady=6)
        self.search_entry.insert(0, "Search questions...")
        self.search_entry.bind('<FocusIn>',  self._search_focus_in)
        self.search_entry.bind('<FocusOut>', self._search_focus_out)
        self.search_var.trace('w', self._filter_questions)

        # Category
        cat_frame = tk.Frame(body, bg=BG_WHITE)
        cat_frame.pack(fill='x', pady=(0, 8))
        tk.Label(cat_frame, text="Category:", font=('Segoe UI', 10, 'bold'),
                 bg=BG_WHITE, fg=TEXT_MID).pack(side='left', padx=(0, 8))
        self.cat_var = tk.StringVar()
        categories = list(BOT_QA.keys())
        self.cat_combo = ttk.Combobox(cat_frame, textvariable=self.cat_var,
                                      values=categories, state='readonly',
                                      width=36, style='Blue.TCombobox')
        self.cat_combo.pack(side='left')
        self.cat_combo.bind('<<ComboboxSelected>>', self._load_questions)
        if categories:
            self.cat_combo.set(categories[0])

        # Question listbox
        tk.Label(body, text="Questions  (click to get answer)",
                 font=('Segoe UI', 9), bg=BG_WHITE, fg=TEXT_LIGHT).pack(anchor='w', pady=(4, 2))

        q_frame = tk.Frame(body, bg=BG_WHITE)
        q_frame.pack(fill='both', expand=True)
        q_scroll = ttk.Scrollbar(q_frame)
        q_scroll.pack(side='right', fill='y')
        self.q_listbox = tk.Listbox(q_frame, yscrollcommand=q_scroll.set,
                                    bg=BG_PANEL, fg=TEXT_DARK,
                                    selectbackground=BLUE_MID,
                                    selectforeground=BG_WHITE,
                                    font=('Segoe UI', 10),
                                    relief='flat', bd=0,
                                    activestyle='none',
                                    highlightthickness=0,
                                    height=9)
        self.q_listbox.pack(side='left', fill='both', expand=True)
        q_scroll.config(command=self.q_listbox.yview)
        self.q_listbox.bind('<<ListboxSelect>>', self._show_answer)

        # Answer box
        tk.Label(body, text="💡  Answer",
                 font=('Segoe UI', 10, 'bold'), bg=BG_WHITE, fg=BLUE_DARK).pack(
                 anchor='w', pady=(10, 4))
        self.answer_text = scrolledtext.ScrolledText(body, wrap=tk.WORD,
                                                     bg=BG_PANEL, fg=TEXT_DARK,
                                                     font=('Segoe UI', 10),
                                                     relief='flat', bd=0,
                                                     padx=12, pady=10, height=8)
        self.answer_text.pack(fill='both', expand=True)
        self.answer_text.insert(tk.END, "👆  Select a question above to see the answer here.")
        self.answer_text.config(state='disabled')

        self._load_questions()

    def _search_focus_in(self, event):
        if self.search_entry.get() == "Search questions...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=TEXT_DARK)

    def _search_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search questions...")
            self.search_entry.config(fg=TEXT_LIGHT)

    def _filter_questions(self, *args):
        query = self.search_var.get().lower().strip()
        if not query or query == "search questions...":
            self._load_questions()
            return
        self.q_listbox.delete(0, tk.END)
        self.current_qa = []
        for cat_qa in BOT_QA.values():
            for q, a in cat_qa:
                if query in q.lower() or query in a.lower():
                    self.q_listbox.insert(tk.END, f"  {q}")
                    self.current_qa.append((q, a))

    def _load_questions(self, event=None):
        cat = self.cat_var.get()
        if not cat:
            return
        self.q_listbox.delete(0, tk.END)
        self.current_qa = BOT_QA.get(cat, [])
        for q, _ in self.current_qa:
            self.q_listbox.insert(tk.END, f"  {q}")

    def _show_answer(self, event):
        sel = self.q_listbox.curselection()
        if not sel:
            return
        _, answer = self.current_qa[sel[0]]
        self.answer_text.config(state='normal')
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, answer)
        self.answer_text.config(state='disabled')

    # ── Core Analysis ──────────────────────────────────────────────────────────
    def _upload(self):
        path = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=[("Resume files", "*.pdf *.txt"), ("PDF files", "*.pdf"),
                       ("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        self.current_filename = os.path.basename(path)
        self.file_label.config(text=f"📄  {self.current_filename}", fg=BLUE_MID)
        ext = os.path.splitext(path)[1].lower()
        text = None

        if ext == '.txt':
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                    text = fh.read()
            except Exception as e:
                messagebox.showerror("File Error", f"Cannot read TXT file:\n{e}")
                return

        elif ext == '.pdf':
            if not PDF_READ_OK:
                messagebox.showerror("Missing Library",
                    "PDF reading requires pypdf.\n\nInstall it:\n  pip install pypdf\n\nOr paste your resume text in the 'Paste Text' tab.")
                return
            try:
                try:
                    reader = PdfReader(path)
                    text = "".join(page.extract_text() or "" for page in reader.pages)
                except NameError:
                    import PyPDF2
                    with open(path, 'rb') as fh:
                        reader = PyPDF2.PdfReader(fh)
                        text = "".join(p.extract_text() or "" for p in reader.pages)
            except Exception as e:
                messagebox.showerror("PDF Error", f"Could not read PDF:\n{e}\n\nTry the 'Paste Text' tab instead.")
                return
        else:
            messagebox.showerror("Format Error", "Please select a PDF or TXT file.")
            return

        if not text or not text.strip():
            messagebox.showerror("Empty File", "No readable text found in this file.\nTry the 'Paste Text' tab.")
            return

        self.current_text = text
        self._run_analysis()

    def _analyze_pasted(self):
        text = self.paste_area.get(1.0, tk.END).strip()
        if not text or text.startswith("Paste your resume text here"):
            messagebox.showwarning("No Content", "Please paste your resume text first.")
            return
        self.current_text = text
        self.current_filename = "Pasted Resume Text"
        self._run_analysis()

    def _run_analysis(self):
        self.status_var.set("⏳  Analyzing resume...")
        self.root.update()

        result = analyze_resume(self.current_text)
        self.last_result = result

        # Build text report
        bars = {cat: '#' * got + '-' * (mx - got) for cat, (got, mx) in result['breakdown'].items()}

        tech_str = '\n'.join(f"  • {d}" for _, d in result['tech_skills']) if result['tech_skills'] else "  None detected"
        soft_str = '\n'.join(f"  • {d}" for _, d in result['soft_skills']) if result['soft_skills'] else "  None detected"
        sec_str  = ', '.join(result['sections'].values()) if result['sections'] else "None"
        sugg_str = '\n'.join(f"  {s}" for s in result['suggestions'])
        role_str = '\n'.join(f"  {i+1}. {r}  —  {p}% match  ({m}/{t} skills)"
                             for i, (r, p, m, t) in enumerate(result['role_matches'])) \
                   if result['role_matches'] else "  Add more technical skills to see role matches."

        bdown_str = '\n'.join(
            f"  {cat:<22} {got:>2}/{mx}  [{bars[cat]}]"
            for cat, (got, mx) in result['breakdown'].items())

        contact_str = (f"  Email:     {'✅' if result['has_email'] else '❌'}\n"
                       f"  Phone:     {'✅' if result['has_phone'] else '❌'}\n"
                       f"  LinkedIn:  {'✅' if result['has_linkedin'] else '❌'}\n"
                       f"  GitHub:    {'✅' if result['has_github'] else '❌'}\n"
                       f"  Portfolio: {'✅' if result['has_portfolio'] else '❌'}")

        divider = "─" * 58
        report = f"""
{divider}
  ✨  SKILLSPARK PRO — RESUME ANALYSIS REPORT
{divider}
  File     : {self.current_filename}
  Analyzed : {datetime.now().strftime('%d %B %Y  %I:%M %p')}
  Words    : {result['word_count']}
{divider}

  OVERALL SCORE :  {result['score']} / 100
  RATING        :  {result['level']}

{divider}
  SCORE BREAKDOWN
{divider}
{bdown_str}

{divider}
  CONTACT INFORMATION
{divider}
{contact_str}

{divider}
  TECHNICAL SKILLS  ({len(result['tech_skills'])} detected)
{divider}
{tech_str}

{divider}
  SOFT SKILLS  ({len(result['soft_skills'])} detected)
{divider}
{soft_str}

{divider}
  RESUME SECTIONS FOUND
{divider}
  {sec_str}

{divider}
  TOP JOB ROLE MATCHES
{divider}
{role_str}

{divider}
  IMPROVEMENT SUGGESTIONS
{divider}
{sugg_str}

{divider}
  Generated by SkillSpark Pro v2.0
{divider}
"""
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, report)
        self.results_text.config(state='disabled')

        # Update score banner after tab is shown
        self.notebook.select(2)
        self.root.after(50, lambda: self._draw_score_banner(result))

        self.status_var.set(
            f"✅  Analysis complete — Score: {result['score']}/100  |  "
            f"{len(result['tech_skills'])} tech skills  |  "
            f"{len(result['role_matches'])} role matches  |  "
            f"Words: {result['word_count']}")

    def _copy_results(self):
        content = self.results_text.get("1.0", tk.END).strip()
        if not content or "will appear here" in content:
            messagebox.showwarning("Nothing to Copy", "Run an analysis first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.status_var.set("📋  Report copied to clipboard!")

    def _export_pdf(self):
        if not PDF_EXPORT_OK:
            messagebox.showerror("Missing Library",
                "PDF export requires reportlab.\n\nInstall it:\n  pip install reportlab")
            return
        if not self.last_result:
            messagebox.showwarning("No Results", "Run an analysis first before exporting.")
            return
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"SkillSpark_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            title="Save Report as PDF")
        if not save_path:
            return
        self.status_var.set("⏳  Generating PDF...")
        self.root.update()
        ok, msg = export_to_pdf(self.last_result, self.current_filename, save_path)
        if ok:
            self.status_var.set(f"✅  PDF saved: {os.path.basename(save_path)}")
            messagebox.showinfo("PDF Exported",
                f"Report saved successfully!\n\nLocation:\n{save_path}")
        else:
            self.status_var.set("❌  PDF export failed")
            messagebox.showerror("Export Error", f"Could not create PDF:\n{msg}")

# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = SkillSparkApp(root)
    root.mainloop()