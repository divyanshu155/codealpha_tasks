# Mini Social Media Platform (Django + HTML/CSS/JS)

Welcome to the **Mini Social Media Platform**, a full-stack social web application built with Python **Django 6.0**, **SQLite**, and a modern glassmorphic **HTML, CSS, and JavaScript** single-page feel frontend.

## 🚀 Features

- **User Authentication**: Secure Registration, Login, and Logout functionality.
- **Customizable User Profiles**: User profiles with custom avatars, location, bio, and real-time post/follower/following counters.
- **Posts & Micro-Feed**: Create, publish, and view text posts with real-time timestamps.
- **AJAX Like System**: Like/Unlike posts with dynamic heart animations and instant counter updates.
- **Collapsible Comments**: Comment section under each post with dynamic AJAX comment submission without page reload.
- **Follow / Unfollow System**: Discover community members and follow/unfollow users with real-time stats updates.
- **Glassmorphism UI**: Premium dark slate design system (`#0f172a`), Inter typography, floating toast notifications, and smooth animations.

---

## 🛠️ Technologies Used

- **Backend**: Python 3.13, Django 6.0
- **Database**: SQLite (`db.sqlite3`)
- **Frontend**: HTML5, CSS3 (Glassmorphism design system), JavaScript (Fetch AJAX APIs)

---

## 💻 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/divyanshu155/codealpha_tasks.git
cd codealpha_tasks/codealpha-social-media-app
```

### 2. Apply Database Migrations
```bash
python manage.py migrate
```

### 3. Seed Sample Data (Optional)
Populate test users, sample posts, and follow connections:
```bash
python seed.py
```

### 4. Start the Django Server
```bash
python manage.py runserver 8000
```

Open your browser and navigate to: **`http://127.0.0.1:8000`**

---

## 🔑 Pre-seeded Demo Accounts

| Username | Password | Bio |
| :--- | :--- | :--- |
| `alex_dev` | `password123` | Full-stack software engineer & open source enthusiast |
| `sarah_design` | `password123` | UI/UX designer crafting beautiful digital experiences |
| `tech_lead_jon` | `password123` | Building distributed systems & scaling web applications |

---

## 📄 License
This project is licensed under the MIT License.
