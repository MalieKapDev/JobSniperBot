USER_PROFILE = {
  "title": "Junior Full-Stack Developer",
  "summary": (
    "Aspiring full-stack developer with a strong foundation in front-end technologies "
    "(HTML, CSS, JavaScript, React) and a growing skill set in backend development "
    "(Node.js, Express, APIs, SQL). Passionate about building efficient, responsive, and user-friendly "
    "applications. Committed to continuous learning and open to mentorship while contributing to real-world projects."
  ),

  "experience": [
    "Vape Junction | Jan 2024 – Present | Sales Associate | Pretoria, Gauteng | "
    "Increased advanced vape product sales by 20% through customer education. "
    "Recommended custom starter kits to 1000+ customers with a 90% satisfaction rate. "
    "Fostered customer loyalty with a 30% rise in repeat visits through personalized service.",

    "Infinity Times Infinity Productions | Oct 2023 – Dec 2023 | Videographer & Editor | Pretoria, Gauteng | "
    "Produced highlight and full-length wedding films with a 95% client satisfaction rate. "
    "Utilized multi-camera setups to improve storytelling, generating a 20% increase in referral business. "
    "Delivered high-quality edits within tight deadlines, boosting positive client reviews.",

    "PUC Marketing | Jan 2021 – Aug 2023 | Office Administrator & Data Analyst | Remote across SA | "
    "Implemented data systems to streamline reporting and increase improvement insights by 10%. "
    "Supported 200+ team members with efficient data handling. "
    "Managed payroll, travel bookings, and communication for executive teams, improving workflow by 15%.",

    "Visual Impact | Jan 2020 – Feb 2020 | Rentals Intern | Johannesburg, Gauteng | "
    "Prepared and maintained film equipment for rentals. Ensured client readiness through gear tests and tutorials. "
    "Documented and coordinated repair processes, maintaining equipment quality."
  ],

  "education": [
    "Harvard edX | In Progress | CS50: Introduction to Computer Science | Focused on C, Python, SQL, web dev fundamentals, and algorithms.",
    "freeCodeCamp | Aug 2024 | Data Visualization Certification | Created interactive charts with D3.js and APIs.",
    "SheCodes | Sep 2024 | React Development Certificate | Built responsive React apps with API integration.",
    "freeCodeCamp | May 2024 | Front End Libraries Certification | Learned React, Redux, Bootstrap, Sass.",
    "SheCodes | Apr 2024 | Web Development Certificate | Deepened ES6, animations, and API calls.",
    "freeCodeCamp | Mar 2024 | JavaScript Algorithms & Data Structures | Focused on DOM manipulation, ES6, regex.",
    "SheCodes | Feb 2024 | Coding Basics | Foundations in HTML5, CSS3, and JavaScript.",
    "freeCodeCamp | Jan 2024 | Responsive Web Design Certification | Developed responsive layouts using HTML & CSS.",
    "Type Whizz | Sep 2023 | Professional Transcription Certificate | Mastered audio typing and editing best practices.",
    "The Open Window Institute | 2016–2020 | BA in Film & TV, Cinematography | Specialized in visual storytelling, sound design, and post-production.",
    "Die Hoërskool Menlopark | 2015 | National Senior Certificate (NSC) | Focus on Visual Arts, Design, and STEM."
  ],

  "project_highlights": [
    "Code with Malie Blog | Oct 2024 | HTML, CSS, JavaScript, WordPress, SEO | "
    "Built a personal blog to share coding insights and resources. "
    "Managed a multi-platform content strategy growing TikTok to 1800+ followers. "
    "Produced SEO-optimized posts to boost site visibility and build a community of learners.",

    "Weather App with News | Sep 2024 | React, APIs | "
    "Integrated live weather data and news headlines into a single-page React app. "
    "Implemented state management and dynamic UI updates.",

    "Classic Weather App | Mar 2024 | JavaScript, HTML, CSS | "
    "Built a real-time weather forecast site fetching data from OpenWeather API. "
    "Focused on clean UI, responsive design, and user accessibility.",

    "Dragon Repeller Game | Feb 2024 | JavaScript, HTML, CSS | "
    "Created an interactive RPG-style game with animations, event-driven logic, and responsive UI elements.",

    "Portfolio Website | Jan 2024 | HTML, CSS, JavaScript | "
    "Developed a responsive personal website to showcase projects and skills. "
    "Includes interactive features and GitHub project links."
  ],

  "technical_skills": [
    "HTML5 (semantic & accessible web design)",
    "CSS3 (Flexbox, Grid, responsive layouts)",
    "JavaScript (ES6+, DOM manipulation, fetch/AJAX)",
    "React (components, hooks, state management)",
    "Redux (basic)",
    "Bootstrap & Sass",
    "jQuery",
    "Node.js (beginner)",
    "Express.js (basic backend routing & middleware)",
    "REST APIs (Fetch, Axios)",
    "SQL (basic queries & data structures)",
    "Git & GitHub (version control, branching)",
    "CLI (basic terminal commands)",
    "Netlify (project deployment)",
    "Visual Studio Code",
    "Microsoft Office (Word, Excel, PowerPoint)",
    "Power BI & Repsly (data analytics & visualization)",
    "Adobe Creative Suite (Photoshop, Illustrator, Premiere Pro)",
    "Sage Payroll (admin & HR reporting experience)"
  ],

  "professional_strengths": [
    "Adaptability",
    "Problem Solving",
    "Debugging & Troubleshooting",
    "Responsive Design",
    "Teamwork & Collaboration",
    "Communication Skills",
    "Attention to Detail",
    "Time Management",
    "Continuous Learning",
    "Customer Experience Mindset",
    "HR & Payroll Workflow Understanding"
  ],

  "languages": [
    "English: Fluent",
    "Afrikaans: Native",
    "French: Basic"
  ],

  "achievements": [
    "Harvard edX CS50 Financial Aid Recipient | 2024 | Received financial assistance for top-tier CS education.",
    "SheCodes Foundation Scholarship Winner | 2023 | Awarded full scholarship for coding bootcamps in Web Dev & React.",
    "Pretoria Eisteddfod | 2015 | Received A & A+ awards for visual art pieces.",
    "Visual Arts Colours | 2014 & 2015 | Recognized for outstanding achievement in arts.",
    "Afrikaans Expo Winner | 2012 | Took 1st place in Media category."
  ]
}

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def get_clean_resume_text(profile=USER_PROFILE):
    # Flatten dictionary into a big string
    combined_text = ""

    for key, value in profile.items():
        if isinstance(value, str):
            combined_text += value + " "
        elif isinstance(value, list):
            for item in value:
                combined_text += item + " "

    # Normalize text
    text = combined_text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # remove punctuation
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return " ".join(tokens)