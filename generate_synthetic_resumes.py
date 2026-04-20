#!/usr/bin/env python3
"""
Synthetic Resume Dataset Generator
Generates ~12,000 resumes: 5000 genuine (0), 5000 fake (1), 2000 suspicious (2).
Output: synthetic_resumes.csv  +  sample_resumes.json
"""

import csv
import json
import random
import os

# ──────────────────────────────────────────────────────────────────────────────
# DATA POOLS
# ──────────────────────────────────────────────────────────────────────────────

FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael",
    "Linda", "David", "Elizabeth", "William", "Barbara", "Richard", "Susan",
    "Joseph", "Jessica", "Thomas", "Sarah", "Christopher", "Karen", "Charles",
    "Lisa", "Daniel", "Nancy", "Matthew", "Betty", "Anthony", "Margaret",
    "Mark", "Sandra", "Steven", "Ashley", "Paul", "Kimberly", "Andrew",
    "Emily", "Joshua", "Donna", "Kenneth", "Michelle", "Kevin", "Carol",
    "Brian", "Amanda", "George", "Dorothy", "Timothy", "Melissa", "Ronald",
    "Deborah", "Jason", "Stephanie", "Edward", "Rebecca", "Jeffrey", "Sharon",
    "Ryan", "Laura", "Jacob", "Cynthia", "Gary", "Kathleen", "Nicholas",
    "Amy", "Eric", "Angela", "Jonathan", "Shirley", "Stephen", "Anna",
    "Larry", "Brenda", "Justin", "Pamela", "Scott", "Emma", "Brandon",
    "Nicole", "Benjamin", "Helen", "Samuel", "Samantha", "Raymond", "Katherine",
    "Gregory", "Christine", "Frank", "Debra", "Alexander", "Rachel", "Patrick",
    "Carolyn", "Jack", "Janet", "Dennis", "Catherine", "Jerry", "Maria",
    "Tyler", "Heather", "Aaron", "Diane", "Jose", "Ruth", "Nathan", "Julie",
    "Henry", "Olivia", "Douglas", "Joyce", "Peter", "Virginia", "Zachary",
    "Victoria", "Kyle", "Kelly", "Noah", "Lauren", "Ethan", "Christina",
    "Jeremy", "Joan", "Walter", "Evelyn", "Christian", "Judith", "Keith",
    "Megan", "Roger", "Andrea", "Terry", "Cheryl", "Austin", "Hannah",
    "Sean", "Jacqueline", "Gerald", "Martha", "Carl", "Gloria", "Harold",
    "Teresa", "Dylan", "Ann", "Arthur", "Sara", "Lawrence", "Madison",
    "Jordan", "Frances", "Jesse", "Kathryn", "Bryan", "Janice", "Billy",
    "Jean", "Bruce", "Abigail", "Gabriel", "Alice", "Joe", "Judy",
    "Aiden", "Priya", "Rahul", "Sneha", "Vikram", "Ananya", "Rohit",
    "Deepika", "Arjun", "Kavita", "Suresh", "Neha", "Amit", "Pooja",
    "Raj", "Meena", "Sanjay", "Divya", "Wei", "Mei", "Hiroshi", "Yuki",
    "Ahmed", "Fatima", "Omar", "Aisha", "Ali", "Zara", "Hassan", "Layla",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz",
    "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris",
    "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan",
    "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos",
    "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez",
    "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long",
    "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry", "Russell",
    "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes",
    "Sharma", "Gupta", "Singh", "Kumar", "Mehta", "Reddy", "Joshi",
    "Mishra", "Verma", "Chopra", "Tanaka", "Yamamoto", "Nakamura",
    "Chen", "Wang", "Li", "Zhang", "Liu", "Yang", "Huang", "Khan",
    "Ali", "Hassan", "Ahmed", "Rahman", "Begum", "Chowdhury",
]

DOMAINS = {
    "Software Engineering": {
        "fresher_skills": ["Python", "Java", "HTML", "CSS", "JavaScript", "Git", "SQL", "REST APIs"],
        "junior_skills": ["React", "Node.js", "PostgreSQL", "Docker", "TypeScript", "MongoDB", "Redis", "CI/CD", "Agile"],
        "mid_skills": ["Kubernetes", "AWS", "Microservices", "System Design", "GraphQL", "Kafka", "Terraform", "Jenkins", "ElasticSearch"],
        "senior_skills": ["Architecture Design", "Cloud Native", "Performance Optimization", "Technical Leadership", "Distributed Systems", "Service Mesh", "Event-Driven Architecture"],
        "titles": {
            "fresher": ["Software Developer Intern", "Junior Software Developer", "Trainee Software Engineer", "Associate Developer"],
            "junior": ["Software Developer", "Software Engineer", "Backend Developer", "Frontend Developer", "Full Stack Developer"],
            "mid": ["Senior Software Engineer", "Lead Developer", "Staff Engineer", "Software Architect", "Engineering Lead"],
            "senior": ["Principal Engineer", "VP of Engineering", "Director of Engineering", "Chief Technology Officer", "Distinguished Engineer"],
        },
        "projects": [
            "Built a RESTful API for an e-commerce platform handling {n} daily transactions",
            "Developed a real-time chat application using WebSocket and {tech}",
            "Created an automated CI/CD pipeline reducing deployment time by {p}%",
            "Implemented microservices architecture serving {n} concurrent users",
            "Designed and built a data pipeline processing {n} records daily",
            "Developed a responsive web application using {tech} for {domain}",
            "Built a notification service handling {n} push notifications per day",
            "Implemented authentication and authorization using OAuth 2.0 and JWT",
            "Created a caching layer using Redis improving response time by {p}%",
            "Developed a search feature using ElasticSearch for {n} products",
            "Migrated legacy monolith to microservices architecture",
            "Built internal tooling dashboard for monitoring system health",
            "Implemented automated testing framework achieving {p}% code coverage",
        ],
    },
    "Data Science": {
        "fresher_skills": ["Python", "Pandas", "NumPy", "Matplotlib", "SQL", "Excel", "Statistics", "Jupyter"],
        "junior_skills": ["Scikit-learn", "TensorFlow", "Machine Learning", "Data Visualization", "Feature Engineering", "A/B Testing", "Tableau"],
        "mid_skills": ["Deep Learning", "NLP", "Computer Vision", "PyTorch", "Spark", "MLOps", "Model Deployment", "AWS SageMaker"],
        "senior_skills": ["Research Leadership", "ML Strategy", "Large-Scale ML Systems", "Causal Inference", "Reinforcement Learning", "AI Ethics", "Technical Mentorship"],
        "titles": {
            "fresher": ["Data Science Intern", "Junior Data Analyst", "Trainee Data Scientist", "Associate Analyst"],
            "junior": ["Data Scientist", "Data Analyst", "ML Engineer", "Analytics Engineer", "Business Analyst"],
            "mid": ["Senior Data Scientist", "Lead ML Engineer", "Staff Data Scientist", "Principal Analyst"],
            "senior": ["Director of Data Science", "VP of Analytics", "Chief Data Officer", "Head of ML", "Distinguished Data Scientist"],
        },
        "projects": [
            "Built a recommendation engine increasing user engagement by {p}%",
            "Developed a sentiment analysis model with {p}% accuracy on customer reviews",
            "Created a fraud detection system identifying {p}% of fraudulent transactions",
            "Implemented a churn prediction model reducing customer attrition by {p}%",
            "Built an NLP pipeline for processing {n} documents daily",
            "Designed A/B testing framework and analyzed results for {n} experiments",
            "Developed time-series forecasting model for demand planning",
            "Created customer segmentation model improving targeted marketing ROI by {p}%",
            "Built image classification model using {tech} with {p}% accuracy",
            "Implemented real-time anomaly detection for system monitoring",
        ],
    },
    "Web Development": {
        "fresher_skills": ["HTML", "CSS", "JavaScript", "Bootstrap", "jQuery", "Git", "Responsive Design"],
        "junior_skills": ["React", "Angular", "Vue.js", "Node.js", "Express", "MongoDB", "SASS", "TypeScript", "Webpack"],
        "mid_skills": ["Next.js", "GraphQL", "Performance Optimization", "SEO", "PWA", "Server-Side Rendering", "AWS", "Docker"],
        "senior_skills": ["Web Architecture", "Design Systems", "Accessibility", "Technical Leadership", "Cross-browser Compatibility", "Micro-Frontends"],
        "titles": {
            "fresher": ["Web Developer Intern", "Junior Web Developer", "Frontend Intern", "Trainee Web Developer"],
            "junior": ["Web Developer", "Frontend Developer", "UI Developer", "Full Stack Developer"],
            "mid": ["Senior Web Developer", "Lead Frontend Engineer", "Staff Web Developer", "Frontend Architect"],
            "senior": ["Head of Frontend", "Director of Web Engineering", "VP of Frontend", "Principal Web Architect"],
        },
        "projects": [
            "Built a responsive e-commerce website with {n} product listings",
            "Developed a single-page application using {tech}",
            "Created a content management system for {domain}",
            "Implemented Progressive Web App with offline functionality",
            "Built a real-time dashboard for monitoring {domain} metrics",
            "Designed and developed a design system with {n} reusable components",
            "Implemented server-side rendering improving SEO score by {p}%",
            "Created an interactive data visualization dashboard using D3.js",
            "Built a multi-tenant SaaS platform for {domain}",
            "Optimized website performance achieving {p}% improvement in load time",
        ],
    },
    "DevOps": {
        "fresher_skills": ["Linux", "Bash", "Git", "Python", "Networking Basics", "AWS Basics", "Docker Basics"],
        "junior_skills": ["Docker", "Jenkins", "Ansible", "Terraform", "CI/CD", "AWS", "Monitoring", "Nginx"],
        "mid_skills": ["Kubernetes", "Helm", "Prometheus", "Grafana", "Infrastructure as Code", "Service Mesh", "Multi-Cloud"],
        "senior_skills": ["Platform Engineering", "SRE", "Chaos Engineering", "Cost Optimization", "Enterprise Architecture", "Cloud Strategy"],
        "titles": {
            "fresher": ["DevOps Intern", "Junior Systems Administrator", "Cloud Intern", "IT Support Engineer"],
            "junior": ["DevOps Engineer", "Systems Engineer", "Cloud Engineer", "Release Engineer"],
            "mid": ["Senior DevOps Engineer", "SRE Lead", "Platform Engineer", "Infrastructure Architect"],
            "senior": ["Director of DevOps", "VP of Infrastructure", "Head of Platform", "Chief Infrastructure Officer"],
        },
        "projects": [
            "Automated infrastructure provisioning using Terraform for {n} servers",
            "Built CI/CD pipeline reducing deployment time from {n} hours to {n2} minutes",
            "Implemented container orchestration using Kubernetes for {n} microservices",
            "Set up monitoring and alerting using Prometheus and Grafana",
            "Migrated {n} applications from on-premise to AWS cloud",
            "Implemented GitOps workflow using ArgoCD",
            "Designed disaster recovery solution with {p}% uptime SLA",
            "Built self-healing infrastructure reducing incidents by {p}%",
            "Automated security scanning in CI/CD pipeline",
            "Implemented blue-green deployment strategy",
        ],
    },
    "Cybersecurity": {
        "fresher_skills": ["Networking", "Linux", "Python", "Security Fundamentals", "Firewalls", "TCP/IP"],
        "junior_skills": ["Penetration Testing", "SIEM", "Incident Response", "Vulnerability Assessment", "IDS/IPS", "OWASP"],
        "mid_skills": ["Threat Hunting", "Malware Analysis", "Cloud Security", "SOC Operations", "Forensics", "Zero Trust Architecture"],
        "senior_skills": ["Security Architecture", "Risk Management", "Compliance", "Security Strategy", "Red Team Leadership", "CISO Advisory"],
        "titles": {
            "fresher": ["Security Analyst Intern", "Junior SOC Analyst", "IT Security Trainee"],
            "junior": ["Security Analyst", "SOC Analyst", "Penetration Tester", "Security Engineer"],
            "mid": ["Senior Security Engineer", "Lead Security Analyst", "Security Architect", "Threat Intelligence Lead"],
            "senior": ["CISO", "Director of Security", "VP of Cybersecurity", "Head of Information Security"],
        },
        "projects": [
            "Conducted penetration testing for {n} client applications",
            "Implemented SIEM solution processing {n} events per second",
            "Developed incident response playbook reducing response time by {p}%",
            "Built automated vulnerability scanning pipeline for {n} assets",
            "Designed zero trust architecture for enterprise network",
            "Implemented DLP solution protecting {n} sensitive records",
            "Conducted security awareness training for {n} employees",
            "Built threat intelligence platform aggregating {n} data sources",
        ],
    },
    "Mobile Development": {
        "fresher_skills": ["Java", "Kotlin", "Swift", "XML", "Git", "REST APIs", "Android Studio", "Xcode"],
        "junior_skills": ["React Native", "Flutter", "Firebase", "SQLite", "Push Notifications", "App Store Deployment", "MVVM"],
        "mid_skills": ["Performance Optimization", "CI/CD for Mobile", "Architecture Patterns", "BLE", "AR/VR", "In-App Purchases"],
        "senior_skills": ["Mobile Architecture", "Cross-Platform Strategy", "Mobile DevOps", "Technical Leadership", "Platform SDKs"],
        "titles": {
            "fresher": ["Mobile Developer Intern", "Junior Android Developer", "iOS Developer Trainee"],
            "junior": ["Android Developer", "iOS Developer", "Mobile Developer", "React Native Developer"],
            "mid": ["Senior Mobile Developer", "Lead Mobile Engineer", "Mobile Architect", "Staff Mobile Engineer"],
            "senior": ["Head of Mobile", "Director of Mobile Engineering", "VP of Mobile", "Principal Mobile Architect"],
        },
        "projects": [
            "Developed a fitness tracking app with {n} downloads on Play Store",
            "Built a food delivery application using {tech}",
            "Created a social media app with real-time messaging",
            "Implemented offline-first architecture for field service application",
            "Built a banking app with biometric authentication",
            "Developed AR-based shopping experience for {domain}",
            "Created a custom camera SDK used by {n} third-party apps",
            "Implemented push notification system reaching {n} daily users",
        ],
    },
    "Database Administration": {
        "fresher_skills": ["SQL", "MySQL", "Database Design", "Excel", "Data Entry", "Basic Queries"],
        "junior_skills": ["PostgreSQL", "Oracle", "MongoDB", "Indexing", "Backup and Recovery", "Performance Tuning", "Data Migration"],
        "mid_skills": ["Replication", "Sharding", "Data Warehouse", "ETL", "Partitioning", "High Availability", "Cloud Databases"],
        "senior_skills": ["Database Architecture", "Capacity Planning", "Multi-Region Deployments", "Database Strategy", "Data Governance"],
        "titles": {
            "fresher": ["Database Intern", "Junior DBA", "Data Entry Specialist"],
            "junior": ["Database Administrator", "SQL Developer", "Data Engineer"],
            "mid": ["Senior DBA", "Lead Data Engineer", "Database Architect"],
            "senior": ["Director of Data Engineering", "VP of Data Infrastructure", "Chief Data Architect"],
        },
        "projects": [
            "Managed {n} production databases with 99.{p}% uptime",
            "Migrated {n} TB of data from Oracle to PostgreSQL",
            "Implemented database sharding reducing query time by {p}%",
            "Designed ETL pipeline processing {n} records per hour",
            "Built automated backup and recovery system",
            "Optimized slow queries improving performance by {p}%",
            "Implemented database monitoring and alerting for {n} instances",
        ],
    },
    "Cloud Engineering": {
        "fresher_skills": ["AWS Basics", "Linux", "Python", "Networking", "Virtualization", "Bash"],
        "junior_skills": ["AWS EC2", "S3", "Lambda", "CloudFormation", "Azure", "GCP", "IAM", "VPC"],
        "mid_skills": ["Multi-Cloud", "Cost Optimization", "Security Best Practices", "Serverless Architecture", "Data Lakes", "CDN"],
        "senior_skills": ["Cloud Strategy", "Enterprise Architecture", "Cloud Migration Leadership", "Vendor Management", "Cloud Governance"],
        "titles": {
            "fresher": ["Cloud Intern", "Junior Cloud Engineer", "IT Associate"],
            "junior": ["Cloud Engineer", "AWS Solutions Architect", "Cloud Developer"],
            "mid": ["Senior Cloud Engineer", "Cloud Architect", "Lead Cloud Engineer"],
            "senior": ["Director of Cloud", "VP of Cloud Infrastructure", "Chief Cloud Officer"],
        },
        "projects": [
            "Migrated {n} applications to AWS cloud reducing costs by {p}%",
            "Designed multi-region architecture with {p}% uptime SLA",
            "Implemented serverless architecture using Lambda for {domain}",
            "Built data lake processing {n} GB of data daily",
            "Designed cloud security framework for enterprise",
            "Implemented auto-scaling solution handling {n}x traffic spikes",
            "Built cloud cost optimization tool saving ${n}K annually",
        ],
    },
    "QA Engineering": {
        "fresher_skills": ["Manual Testing", "Test Cases", "Bug Reporting", "JIRA", "SQL", "Basic Automation"],
        "junior_skills": ["Selenium", "API Testing", "Postman", "TestNG", "BDD", "Jenkins", "Python for Testing"],
        "mid_skills": ["Performance Testing", "Security Testing", "Test Architecture", "CI/CD Integration", "Load Testing", "JMeter"],
        "senior_skills": ["QA Strategy", "Test Automation Architecture", "Quality Leadership", "Release Management", "SDQA Process"],
        "titles": {
            "fresher": ["QA Intern", "Junior QA Analyst", "Test Engineer Trainee"],
            "junior": ["QA Engineer", "Test Engineer", "QA Analyst", "SDET"],
            "mid": ["Senior QA Engineer", "QA Lead", "Test Architect", "Senior SDET"],
            "senior": ["Director of QA", "VP of Quality", "Head of QA Engineering"],
        },
        "projects": [
            "Automated {n} test cases reducing regression testing time by {p}%",
            "Built API test framework using {tech} for {n} endpoints",
            "Implemented performance testing for application handling {n} concurrent users",
            "Created BDD test suite with {n} scenarios using Cucumber",
            "Designed test data management solution for {n} environments",
            "Implemented visual regression testing for {n} UI components",
            "Built test reporting dashboard for stakeholder visibility",
        ],
    },
    "Project Management": {
        "fresher_skills": ["MS Office", "Communication", "Documentation", "JIRA", "Agile Basics", "Presentation Skills"],
        "junior_skills": ["Scrum", "Kanban", "Risk Management", "Stakeholder Management", "Budgeting", "Resource Planning", "Confluence"],
        "mid_skills": ["Program Management", "Vendor Management", "PMP", "SAFe", "Strategic Planning", "Change Management"],
        "senior_skills": ["Portfolio Management", "Executive Communication", "Organizational Transformation", "P&L Responsibility", "C-Suite Advisory"],
        "titles": {
            "fresher": ["Project Coordinator", "Junior Project Manager", "PMO Analyst"],
            "junior": ["Project Manager", "Scrum Master", "Delivery Manager"],
            "mid": ["Senior Project Manager", "Program Manager", "Delivery Lead", "Engagement Manager"],
            "senior": ["Director of PMO", "VP of Delivery", "Head of Programs", "Chief Operating Officer"],
        },
        "projects": [
            "Managed {n}-member cross-functional team delivering {domain} platform",
            "Led Agile transformation for team of {n} engineers",
            "Delivered project worth ${n}M on time and under budget",
            "Managed vendor relationships with {n} external partners",
            "Implemented PMO best practices reducing project overruns by {p}%",
            "Coordinated release management for {n} product releases per quarter",
        ],
    },
    "Finance": {
        "fresher_skills": ["Excel", "Financial Analysis", "Accounting", "SQL", "Communication", "Data Entry"],
        "junior_skills": ["Financial Modeling", "Forecasting", "SAP", "Budgeting", "Compliance", "VBA", "Power BI"],
        "mid_skills": ["Risk Analysis", "Portfolio Management", "Derivatives", "Regulatory Compliance", "M&A Analysis", "Bloomberg Terminal"],
        "senior_skills": ["Financial Strategy", "C-Suite Advisory", "Capital Markets", "Fund Management", "Board Reporting"],
        "titles": {
            "fresher": ["Finance Intern", "Junior Financial Analyst", "Accounting Assistant"],
            "junior": ["Financial Analyst", "Accountant", "Credit Analyst", "Investment Analyst"],
            "mid": ["Senior Financial Analyst", "Finance Manager", "Portfolio Manager"],
            "senior": ["CFO", "VP of Finance", "Director of Finance", "Controller"],
        },
        "projects": [
            "Built financial model for ${n}M product launch",
            "Automated monthly reporting saving {n} hours per cycle",
            "Analyzed portfolio performance across {n} asset classes",
            "Implemented budgeting system for {n} departments",
            "Developed risk assessment framework for ${n}M loan portfolio",
        ],
    },
    "Healthcare IT": {
        "fresher_skills": ["HL7", "Medical Terminology", "EMR Basics", "SQL", "Excel", "HIPAA Basics"],
        "junior_skills": ["Epic", "Cerner", "FHIR", "Clinical Data", "ICD-10", "Database Management"],
        "mid_skills": ["Health Informatics", "Interoperability", "Data Analytics", "Clinical Decision Support", "Population Health"],
        "senior_skills": ["Healthcare Strategy", "Regulatory Compliance", "Digital Health Leadership", "Telehealth Architecture"],
        "titles": {
            "fresher": ["Health IT Intern", "Clinical Data Analyst Trainee", "Junior EMR Analyst"],
            "junior": ["Health IT Analyst", "Clinical Informatics Analyst", "EMR Specialist"],
            "mid": ["Senior Health IT Analyst", "Informatics Manager", "Clinical Systems Lead"],
            "senior": ["CMIO", "VP of Health IT", "Director of Clinical Informatics"],
        },
        "projects": [
            "Implemented Epic EMR system for {n}-bed hospital",
            "Built clinical data warehouse with {n} patient records",
            "Developed HL7/FHIR integration connecting {n} systems",
            "Implemented telehealth platform serving {n} patients monthly",
            "Built clinical decision support system for {domain}",
        ],
    },
    "Marketing": {
        "fresher_skills": ["Social Media", "Content Writing", "SEO Basics", "Google Analytics", "Canva", "Email Marketing"],
        "junior_skills": ["Digital Marketing", "PPC", "Marketing Automation", "HubSpot", "A/B Testing", "CRM", "Google Ads"],
        "mid_skills": ["Brand Strategy", "Market Research", "Campaign Management", "Marketing Analytics", "Content Strategy"],
        "senior_skills": ["CMO Strategy", "P&L Management", "Brand Architecture", "GTM Strategy", "Marketing Transformation"],
        "titles": {
            "fresher": ["Marketing Intern", "Junior Marketing Associate", "Content Intern"],
            "junior": ["Marketing Specialist", "Digital Marketer", "Content Manager", "SEO Specialist"],
            "mid": ["Senior Marketing Manager", "Brand Manager", "Marketing Lead", "Growth Manager"],
            "senior": ["CMO", "VP of Marketing", "Director of Marketing", "Head of Growth"],
        },
        "projects": [
            "Managed social media accounts growing following by {p}%",
            "Launched email campaign with {p}% open rate for {n} subscribers",
            "Implemented SEO strategy increasing organic traffic by {p}%",
            "Created content marketing strategy generating {n} leads per month",
            "Managed PPC campaigns with ${n}K monthly budget achieving {p}% ROI",
        ],
    },
    "HR": {
        "fresher_skills": ["Recruitment Basics", "MS Office", "Communication", "Data Entry", "HR Software Basics"],
        "junior_skills": ["Talent Acquisition", "HRIS", "Employee Relations", "Payroll", "Onboarding", "ATS"],
        "mid_skills": ["HR Analytics", "Compensation", "Performance Management", "Learning & Development", "HR Strategy"],
        "senior_skills": ["Organizational Development", "Executive Search", "HR Transformation", "Culture Strategy", "Board Advisory"],
        "titles": {
            "fresher": ["HR Intern", "Junior HR Coordinator", "Recruitment Assistant"],
            "junior": ["HR Generalist", "Recruiter", "HR Coordinator", "Talent Acquisition Specialist"],
            "mid": ["Senior HR Manager", "HR Business Partner", "Talent Acquisition Lead"],
            "senior": ["CHRO", "VP of HR", "Director of People", "Head of Talent"],
        },
        "projects": [
            "Managed hiring process for {n} positions across {n2} departments",
            "Implemented HRIS system for {n}-employee organization",
            "Designed onboarding program reducing time-to-productivity by {p}%",
            "Built employee engagement program improving retention by {p}%",
            "Led diversity and inclusion initiative increasing diverse hires by {p}%",
        ],
    },
    "Sales": {
        "fresher_skills": ["Communication", "CRM Basics", "Cold Calling", "Lead Generation", "MS Office", "Presentation Skills"],
        "junior_skills": ["Salesforce", "Account Management", "Pipeline Management", "Negotiation", "B2B Sales", "HubSpot CRM"],
        "mid_skills": ["Enterprise Sales", "Sales Strategy", "Territory Management", "Sales Analytics", "Partnership Development"],
        "senior_skills": ["Revenue Strategy", "Sales Leadership", "P&L Management", "Market Expansion", "Board Reporting"],
        "titles": {
            "fresher": ["Sales Intern", "Junior Sales Representative", "Sales Associate", "Business Development Trainee"],
            "junior": ["Sales Executive", "Account Executive", "Business Development Representative"],
            "mid": ["Senior Sales Manager", "Regional Sales Manager", "Sales Lead", "Key Account Manager"],
            "senior": ["VP of Sales", "Chief Revenue Officer", "Director of Sales", "Head of Business Development"],
        },
        "projects": [
            "Closed deals worth ${n}M in annual revenue",
            "Managed portfolio of {n} enterprise accounts",
            "Built sales pipeline generating ${n}M in opportunities",
            "Implemented Salesforce CRM for team of {n} reps",
            "Exceeded quarterly targets by {p}% for {n} consecutive quarters",
        ],
    },
}

UNIVERSITIES = [
    "Massachusetts Institute of Technology", "Stanford University",
    "University of California, Berkeley", "Carnegie Mellon University",
    "Georgia Institute of Technology", "University of Michigan",
    "University of Texas at Austin", "University of Illinois at Urbana-Champaign",
    "Purdue University", "University of Washington",
    "Penn State University", "Ohio State University",
    "Virginia Tech", "Texas A&M University",
    "University of Florida", "Arizona State University",
    "University of Maryland", "University of Minnesota",
    "North Carolina State University", "University of Colorado Boulder",
    "Boston University", "Northeastern University",
    "University of Southern California", "Columbia University",
    "New York University", "University of Pennsylvania",
    "Cornell University", "Princeton University",
    "Rice University", "Duke University",
    "University of Wisconsin-Madison", "Rutgers University",
    "University of California, Los Angeles", "University of California, San Diego",
    "University of Virginia", "Indiana University",
    "Michigan State University", "San Jose State University",
    "California State University", "University of North Carolina",
    "IIT Bombay", "IIT Delhi", "IIT Madras",
    "NIT Trichy", "BITS Pilani", "Delhi University",
    "Anna University", "VIT University", "SRM University", "Manipal University",
    "National University of Singapore", "University of Toronto",
    "University of Waterloo", "University of British Columbia",
    "Nanyang Technological University",
]

DEGREES = {
    "tech": ["B.Tech in Computer Science", "B.S. in Computer Science", "B.Tech in Information Technology",
             "B.S. in Software Engineering", "B.Tech in Electronics and Communication",
             "B.S. in Information Systems", "B.Tech in Computer Engineering",
             "B.S. in Electrical Engineering", "B.S. in Mathematics and Computer Science"],
    "tech_masters": ["M.Tech in Computer Science", "M.S. in Computer Science", "M.S. in Data Science",
                     "M.S. in Artificial Intelligence", "M.Tech in Software Engineering",
                     "M.S. in Information Systems", "M.S. in Cybersecurity",
                     "MBA in Information Technology"],
    "business": ["BBA", "B.Com", "B.S. in Business Administration", "B.S. in Finance",
                 "B.S. in Marketing", "B.S. in Economics"],
    "business_masters": ["MBA", "M.S. in Finance", "M.S. in Marketing Analytics", "M.Com"],
}

COMPANIES = [
    "Google", "Microsoft", "Amazon", "Apple", "Meta", "Netflix", "Tesla",
    "IBM", "Oracle", "SAP", "Salesforce", "Adobe", "Cisco", "Intel",
    "TCS", "Infosys", "Wipro", "HCL Technologies", "Cognizant",
    "Accenture", "Deloitte", "PwC", "KPMG", "EY",
    "JPMorgan Chase", "Goldman Sachs", "Morgan Stanley", "Citigroup",
    "Uber", "Lyft", "Airbnb", "Stripe", "Square", "Shopify",
    "Twitter", "LinkedIn", "Snap", "Pinterest", "Reddit",
    "PayPal", "Visa", "Mastercard", "American Express",
    "Walmart", "Target", "Best Buy", "Home Depot",
    "Lockheed Martin", "Boeing", "Raytheon",
    "Johnson & Johnson", "Pfizer", "Abbott",
    "Techsys Solutions", "Innovatech Corp", "DataDriven Inc",
    "CloudVista Technologies", "NexGen Software", "Synapse Digital",
    "Quantum Analytics", "FutureTech Solutions", "AlphaWave Systems",
    "CyberShield Corp", "Brightpath IT", "Codewave Technologies",
    "PrimeSoft Solutions", "LogicTree Inc", "Skyline Digital",
    "CoreBridge Systems", "Zenith Technologies", "VertexAI Labs",
    "MetaScale Corp", "BluePeak Software", "Agile Dynamics",
    "SwiftCode Technologies", "DataForge Systems", "CloudBridge Inc",
    "TechNova Solutions", "Mindcraft Digital", "PivotPoint Analytics",
    "InfraCore Systems", "PixelPerfect Studios", "StreamLine Tech",
]

CITIES = [
    "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
    "Boston, MA", "Chicago, IL", "Denver, CO", "Los Angeles, CA",
    "San Jose, CA", "Raleigh, NC", "Atlanta, GA", "Dallas, TX",
    "Portland, OR", "Washington, DC", "Minneapolis, MN",
    "Phoenix, AZ", "San Diego, CA", "Philadelphia, PA",
    "Detroit, MI", "Orlando, FL", "Charlotte, NC", "Nashville, TN",
    "Bangalore, India", "Hyderabad, India", "Pune, India",
    "Chennai, India", "Mumbai, India", "Gurgaon, India",
    "Toronto, Canada", "Vancouver, Canada", "London, UK",
    "Singapore", "Berlin, Germany", "Dublin, Ireland",
]

CERTIFICATIONS = {
    "tech": ["AWS Solutions Architect", "Google Cloud Professional", "Azure Administrator",
             "Certified Kubernetes Administrator", "HashiCorp Terraform Associate",
             "Docker Certified Associate", "CompTIA Security+", "CISSP",
             "Oracle Certified Professional", "Certified Scrum Master"],
    "business": ["PMP", "Six Sigma Green Belt", "Six Sigma Black Belt", "PRINCE2",
                 "CFA Level I", "CFA Level II", "CFA Level III", "CPA",
                 "SHRM-CP", "PHR", "Google Analytics Certified"],
}

# ──────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────

def rand_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def rand_year(low, high):
    return random.randint(low, high)

def rand_percent(low=10, high=60):
    return random.randint(low, high)

def rand_num(low=50, high=5000):
    return random.randint(low, high)

def fill_project_template(template):
    """Fill placeholders in a project template."""
    text = template
    text = text.replace("{p}", str(rand_percent()))
    text = text.replace("{n2}", str(rand_num(5, 30)))
    text = text.replace("{n}", str(rand_num()))
    text = text.replace("{tech}", random.choice([
        "React", "Angular", "Vue.js", "Node.js", "Python", "Django",
        "Flask", "Spring Boot", "TensorFlow", "PyTorch", "Flutter",
        "React Native", "Kubernetes", "Docker", "AWS Lambda",
    ]))
    text = text.replace("{domain}", random.choice([
        "healthcare", "finance", "e-commerce", "logistics",
        "education", "real estate", "insurance", "retail",
        "manufacturing", "media", "travel", "hospitality",
    ]))
    return text

def get_tier(experience_years):
    """Return experience tier based on years."""
    if experience_years <= 1:
        return "fresher"
    elif experience_years <= 3:
        return "junior"
    elif experience_years <= 7:
        return "mid"
    else:
        return "senior"

def get_skills_for_tier(domain_info, tier, experience_years):
    """Return an appropriate skill set for the tier."""
    skills = list(domain_info["fresher_skills"])
    if tier in ("junior", "mid", "senior"):
        skills += random.sample(domain_info["junior_skills"],
                                min(len(domain_info["junior_skills"]),
                                    random.randint(2, len(domain_info["junior_skills"]))))
    if tier in ("mid", "senior"):
        skills += random.sample(domain_info["mid_skills"],
                                min(len(domain_info["mid_skills"]),
                                    random.randint(2, len(domain_info["mid_skills"]))))
    if tier == "senior":
        skills += random.sample(domain_info["senior_skills"],
                                min(len(domain_info["senior_skills"]),
                                    random.randint(2, len(domain_info["senior_skills"]))))
    # Vary count slightly
    max_skills = min(len(skills), 5 + experience_years * 2)
    return random.sample(skills, min(len(skills), max(4, max_skills)))

def rand_company():
    return random.choice(COMPANIES)

def get_degree(domain_key, is_masters=False):
    """Pick a degree appropriate for the domain."""
    tech_domains = {"Software Engineering", "Data Science", "Web Development", "DevOps",
                    "Cybersecurity", "Mobile Development", "Database Administration",
                    "Cloud Engineering", "QA Engineering", "Healthcare IT"}
    if domain_key in tech_domains:
        if is_masters:
            return random.choice(DEGREES["tech_masters"])
        return random.choice(DEGREES["tech"])
    else:
        if is_masters:
            return random.choice(DEGREES["business_masters"])
        return random.choice(DEGREES["business"])

# ──────────────────────────────────────────────────────────────────────────────
# GENUINE RESUME GENERATOR (label = 0)
# ──────────────────────────────────────────────────────────────────────────────

def generate_genuine_resume():
    """Generate a logically consistent, genuine resume."""
    domain_key = random.choice(list(DOMAINS.keys()))
    domain = DOMAINS[domain_key]

    # Experience: weighted toward junior/mid
    experience_years = random.choices(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15],
        weights=[5, 10, 12, 12, 10, 10, 8, 8, 6, 5, 5, 5, 4],
        k=1
    )[0]

    tier = get_tier(experience_years)
    name = rand_name()
    grad_year = rand_year(2008, 2025) if experience_years > 0 else rand_year(2023, 2025)
    # Make sure experience starts after graduation
    if experience_years > 0:
        grad_year = min(grad_year, 2026 - experience_years)

    has_masters = experience_years >= 3 and random.random() < 0.3
    degree = get_degree(domain_key, is_masters=False)
    university = random.choice(UNIVERSITIES)
    education = f"{degree} from {university}, graduated {grad_year}"
    if has_masters:
        masters_degree = get_degree(domain_key, is_masters=True)
        masters_year = grad_year + random.randint(1, 3)
        if masters_year <= 2025:
            education += f". {masters_degree} from {random.choice(UNIVERSITIES)}, graduated {masters_year}"

    skills = get_skills_for_tier(domain, tier, experience_years)
    title = random.choice(domain["titles"][tier])

    # Build work experience entries
    work_entries = []
    remaining_years = experience_years
    current_year = 2026

    while remaining_years > 0:
        duration = min(remaining_years, random.choices([1, 2, 3, 4, 5], weights=[15, 25, 25, 20, 15], k=1)[0])
        if duration < 1:
            duration = 1
        entry_tier = get_tier(experience_years - remaining_years + duration)
        job_title = random.choice(domain["titles"][entry_tier])
        company = rand_company()
        city = random.choice(CITIES)
        end_year = current_year
        start_year = end_year - duration
        work_entries.append(
            f"{job_title} at {company}, {city} ({start_year}-{end_year})"
        )
        remaining_years -= duration
        current_year = start_year

    # Projects
    num_projects = min(len(domain["projects"]), random.randint(1, max(1, min(4, experience_years))))
    projects = [fill_project_template(p) for p in random.sample(domain["projects"], num_projects)]

    # Certifications
    cert_list = []
    cert_pool = "tech" if domain_key in {"Software Engineering", "Data Science", "Web Development",
                                          "DevOps", "Cybersecurity", "Mobile Development",
                                          "Database Administration", "Cloud Engineering",
                                          "QA Engineering", "Healthcare IT"} else "business"
    if experience_years >= 2 and random.random() < 0.4:
        cert_list = random.sample(CERTIFICATIONS[cert_pool],
                                  min(len(CERTIFICATIONS[cert_pool]), random.randint(1, 2)))

    # Compose resume text
    parts = [f"{name}. {title}."]
    parts.append(f"Education: {education}.")
    parts.append(f"Experience: {experience_years} years in {domain_key}.")
    if work_entries:
        parts.append("Work History: " + ". ".join(work_entries) + ".")
    parts.append("Skills: " + ", ".join(skills) + ".")
    if projects:
        parts.append("Projects: " + ". ".join(projects) + ".")
    if cert_list:
        parts.append("Certifications: " + ", ".join(cert_list) + ".")
    parts.append(f"Location: {random.choice(CITIES)}.")

    resume_text = " ".join(parts)

    return {
        "name": name,
        "education": education,
        "graduation_year": str(grad_year),
        "experience_years": str(experience_years),
        "skills": skills,
        "projects": projects,
        "resume_text": resume_text,
        "label": 0,
    }

# ──────────────────────────────────────────────────────────────────────────────
# FAKE RESUME GENERATOR (label = 1)
# ──────────────────────────────────────────────────────────────────────────────

FAKE_STRATEGIES = [
    "too_many_skills_for_fresher",
    "experience_before_graduation",
    "unrealistic_achievements",
    "senior_role_for_fresher",
    "short_durations_senior",
    "skill_overload",
    "impossible_timeline",
    "inflated_experience",
]

def generate_fake_resume():
    """Generate a resume with intentional red flags."""
    domain_key = random.choice(list(DOMAINS.keys()))
    domain = DOMAINS[domain_key]
    strategy = random.choice(FAKE_STRATEGIES)

    name = rand_name()
    grad_year = rand_year(2020, 2025)
    university = random.choice(UNIVERSITIES)
    degree = get_degree(domain_key)

    if strategy == "too_many_skills_for_fresher":
        experience_years = random.randint(0, 1)
        # Pile on advanced skills
        all_skills = (domain["fresher_skills"] + domain["junior_skills"] +
                      domain["mid_skills"] + domain["senior_skills"])
        skills = random.sample(all_skills, min(len(all_skills), random.randint(15, 25)))
        title = random.choice(domain["titles"]["fresher"])
        work_entries = [f"{title} at {rand_company()}, {random.choice(CITIES)} (2025-2026)"]
        projects = [fill_project_template(p) for p in random.sample(domain["projects"], min(2, len(domain["projects"])))]
        achievement = ""

    elif strategy == "experience_before_graduation":
        experience_years = random.randint(3, 8)
        grad_year = rand_year(2024, 2026)  # Recent grad
        tier = get_tier(experience_years)
        skills = get_skills_for_tier(domain, tier, experience_years)
        title = random.choice(domain["titles"][tier])
        # Work started well before graduation
        work_start = grad_year - experience_years - random.randint(1, 3)
        work_entries = [
            f"{random.choice(domain['titles']['junior'])} at {rand_company()}, {random.choice(CITIES)} ({work_start}-{work_start + 2})",
            f"{title} at {rand_company()}, {random.choice(CITIES)} ({work_start + 2}-2026)",
        ]
        projects = [fill_project_template(p) for p in random.sample(domain["projects"], min(3, len(domain["projects"])))]
        achievement = ""

    elif strategy == "unrealistic_achievements":
        experience_years = random.randint(1, 4)
        tier = get_tier(experience_years)
        skills = get_skills_for_tier(domain, tier, experience_years)
        title = random.choice(domain["titles"][tier])
        work_entries = [f"{title} at {rand_company()}, {random.choice(CITIES)} ({2026 - experience_years}-2026)"]
        projects = [fill_project_template(p) for p in random.sample(domain["projects"], min(2, len(domain["projects"])))]
        achievement = random.choice([
            f"Increased company revenue by {random.randint(300, 900)}% single-handedly",
            f"Reduced operational costs by ${random.randint(50, 200)}M through a single optimization",
            f"Led a team of {random.randint(200, 500)} engineers as a {title}",
            f"Filed {random.randint(20, 50)} patents in {experience_years} year(s)",
            f"Built a product generating ${random.randint(100, 500)}M in revenue within first year",
            f"Trained {random.randint(1000, 5000)} employees globally in first role",
            f"Awarded Employee of the Year {random.randint(5, 10)} times in {experience_years} years",
            f"Managed a budget of ${random.randint(50, 300)}M as a {title}",
            f"Personally responsible for saving the company ${random.randint(20, 100)}M",
            f"Published {random.randint(15, 40)} research papers while working full-time as {title}",
        ])

    elif strategy == "senior_role_for_fresher":
        experience_years = random.randint(0, 1)
        grad_year = rand_year(2024, 2025)
        skills = get_skills_for_tier(domain, "mid", 5)
        title = random.choice(domain["titles"]["senior"])
        work_entries = [f"{title} at {rand_company()}, {random.choice(CITIES)} ({grad_year}-2026)"]
        projects = [fill_project_template(p) for p in random.sample(domain["projects"], min(3, len(domain["projects"])))]
        achievement = ""

    elif strategy == "short_durations_senior":
        experience_years = random.randint(2, 5)
        skills = get_skills_for_tier(domain, "senior", 10)
        work_entries = []
        for i in range(random.randint(5, 8)):
            sr_title = random.choice(domain["titles"]["senior"] + domain["titles"]["mid"])
            year = 2026 - i
            months = random.randint(2, 4)
            work_entries.append(f"{sr_title} at {rand_company()}, {random.choice(CITIES)} ({months} months in {year})")
        title = random.choice(domain["titles"]["senior"])
        projects = [fill_project_template(p) for p in random.sample(domain["projects"], min(2, len(domain["projects"])))]
        achievement = ""

    elif strategy == "skill_overload":
        experience_years = random.randint(0, 2)
        all_skills_pool = []
        for d in DOMAINS.values():
            all_skills_pool += d["fresher_skills"] + d["junior_skills"] + d["mid_skills"] + d["senior_skills"]
        all_skills_pool = list(set(all_skills_pool))
        skills = random.sample(all_skills_pool, min(len(all_skills_pool), random.randint(20, 35)))
        title = random.choice(domain["titles"]["fresher"])
        work_entries = [f"Intern at {rand_company()}, {random.choice(CITIES)} (6 months in 2025)"]
        projects = []
        achievement = ""

    elif strategy == "impossible_timeline":
        experience_years = random.randint(8, 15)
        grad_year = rand_year(2022, 2025)  # Very recent grad claims lots of exp
        tier = "senior"
        skills = get_skills_for_tier(domain, "senior", experience_years)
        title = random.choice(domain["titles"]["senior"])
        work_entries = [
            f"{random.choice(domain['titles']['junior'])} at {rand_company()} ({grad_year - experience_years}-{grad_year - experience_years + 3})",
            f"{random.choice(domain['titles']['mid'])} at {rand_company()} ({grad_year - experience_years + 3}-{grad_year - 2})",
            f"{title} at {rand_company()} ({grad_year - 2}-2026)",
        ]
        projects = [fill_project_template(p) for p in random.sample(domain["projects"], min(3, len(domain["projects"])))]
        achievement = ""

    else:  # inflated_experience
        actual_years = random.randint(1, 3)
        experience_years = actual_years + random.randint(5, 10)
        tier = get_tier(experience_years)
        skills = get_skills_for_tier(domain, tier, experience_years)
        title = random.choice(domain["titles"][tier])
        work_entries = [f"{title} at {rand_company()}, {random.choice(CITIES)} ({2026 - actual_years}-2026)"]
        projects = [fill_project_template(p) for p in random.sample(domain["projects"], min(2, len(domain["projects"])))]
        achievement = ""

    education = f"{degree} from {university}, graduated {grad_year}"

    parts = [f"{name}. {title}."]
    parts.append(f"Education: {education}.")
    parts.append(f"Experience: {experience_years} years in {domain_key}.")
    if work_entries:
        parts.append("Work History: " + ". ".join(work_entries) + ".")
    parts.append("Skills: " + ", ".join(skills) + ".")
    if projects:
        parts.append("Projects: " + ". ".join(projects) + ".")
    if achievement:
        parts.append(f"Achievements: {achievement}.")
    parts.append(f"Location: {random.choice(CITIES)}.")

    resume_text = " ".join(parts)

    return {
        "name": name,
        "education": education,
        "graduation_year": str(grad_year),
        "experience_years": str(experience_years),
        "skills": skills,
        "projects": projects,
        "resume_text": resume_text,
        "label": 1,
    }

# ──────────────────────────────────────────────────────────────────────────────
# SUSPICIOUS RESUME GENERATOR (label = 2)
# ──────────────────────────────────────────────────────────────────────────────

SUSPICIOUS_STRATEGIES = [
    "slightly_inflated_skills",
    "title_one_rank_up",
    "missing_project_details",
    "short_tenures",
    "vague_descriptions",
    "minor_timeline_gap",
]

def generate_suspicious_resume():
    """Generate a borderline suspicious resume."""
    domain_key = random.choice(list(DOMAINS.keys()))
    domain = DOMAINS[domain_key]
    strategy = random.choice(SUSPICIOUS_STRATEGIES)

    name = rand_name()
    experience_years = random.randint(1, 8)
    tier = get_tier(experience_years)
    grad_year = rand_year(2012, 2024)
    grad_year = min(grad_year, 2026 - experience_years)

    university = random.choice(UNIVERSITIES)
    degree = get_degree(domain_key)
    education = f"{degree} from {university}, graduated {grad_year}"

    if strategy == "slightly_inflated_skills":
        # Has a few more skills than typical for their tier
        skills = get_skills_for_tier(domain, tier, experience_years)
        # Add 3-5 skills from the next tier
        next_tier_map = {"fresher": "junior", "junior": "mid", "mid": "senior", "senior": "senior"}
        next_key = next_tier_map[tier] + "_skills"
        extra = random.sample(domain[next_key], min(len(domain[next_key]), random.randint(3, 5)))
        skills = list(set(skills + extra))
        title = random.choice(domain["titles"][tier])
        work_entries = [f"{title} at {rand_company()}, {random.choice(CITIES)} ({2026 - experience_years}-2026)"]
        projects = [fill_project_template(p) for p in random.sample(domain["projects"], min(2, len(domain["projects"])))]

    elif strategy == "title_one_rank_up":
        # Title is one level above what experience warrants
        tier_up = {"fresher": "junior", "junior": "mid", "mid": "senior", "senior": "senior"}
        inflated_tier = tier_up[tier]
        skills = get_skills_for_tier(domain, tier, experience_years)
        title = random.choice(domain["titles"][inflated_tier])
        work_entries = [f"{title} at {rand_company()}, {random.choice(CITIES)} ({2026 - experience_years}-2026)"]
        projects = [fill_project_template(p) for p in random.sample(domain["projects"], min(2, len(domain["projects"])))]

    elif strategy == "missing_project_details":
        skills = get_skills_for_tier(domain, tier, experience_years)
        title = random.choice(domain["titles"][tier])
        work_entries = [f"{title} at {rand_company()}, {random.choice(CITIES)} ({2026 - experience_years}-2026)"]
        # List skill-heavy resume but very vague projects
        projects = [
            "Worked on various internal projects",
            "Contributed to team deliverables",
            "Participated in product development",
        ]

    elif strategy == "short_tenures":
        skills = get_skills_for_tier(domain, tier, experience_years)
        title = random.choice(domain["titles"][tier])
        work_entries = []
        for i in range(random.randint(3, 5)):
            t = random.choice(domain["titles"][tier])
            work_entries.append(f"{t} at {rand_company()}, {random.choice(CITIES)} ({random.randint(6, 10)} months in {2026 - i})")
        projects = [fill_project_template(p) for p in random.sample(domain["projects"], min(2, len(domain["projects"])))]

    elif strategy == "vague_descriptions":
        skills = get_skills_for_tier(domain, tier, experience_years)
        title = random.choice(domain["titles"][tier])
        work_entries = [f"{title} at {rand_company()}, {random.choice(CITIES)} ({2026 - experience_years}-2026)"]
        projects = [
            "Responsible for improving system efficiency",
            "Handled multiple client-facing deliverables",
            f"Used {random.choice(skills)} in day-to-day operations",
        ]

    else:  # minor_timeline_gap
        skills = get_skills_for_tier(domain, tier, experience_years)
        title = random.choice(domain["titles"][tier])
        # Small gap between graduation and first job
        gap = random.randint(1, 2)
        work_entries = [
            f"{random.choice(domain['titles']['fresher'])} at {rand_company()}, {random.choice(CITIES)} ({grad_year + gap}-{grad_year + gap + 2})",
            f"{title} at {rand_company()}, {random.choice(CITIES)} ({grad_year + gap + 2}-2026)",
        ]
        projects = [fill_project_template(p) for p in random.sample(domain["projects"], min(2, len(domain["projects"])))]

    parts = [f"{name}. {title}."]
    parts.append(f"Education: {education}.")
    parts.append(f"Experience: {experience_years} years in {domain_key}.")
    if work_entries:
        parts.append("Work History: " + ". ".join(work_entries) + ".")
    parts.append("Skills: " + ", ".join(skills) + ".")
    if projects:
        parts.append("Projects: " + ". ".join(projects) + ".")
    parts.append(f"Location: {random.choice(CITIES)}.")

    resume_text = " ".join(parts)

    return {
        "name": name,
        "education": education,
        "graduation_year": str(grad_year),
        "experience_years": str(experience_years),
        "skills": skills,
        "projects": projects,
        "resume_text": resume_text,
        "label": 2,
    }

# ──────────────────────────────────────────────────────────────────────────────
# MAIN — GENERATE EVERYTHING
# ──────────────────────────────────────────────────────────────────────────────

def main():
    random.seed(42)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    print("Generating 5,000 genuine resumes (label=0)...")
    genuine = [generate_genuine_resume() for _ in range(5000)]

    print("Generating 5,000 fake resumes (label=1)...")
    fake = [generate_fake_resume() for _ in range(5000)]

    print("Generating 2,000 suspicious resumes (label=2)...")
    suspicious = [generate_suspicious_resume() for _ in range(2000)]

    # ── JSON sample file (10 + 10 + 10) ──────────────────────────────────────
    sample_json = {
        "genuine_resumes": genuine[:10],
        "fake_resumes": fake[:10],
        "suspicious_resumes": [
            {"resume_text": s["resume_text"], "label": s["label"]}
            for s in suspicious[:10]
        ],
    }
    json_path = os.path.join(script_dir, "sample_resumes.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sample_json, f, indent=2, ensure_ascii=False)
    print(f"Saved 30 JSON samples → {json_path}")

    # ── CSV dataset ──────────────────────────────────────────────────────────
    all_resumes = genuine + fake + suspicious
    random.shuffle(all_resumes)

    csv_path = os.path.join(script_dir, "synthetic_resumes.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["id", "resume_text", "label"])
        for idx, resume in enumerate(all_resumes, start=1):
            writer.writerow([idx, resume["resume_text"], resume["label"]])

    print(f"Saved {len(all_resumes)} resumes → {csv_path}")
    print("Done!")

if __name__ == "__main__":
    main()
