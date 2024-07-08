# File Server

File Server is a web application designed to facilitate the distribution and management of documents digitally. It allows businesses to upload documents such as wedding cards, admission forms, and more, which users can then access remotely. This platform will streamline the process of distributing documents to various users, providing a digital platform for easy document access and download.

## Key Features

### User Features
1. **User Authentication**: Users can sign up and log in with an email and password. An account verification feature ensures secure access.
2. **Password Recovery**: Users can reset their password if they forget it.
3. **Document Feed**: Users can see a feed page containing a list of files available for download.
4. **Search Functionality**: Users can search the file server to find specific documents.
5. **Email Sharing**: Users can send a file to an email through the platform.

### Admin Features
1. **File Upload**: Admins can upload files with a title and description.
2. **Analytics**: Admins can see the number of downloads and emails sent for each file.

## Prerequisites

- Python 3.x
- Django
- SQL
- HTML
- JavaScript
- CSS
- Bootstrap

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/File_Server.git
   cd File_Server
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

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

7. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000`.

## Usage

### User Guide

1. **Sign Up**: Create an account by signing up with an email and password.
2. **Log In**: Log in with your credentials.
3. **View Files**: Browse the feed page to see available files.
4. **Search**: Use the search bar to find specific documents.
5. **Download**: Click on a file to download it.
6. **Email a File**: Use the email feature to send a file to a recipient.

### Admin Guide

1. **Log In as Admin**: Use your admin credentials to log in.
2. **Upload Files**: Go to the upload page to add new files.
3. **View Analytics**: Check the number of downloads and emails sent for each file.

## Project Structure

```
File-Server/
├── backend/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── activation_email.html
│   ├── add_file.html
│   ├── adminDashboard.html
│   ├── base.html
│   ├── confirmation_sent.html
│   ├── delete_file.html
│   ├── edit_file.html
│   ├── email_form.html
│   ├── landing_page.html
│   ├── login_page.html
│   ├── reset_password.html
│   ├── signUp_page.html
│   └── userdashboard_page.html
├── FileServer/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

## Contributing

1. **Fork the repository**.
2. **Create a new branch** (`git checkout -b feature-branch`).
3. **Make your changes**.
4. **Commit your changes** (`git commit -m 'Add some feature'`).
5. **Push to the branch** (`git push origin feature-branch`).
6. **Open a pull request**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
