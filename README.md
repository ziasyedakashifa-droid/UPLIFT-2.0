# UPLIFT-2.0
# 🌸 UPLIFT 2.0 – AI-Powered Student Wellbeing Platform

### Empowering Students. Supporting Minds. Building a Better Campus.

UPLIFT 2.0 is an AI-powered student wellbeing platform designed to support students in managing their emotional wellbeing, tracking their moods, reflecting on their feelings and accessing human support when needed.

The platform combines Artificial Intelligence, web technologies and database management to create a student-friendly digital wellbeing environment.

It aims to make emotional wellbeing support more accessible, private and convenient for students.

---

# 📌 1. Problem Statement

Students frequently experience academic pressure, examination stress, anxiety, loneliness and other emotional challenges.

However, many students:

* Hesitate to discuss their emotional struggles.
* Do not have easy access to counselling services.
* Find it difficult to track their emotional wellbeing.
* Lack a private space to express their thoughts.
* May not recognise changes in their emotional patterns.

Traditional student support systems may not always provide convenient and continuous access to wellbeing resources.

### Our Solution

UPLIFT 2.0 provides a digital platform where students can:

* Track their daily moods.
* Express their thoughts through a private journal.
* Receive AI-generated reflections and suggestions.
* Request human support.
* Access their personal wellbeing dashboard.

---

# 🎯 2. Project Objectives

1. Develop an accessible student wellbeing platform.
2. Provide mood-tracking functionality.
3. Integrate AI-powered journal analysis.
4. Maintain individual student accounts.
5. Store student information in a database.
6. Provide a human-support request mechanism.
7. Encourage students to understand and monitor their emotional wellbeing.

---

# 💡 3. Main Features

## A. MoodMap – Mood Tracking

MoodMap allows students to record their current mood using a numerical scale from 1 to 5.

The application stores each mood check-in in the database.

Purpose:

* Encourage regular emotional self-reflection.
* Help students monitor mood patterns.
* Maintain a history of mood check-ins.

## B. MindMirror – AI-Powered Journal Analysis

MindMirror provides a space where students can write about their thoughts, experiences and feelings.

The journal analysis uses Google's Gemma open-weight AI model through Ollama.

The AI analyses the journal entry and returns structured information, including:

* Identified emotions.
* Possible stressors.
* Support messages.
* Suggestions.
* Human-support options.

The application also contains a basic phrase-based safety check that looks for certain urgent expressions and displays an appropriate support message.

**Important:** This is a hackathon prototype, not a clinical diagnosis or emergency detection system.

## C. HumanConnect – Human Support

HumanConnect allows students to submit requests for human support.

Students can:

* Describe their concerns.
* Provide optional contact information.
* Submit a support request.

The request is stored in the database.

Authorised counsellor accounts can access the submitted requests through the counsellor demonstration page.

## D. Student Authentication

UPLIFT includes an account system.

Students can:

* Create an account.
* Register using their name and email.
* Create a password.
* Log in using their registered credentials.
* Log out securely.

Passwords are stored as hashes using Werkzeug rather than being saved as plain text.

Each student's records are associated with their individual user ID.

---

# 🛠️ 4. Technologies Used

| Technology | Purpose                                  |
| ---------- | ---------------------------------------- |
| HTML5      | Structure of web pages                   |
| CSS3       | Website styling and responsive design    |
| JavaScript | Frontend interactivity where implemented |
| Python     | Main programming language                |
| Flask      | Backend web framework                    |
| SQLite     | Database management                      |
| Gemma 4    | AI model for journal analysis            |
| Ollama     | Running and accessing the AI model       |
| Werkzeug   | Password hashing and verification        |
| Jinja2     | Dynamic HTML rendering                   |
| GitHub     | Source-code management                   |
| Gunicorn   | Production WSGI server for deployment    |

---

# 🏗️ 5. System Architecture

UPLIFT 2.0 follows a client-server architecture.

### Frontend Layer

The frontend is developed using HTML, CSS and JavaScript.

It provides the user interface for:

* Registration.
* Login.
* Mood tracking.
* Journal entries.
* Human support requests.

### Backend Layer

The backend is developed using Python and Flask.

It handles:

* HTTP requests.
* User authentication.
* Session management.
* Form validation.
* Database operations.
* AI integration.
* Application routing.

### Database Layer

SQLite is used to store application data.

The database contains tables for:

* Users.
* Mood records.
* Journal records.
* Human-support requests.

### AI Layer

Gemma is accessed through Ollama.

The backend sends journal content to the AI model and receives structured analysis.

### System Flow

Student
↓
Frontend (HTML, CSS, JavaScript)
↓
Flask Backend (Python)
↓
Authentication and Application Logic
↓
SQLite Database / Gemma AI
↓
Processed Results
↓
Frontend Displays Results

---

# 📂 6. Project Folder Structure

```text
UPLIFT_AI_Starter/
│
├── app.py
│
├── database.py
│
├── gemma.py
│
├── safety.py
│
├── requirements.txt
│
├── .env
│
├── .env.example
│
├── uplift_demo.db
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── journal.html
│   ├── support.html
│   └── counsellor.html
│
└── static/
    └── style.css
```

Some files, such as `.env` and `uplift_demo.db`, are created locally and should not be uploaded publicly.

---

# 🧩 7. Explanation of Important Source Files

## 7.1 app.py – Main Backend File

`app.py` is the central file of the application.

It connects the frontend, database, authentication system, AI functionality and application routes.

### Main responsibilities

**1. Importing libraries**

Imports Flask functions, operating-system utilities, regular expressions, session management and password-hashing functions.

**2. Application initialisation**

Creates the Flask application and configures its secret key.

**3. Database initialisation**

Calls `init_db()` to create the necessary database tables if they do not already exist.

**4. Login protection**

The `login_required` decorator checks whether a user has logged in before accessing protected pages.

If a user is not authenticated, they are redirected to the login page.

**5. User registration**

The `/signup` route:

* Accepts registration details.
* Validates the submitted information.
* Checks whether the email already exists.
* Hashes the password.
* Creates a new account.
* Starts the user's session.

**6. User login**

The `/login` route verifies the submitted email and password.

It uses Werkzeug's `check_password_hash()` function to compare the password with its stored hash.

**7. Logout**

The `/logout` route clears the current session.

**8. Dashboard**

The `/dashboard` route retrieves the logged-in student's mood history and displays the personal dashboard.

**9. Mood tracking**

The `/mood` route validates the mood score and stores it in the database.

**10. Journal analysis**

The `/journal` route:

* Receives the journal entry.
* Checks its length.
* Runs the basic safety check.
* Calls the Gemma analysis function when appropriate.
* Saves the resulting journal information.

**11. HumanConnect**

The `/support` route accepts support requests and saves them in SQLite.

**12. Counsellor access**

The `/counsellor` route checks whether the logged-in user's email is included in the configured counsellor email list.

Only authorised accounts can access this demonstration page.

---

## 7.2 database.py – Database Management

This file manages the SQLite database.

It handles the creation, insertion and retrieval of application records.

### Database Tables

**Users Table**

| Column        | Description           |
| ------------- | --------------------- |
| id            | Unique student ID     |
| name          | Student name          |
| email         | Registered email      |
| password_hash | Hashed password       |
| created_at    | Account creation time |

**Moods Table**

| Column     | Description           |
| ---------- | --------------------- |
| id         | Unique mood record ID |
| user_id    | Associated student ID |
| score      | Mood score            |
| created_at | Date and time         |

**Journals Table**

| Column     | Description                       |
| ---------- | --------------------------------- |
| id         | Unique journal ID                 |
| user_id    | Associated student ID             |
| entry      | Journal text                      |
| emotions   | Analysed emotions in JSON format  |
| stressors  | Analysed stressors in JSON format |
| created_at | Date and time                     |

**Requests Table**

| Column     | Description                  |
| ---------- | ---------------------------- |
| id         | Unique request ID            |
| user_id    | Associated student ID        |
| concern    | Student's concern            |
| contact    | Optional contact information |
| status     | Request status               |
| created_at | Submission time              |

### Important Database Functions

* `init_db()` – Creates database tables.
* `create_user()` – Registers a new user.
* `get_user_by_email()` – Retrieves an account using its email.
* `get_user_by_id()` – Retrieves a user using their ID.
* `save_mood()` – Stores mood records.
* `get_moods()` – Retrieves mood history.
* `save_journal()` – Stores journal analysis information.
* `create_support_request()` – Stores support requests.
* `get_support_requests()` – Retrieves support requests for authorised counsellor access.

SQLite is a relational database management system that stores information in tables.

---

## 7.3 gemma.py – Artificial Intelligence Integration

This file connects the Flask application to the Gemma AI model through Ollama.

### How it works

1. The student submits a journal entry.
2. Flask receives the journal text.
3. The backend calls the `analyse_journal()` function.
4. The function sends the journal content to the Ollama API.
5. Gemma processes the input.
6. The model returns a structured JSON response.
7. The backend validates and processes the response.
8. The result is displayed on the MindMirror page.

### Why Gemma?

Gemma is an open-weight family of AI models that can be run locally using Ollama.

It allows the project to perform AI-based text analysis without requiring a paid hosted AI API.

In our prototype, the model runs on a separate laptop and the Flask application communicates with it through a local network.

---

## 7.4 safety.py – Basic Safety Check

This file contains a phrase-based safety checking mechanism.

It checks journal entries for certain predefined urgent expressions.

When a matching expression is found, the application displays a predefined support message instead of relying solely on the AI response.

This is a basic demonstration mechanism.

It does not understand every possible expression of distress and must not be considered a reliable crisis-detection system.

---

## 7.5 templates/ – Frontend HTML Files

The `templates` folder contains the HTML pages rendered by Flask.

| File            | Purpose                                      |
| --------------- | -------------------------------------------- |
| base.html       | Common layout, header, navigation and footer |
| index.html      | Public landing page                          |
| login.html      | Student login page                           |
| signup.html     | Student registration page                    |
| dashboard.html  | Personal wellbeing dashboard                 |
| journal.html    | MindMirror journal interface                 |
| support.html    | HumanConnect support form                    |
| counsellor.html | Counsellor demonstration dashboard           |

### Jinja2 Integration

The templates use Jinja2 syntax to display dynamic information.

Examples:

* `{% extends "base.html" %}` – Inherits the common page layout.
* `{% block content %}` – Defines the page-specific content.
* `{{ user.name }}` – Displays the logged-in user's name.
* `{% if session.get('user_id') %}` – Conditionally displays navigation links.

---

## 7.6 static/style.css – Styling

This file controls the visual appearance of UPLIFT.

It includes:

* Colours and theme variables.
* Typography.
* Header and navigation styling.
* Cards and panels.
* Buttons.
* Forms and input fields.
* Authentication page styling.
* Responsive layouts for smaller screens.

The design uses a calming lavender and mint-inspired colour palette to create a welcoming wellbeing environment.

---

# 🔄 8. Application Workflow

### Student Registration

Student opens UPLIFT
↓
Clicks Sign Up
↓
Enters name, email and password
↓
Backend validates information
↓
Password is hashed
↓
Account is stored in SQLite
↓
Student is redirected to the dashboard

### Student Login

Student enters email and password
↓
Flask retrieves the account
↓
Password hash is verified
↓
Session is created
↓
Student accesses their dashboard

### MoodMap Workflow

Student selects a mood score
↓
Flask validates the score
↓
Database stores the mood record
↓
Dashboard displays mood history

### MindMirror Workflow

Student writes a journal entry
↓
Backend receives the text
↓
Safety check is performed
↓
Gemma analyses the entry if appropriate
↓
Structured results are received
↓
Results are displayed to the student
↓
Journal analysis information is stored

### HumanConnect Workflow

Student submits a support request
↓
Backend validates the request
↓
Request is stored in SQLite
↓
Authorised counsellor can view requests

---

# 🗄️ 9. Database Architecture

UPLIFT uses SQLite.

SQLite is a lightweight relational database that does not require a separate database server.

The application uses a database file named:

`uplift_demo.db`

### Relationship Between Tables

* One user can have multiple mood records.
* One user can have multiple journal records.
* One user can submit multiple support requests.

The `user_id` column associates each record with its student account.

This allows the application to retrieve personal records belonging to the logged-in student.

---

# 🔐 10. Security Features

The prototype includes several basic security mechanisms.

1. Password hashing using Werkzeug.
2. Login-required decorators for private routes.
3. Flask session management.
4. Input validation for important form fields.
5. Parameterised SQL queries.
6. Separate user IDs for student records.
7. Counsellor email-based access restrictions.
8. HTTP-only session cookie configuration.

### Current Limitations

This is a hackathon prototype, not a production-ready application.

Before real-world use, additional protections are necessary:

* Email verification.
* CSRF protection.
* Login rate limiting.
* Stronger role-based access controls.
* Secure HTTPS deployment.
* Database backups.
* Data retention and deletion policies.
* Encryption and privacy controls.
* Reliable crisis-support procedures.

Real student mental-health information should not be entered into an unsecured demonstration deployment.

---

# ⚙️ 11. Installation and Setup

### Prerequisites

Install the following:

* Python 3.
* Visual Studio Code.
* Git.
* Ollama.
* A compatible Gemma model.

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Enter the Project Directory

```bash
cd UPLIFT_AI_Starter
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Environment

Windows:

```bash
.venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Environment Variables

Create a `.env` file in the project directory.

Configure a strong Flask secret key and any other settings required by the application.

Never upload this file to a public GitHub repository.

### Step 7: Configure Ollama

Install Ollama and download the required model.

The current prototype uses:

`gemma4:e2b`

Ensure the Ollama server is running and the API endpoint configured in `gemma.py` is reachable from the Flask application.

### Step 8: Start the Application

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:5000
```

---

# 🚀 12. Deployment

The application uses Flask and can be deployed to a Python-compatible hosting platform.

For a typical Gunicorn deployment:

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app:app
```

Deployment also requires:

* A stable Flask secret key.
* Correct environment variables.
* Persistent database storage or a hosted database.
* An accessible AI service endpoint.
* Appropriate security configuration.

The current Ollama configuration uses a private local-network IP address. It must be changed before a public deployment can access the AI service.

SQLite also requires persistent storage if student records must survive hosting restarts.

---

# 🌍 13. Future Enhancements

We aim to improve UPLIFT with:

1. Email OTP verification.
2. A more advanced mood analytics dashboard.
3. Mood trend visualisations.
4. Secure cloud database integration.
5. Improved AI-based emotional reflection.
6. Appointment scheduling with counsellors.
7. Notifications and reminders.
8. Multilingual support.
9. Better accessibility features.
10. Privacy-focused student data management.

---

# 👥 14. Project Team

**Project Name:** UPLIFT 2.0

**Domain:** Artificial Intelligence / Student Wellbeing / Web Development

**Project Type:** Full-Stack Web Application

**Development Approach:** Collaborative hackathon project.

---

# 🏆 15. Innovation and Impact

UPLIFT 2.0 combines AI-assisted journal reflection, mood tracking and human-support requests in one student-oriented platform.

Its main innovation is bringing multiple student wellbeing functions together rather than treating mood tracking, journaling and human support as separate activities.

### Expected Impact

* Encourages emotional self-awareness.
* Promotes regular wellbeing check-ins.
* Makes self-reflection more accessible.
* Provides a channel for requesting human support.
* Encourages a more supportive campus environment.

---

# 📜 16. Disclaimer

UPLIFT 2.0 is an educational hackathon prototype.

It is not a medical application, diagnostic tool, therapy service or emergency response system.

AI-generated responses may be inaccurate or incomplete. Students experiencing serious distress should contact trusted people and qualified professionals or appropriate emergency services.

---

# ❤️ Conclusion

UPLIFT 2.0 represents our effort to combine technology and student wellbeing.

Through Artificial Intelligence, full-stack development and database integration, we aim to create a supportive digital environment where students can reflect, track their moods and reach out for human assistance.

**UPLIFT 2.0 – Because Every Student's Wellbeing Matters.**
