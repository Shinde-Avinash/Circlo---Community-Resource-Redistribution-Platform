### Circlo - Community Resource Redistribution Platform

Circlo is a hyperlocal web application designed to facilitate the redistribution of surplus resources (food, clothing, furniture, etc.) within a community. It connects donors with individuals in need, promoting sustainability and community support.

## 🚀 Features
<img width="1352" height="592" alt="image" src="https://github.com/user-attachments/assets/65462d1f-5ae1-4003-b99a-06fb3547ebe4" />

*   **User Roles**: Distinct roles for Donors, Recipients, Organizations, and Moderators.
*   **Hyperlocal Feed**:  Resources are sorted by proximity (using Haversine formula) and urgency.
*   **Resource Management**: Users can post items with images, categorization, and urgency levels.
*   **Claim System**:  Automated "Claim" and "Unclaim" workflows with real-time inventory updates.
*   **In-App Messaging**: Private chat system for donors and claimants to coordinate pickup.
*   **Admin Dashboard**: comprehensive dashboard for moderators to manage users and content.
*   **Responsive UI**:  Modern, "Cognizant-themed" interface with Dark/Light mode support.

## 🛠️ Tech Stack

*   **Backend**: Django (Python 3.10+)
*   **Frontend**: HTML5, CSS3 (Custom Variables), HTMX (for dynamic interactions)
*   **Database**: SQLite (Development)
*   **Geolocation**:  HTML5 Geolocation API + Server-side distance calculation.

## 📦 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/circlo.git
    cd circlo
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install django pillow
    ```

4.  **Apply Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run Development Server**
    ```bash
    python manage.py runserver
    ```

    Visit `http://127.0.0.1:8000/` in your browser.

## 📂 Project Structure

*   `core/`: Main app handling the Home feed, Templates, and static assets.
*   `users/`: User authentication, profiles, and role management.
*   `resources/`: Resource CRUD operations, logic for posting and claiming items.
*   `messaging/`: Real-time internal messaging system.
*   `crrp/`: Project configuration settings.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---
*Built for the Future of Community Sharing.*
