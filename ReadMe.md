# 🎵 Tron Music App

A Django-based web application that allows users to upload, store, and play music files on the cloud. Due to limitations of using a free database hosting service, the app has certain restrictions related to file storage and database expiration times. This project serves as a demonstration of cloud-based file storage and audio streaming using Django.

---

## 🚀 Features
- **Upload Music**: Users can upload their music files to the cloud.
- **Play Music**: Stream uploaded music files directly from the web interface.
- **File Management**: Manage and view uploaded music files in a user-friendly dashboard.
- **Expiration of Data**: Due to limitations of the free database host, stored files and data will expire or be cleared after a certain period.

---

## ⚠️ Limitations
- **Free Database Hosting**: The app is currently hosted on a free database service, which imposes several limitations:
  - **Storage Restrictions**: The database may have limited storage, affecting the number of music files that can be uploaded.
  - **Data Expiration**: Data, including user information and uploaded files, may be deleted or become inaccessible after a short period due to host limitations.
  - **File Expiration**: Music files stored in the database may expire within a few hours or days, depending on the hosting provider’s policies.
- **Limited Scalability**: The app is designed for demo purposes and may not handle a large number of users or file uploads.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.x
- Django 3.x or higher
- PostgreSQL or any supported database for production
- A cloud storage provider (e.g., Amazon S3) for media file storage (optional)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BlacAc3/MusicCloud
   cd MusicCLoud
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the database:**
   Update your `DATABASES` configuration in `settings.py` to point to your chosen database. For a local setup, you can use SQLite, but for production, a cloud-hosted database (e.g., PostgreSQL) is recommended.

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the app in the browser:**
   Open `http://127.0.0.1:8000` in your browser to view the application.

---

## 🏗️ Technologies Used
- **Backend**: Django (Python)
- **Database**: SQLite (for development), PostgreSQL (for production)
- **Front-end**: HTML5, CSS (Tailwind CSS), JavaScript
- **Cloud Storage**: Optional integration with services like Google Cloud Storage for storing media files

---

## 📦 Deployment
To deploy the app on a cloud platform (e.g., Heroku, DigitalOcean), follow the specific hosting provider's Django deployment guide. You will need to:
- Set up a database (e.g., PostgreSQL).
- Configure a cloud-based storage service for storing media files (e.g., S3).
- Set `DEBUG = False` and configure `ALLOWED_HOSTS` in your `settings.py`.

---

## 📝 License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## 💡 Notes
- This app is not designed for production use due to the limitations of the free database hosting service.
- Data loss or expiration can occur frequently due to free-tier hosting constraints.
- For a scalable and permanent solution, consider switching to a paid database and file storage service.

---

## ✨ Future Improvements
- Integrate cloud storage solutions (e.g., Amazon S3) to handle file storage more effectively.
- Use a more robust database with less frequent expiration, such as a paid PostgreSQL instance.
- Add user authentication and permissions for uploading and managing files.

---
