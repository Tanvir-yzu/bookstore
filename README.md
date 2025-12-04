# Bookstore Django Application

A comprehensive bookstore management system built with Django, allowing users to browse books, manage authors, customers, and orders.

## Features

- **Book Management**: Add, edit, delete, and view books with details including title, author, description, price, stock, and cover photo
- **Author Management**: Manage author information and their associated books
- **Customer Management**: Track customer details and their order history
- **Order Processing**: Create orders, add books to orders, and calculate totals
- **Search Functionality**: Search books by title, author, or description
- **User Authentication**: Protected admin-only views for managing content

## Tech Stack

- **Framework**: Django 5.2.1
- **Database**: SQLite (default, easily configurable to other databases)
- **Frontend**: HTML, Tailwind CSS, Alpine.js
- **File Handling**: Pillow for image processing

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd bookstore
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations to create database tables:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
bookstore/
├── bookstore/              # Project settings directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py
├── store/                  # Main application directory
│   ├── __init__.py
│   ├── admin.py            # Admin configuration
│   ├── apps.py
│   ├── forms.py            # Form definitions
│   ├── migrations/         # Database migrations
│   ├── models.py           # Data models
│   ├── templates/          # HTML templates
│   │   └── store/
│   ├── tests.py
│   ├── urls.py             # App URL configuration
│   └── views.py            # View functions and classes
├── manage.py               # Django command-line utility
└── requirements.txt        # Project dependencies
```

## Key Models

1. **Author**: Stores author information (name, biography)
2. **Book**: Contains book details with a foreign key to Author
3. **Customer**: Stores customer information
4. **Order**: Represents a customer order with a foreign key to Customer
5. **OrderItem**: Individual items within an order, linking Orders and Books

## Usage

### Browsing the Store

- Visit the home page to see recently added books
- Browse all books using the "Books" navigation link
- View author details and their books through the "Authors" section

### Managing Content (Admin Users)

- Add new books, authors, customers, and orders through the respective forms
- Edit existing records using the "Edit" buttons
- Delete records using the "Delete" buttons
- Process orders by adding books and quantities

## Screenshots

*(Add screenshots of your application here)*

1. Home Page: Shows recently added books and featured content
2. Book List: Grid view of all books with filtering options
3. Book Detail: Detailed view of a book with edit options for admins
4. Author Detail: Author information with their published books
5. Order Management: Interface for creating and managing customer orders

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django documentation and community
- Tailwind CSS for styling
- Alpine.js for interactive components
