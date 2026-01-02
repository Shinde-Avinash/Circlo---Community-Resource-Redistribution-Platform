# 🌍 Circlo  
## ♻️ Community Resource Redistribution Platform

**Circlo** is a hyperlocal PWA-enabled web application designed to redistribute surplus resources such as **food, clothing, furniture, and essentials** within local communities.  
It connects **donors with people in need**, reducing waste while strengthening community support ❤️

---

## ✨ Features
<img width="1365" height="766" alt="Circlo Preview" src="https://github.com/user-attachments/assets/af8b82ac-f376-45c5-adc3-ed8e6b6106ff" />

📱 **Installable App (PWA)**
-   **Add to Home Screen**: Install like a native app on iOS and Android.
-   **Offline Support**: Works even with spotty internet connections.
-   **App-like UI**: Standalone experience without browser bars.

🔐 **User Roles**  
- Donors, Recipients, Organizations, and Moderators  
- Role-based access and permissions  

📍 **Hyperlocal Feed**  
- Resources sorted by **distance and urgency**  
- Powered by the **Haversine formula**

📦 **Resource Management**  
- Post items with images, categories, and urgency levels  

🔄 **Claim System**  
- Automated **Claim / Unclaim** workflow  
- Real-time availability updates  

💬 **In-App Messaging**  
- Private chat between donors and recipients  
- Easy coordination for pickups  

🛡️ **Admin Dashboard**  
- Manage users, resources, and platform activity  

🎨 **Responsive UI**  
- Modern **Cognizant-themed** design  
- 🌙 Dark Mode & ☀️ Light Mode support  
- Fully mobile-responsive  

---

## 🧰 Tech Stack

- **Backend** 🧠: Django (Python 3.10+)  
- **Frontend** 🎨: HTML5, CSS3 (Custom Variables), HTMX  
- **Database** 🗄️: SQLite (Development)  
- **Geolocation** 🧭: HTML5 Geolocation API + Server-side distance calculation  
- **PWA** 🚀: Service Workers, Web App Manifest, Cache API

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/circlo.git
cd circlo
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install django pillow
```

### 4️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6️⃣ Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## 📂 Project Structure

*   `core/`: Main app handling the Home feed, Templates, PWA assets (sw.js, manifest), and static files.
*   `users/`: User authentication, profiles, and role management.
*   `resources/`: Resource CRUD operations, logic for posting and claiming items.
*   `messaging/`: Real-time internal messaging system.
*   `crrp/`: Project configuration settings.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---
*Built with ❤️ for the Future of Community Sharing.*