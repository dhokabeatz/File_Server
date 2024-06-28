# File Server Project
File Server is a web application designed to facilitate the distribution and management of documents digitally. It allows businesses to upload documents such as wedding cards, admission forms, and more, which users can then access remotely.

## Description
A digital platform for easy document access and download. This platform will streamline the process of distributing documents to various users. This project is a web-based file server built with Django, allowing users to upload, manage, search, and share documents.

## Table of Contents


- [Features](#Features)
- [Installation](#installation)
- [Usage](#Usage)



## Features
* User authentication and authorization
* File uploading and management
* Searching and filtering documents
* Email integration for sharing files

## Installation

To get started with this project, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd file-server-project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Apply databse migrations
   ```bash
   python manage.py migrate

## Usage
1. Start the server
   ```bash
   python manage.py runserver
2. Access the application at  'http://localhost:8000/'.
