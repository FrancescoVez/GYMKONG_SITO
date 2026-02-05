# GYMKONG_SITO
 GymKong — Web Technologies Project (Flask)

GymKong is a **real-world inspired** web application for a premium fitness club.  
The project is built with **Python Flask** and includes **user authentication**, **admin management**, and a modern **GymKong-style UI**

---

## Project Proposal 

GymKong brings the “premium gym experience” online: users can explore the gym, courses, planning and promotions, while staff (admin) can manage registered users from an internal panel.  
The UI is designed to match the GymKong identity and the app is structured to be reproducible and deployable following this README.

---

## Key Features

- **Public pages**
  - Home
  - Courses
  - Planning
  - The Center
  - The Tribe
  - Highlights / Promotions
  - Contacts

- **Authentication**
  - Register
  - Login
  - Logout
  - Session-based auth with `flask-login`

- **Admin Panel**
  - View registered users
  - Create users
  - Reset user password
  - Delete users  
  *(admin routes protected on backend)*

- **UI / Frontend**
  - GymKong gold theme
  - Responsive layout
  - Logo dropdown actions (Login/Register/Logout/Admin links)

---

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite (SQLAlchemy)
- **Auth:** Flask-Login, Werkzeug password hashing
- **Templates:** Jinja2
- **Styling:** Custom CSS (GymKong theme)

---

## Repository Structure 
├── app.py
├── models.py
├── auth_forms.py
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── corsi.html
│ ├── planning.html
│ ├── tribu.html
│ ├── evidenza.html
│ ├── contatti.html
│ ├── auth_login.html
│ ├── auth_register.html
│ └── admin_users.html
├── static/
│ ├── style.css
│ ├── img/
│ └── video/
└── .env
## Running (Local)

## 1) Clone the repository

##2) Create a virtual environment (recommended)
python -m venv .venv


Activate it:

Windows (PowerShell)

.\.venv\Scripts\Activate.ps1


macOS / Linux

source .venv/bin/activate

##3) Install dependencies
pip install -r requirements.txt


If you don’t have a requirements.txt yet, you can generate it after installing your libs:

pip freeze > requirements.txt

##4) Create the .env file

Create a file named .env in the project root:

FLASK_ENV=development
FLASK_DEBUG=1

# Flask secret key (change in production)
SECRET_KEY=gymkong-super-secret-key-change-in-production

# Database (coherent with app.py: reads DATABASE_URL)
DATABASE_URL=sqlite:///site.db

##5) Run the application
python app.py


Then open:

http://127.0.0.1:5000


##Database Notes

The SQLite database file is typically created at:

./instance/site.db (common with Flask)

or in the project root ./site.db (depending on config)

If you want to reset the database locally, stop the server and delete site.db (wherever it is created), then run the app again.

##Admin Access

The project includes an admin panel protected by login and admin checks.
Depending on your final implementation, you may have:

a default admin created at startup (example: admin@gymkong.it)

or admin users created manually via database/admin form

Make sure to change default credentials before production deployment.

##Presentation

Course slides (e-learning): https://elearning.uniparthenope.it/course/view.php?id=121

Google Drive folder: https://drive.google.com/drive/folders/13hiYKp-IJMY78Nhs6PsWJJw_K4MrKhKZ?usp=sharing

GitHub repository: https://github.com/informatica-uniparthenope/TW6

##Resources Used

Miguel Grinberg — Flask Mega Tutorial
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Aaron Luna — Flask API Tutorial (JWT)
https://aaronluna.dev/series/flask-api-tutorial/overview/

W3Schools
https://w3schools.com

##Authors / Developers

Domenico Paduano — Matricola 2989

Francesco Vezzuto — Matricola 3205

Francesca Anelli — Matricola 3138


