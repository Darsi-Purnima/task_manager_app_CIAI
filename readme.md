# Web-Based Task Management Application

Welcome to TaskManager, a web application developed to facilitate efficient task tracking and management. This project was undertaken as part of an assignment for [CustomerInsights.ai](https://www.customerinsights.ai/). Built using Python and the Flask framework, this application aims to provide a functional and user-friendly experience.

TaskManager enables users to register for an account, log in, and subsequently manage their tasks through creation, viewing, modification, and deletion. The dashboard serves as a centralized interface for all task-related activities, incorporating features for filtering and sorting.

## Core Features

* **User Authentication System:**
    * Secure user registration with unique usernames and robust password hashing.
    * Password complexity enforcement (minimum length of 6 characters).
    * Session-based login and logout functionality, managed by [Flask-Login](https://flask-login.readthedocs.io/).
    * Informative feedback messages for invalid login attempts.
* **Task Management (CRUD Operations):**
    * **Create:** Define new tasks with attributes such as title, description (optional), due date, and status.
    * **Read:** Access and view a comprehensive list of all personal tasks via a dedicated dashboard.
    * **Update:** Modify existing task details including title, description, due date, and status as requirements change.
    * **Delete:** Remove tasks upon completion or if no longer relevant, with a confirmation prompt to prevent accidental deletion.
    * All tasks are user-specific, ensuring data privacy and focused management.
* **Dashboard & User Interface:**
    * A clean, contemporary user interface design, with a color scheme derived from the [Customer Insights AI](https://www.customerinsights.ai/) logo (primary blue: `#0064A7`, accent orange/yellow: `#F69522`).
    * A fixed left-aligned sidebar for consistent and accessible navigation.
    * Content organized within a card-based layout for clarity.
    * Tasks are displayed with essential information: Title, Due Date, and Status.
    * **Filtering:** Users can filter the task list by status (All, Pending, Completed).
    * **Sorting:** Tasks can be sorted by Title, Due Date, or Status in both ascending and descending order.
    * Responsive design elements implemented using [Bootstrap 5](https://getbootstrap.com/).
* **Data Persistence:**
    * Utilizes [SQLAlchemy](https://www.sqlalchemy.org/), an Object Relational Mapper (ORM), for database interactions.
    * Employs a [SQLite](https://www.sqlite.org/) database, providing a simple, file-based storage solution suitable for personal or small-scale applications.
    * Clearly defined User and Task data models with an established one-to-many relationship.

## Project Structure

The application's file and directory organization is as follows:

<pre> <code>task_management_app/ 
├── app.py # Main Flask application 
├── requirements.txt # Project dependencies 
├── instance/ # SQLite DB & instance-specific files 
├── static/ 
    │ ├── css/ 
    │ │ └── custom.css # Custom theme styles 
    │ └── img/ │ └── logo.png # Application logo 
└── templates/ ├── base.html # Base template layout 
├── dashboard.html # Task dashboard 
├── login.html # Login page 
├── register.html # Registration page 
└── add_edit_task.html # Task creation/edit form </code> </pre>


## Setup and Installation Guide

To set up and run the TaskManager application on your local development environment, please follow these instructions:

### Prerequisites

* [Python](https://www.python.org/downloads/) (Version 3.8 or higher recommended)
* `pip` (Python package installer, typically included with Python distributions)
* A virtual environment management tool (e.g., `venv` module, `conda`). Utilization of a virtual environment is strongly recommended to manage project dependencies effectively.

### Installation Procedure

1.  **Project File Configuration:**
    * Create a root directory for the project (e.g., `task_management_app`).
    * Replicate the directory and file structure as detailed in the "Project Structure" section within this root directory.
    * Populate each file with the provided source code.
    * **Logo Asset:** Ensure the application logo (`logo.svg` or your designated filename) is placed within the `task_management_app/static/img/` directory.

2.  **Virtual Environment Setup:**
    Open a terminal or command prompt and navigate to the root directory of the project (`task_management_app`).

    ```bash
    # Create a virtual environment (e.g., named 'venv')
    python -m venv venv

    # Activate the virtual environment
    # On Windows:
    # .\venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```
    An active virtual environment is typically indicated by a prefix like `(venv)` in your command prompt.

3.  **Dependency Installation:**
    With the virtual environment activated, install the necessary Python packages:

    ```bash
    pip install -r requirements.txt
    ```
    This command installs all packages listed in the `requirements.txt` file.

4.  **Environment Variable Configuration (Recommended):**
    For enhanced security, particularly for the Flask `SECRET_KEY`, it is advisable to use environment variables.
    * The `python-dotenv` package (included in `requirements.txt`) facilitates this.
    * Create a file named `.env` in the project's root directory (`task_management_app`).
    * Define the `SECRET_KEY` in the `.env` file. Generate a strong, unique key for this purpose.
        ```env
        SECRET_KEY='your_strong_random_secret_key_here'
        # Optionally, define a custom database URI:
        # DATABASE_URL='sqlite:///instance/production_tasks.db'
        ```
    The `app.py` file is configured to utilize these environment variables. If a `.env` file is not present or a variable is not set, fallback default values in `app.py` will be used (the default `SECRET_KEY` is not suitable for production).

5.  **Database Initialization:**
    The application includes a Flask CLI command for database schema creation.
    * **Set the `FLASK_APP` environment variable:** This informs Flask about your application's entry point.
        ```bash
        # On Windows (Command Prompt):
        # set FLASK_APP=app.py
        # On Windows (PowerShell):
        # $env:FLASK_APP="app.py"
        # On macOS/Linux:
        # export FLASK_APP=app.py
        ```
    * **Execute the database initialization command:**
        ```bash
        flask init-db
        ```
        This command creates the `database.db` file (typically within an `instance` folder in the project root) and establishes the required database tables based on the SQLAlchemy models. Note: The `app.py` file also contains logic to call `db.create_all()` when run in debug mode, which can also create the database if it doesn't exist. Using `flask init-db` is the recommended method for explicit schema creation.

6.  **Application Launch:**
    Ensure the virtual environment is active and the `FLASK_APP` environment variable is set.

    ```bash
    python app.py
    ```
    Alternatively, use the Flask CLI:
    ```bash
    flask run
    ```
    The application will typically be accessible at `http://127.0.0.1:5000/`. Open this URL in a web browser.

## Application Usage

1.  Access the application via its URL in a web browser.
2.  Utilize the "**Register**" link in the sidebar to create a new user account.
3.  **Login** using your registered credentials.
4.  Upon successful authentication, you will be directed to the **Dashboard**.
5.  The Dashboard provides the following functionalities:
    * View all personal tasks.
    * Filter tasks by status using the provided dropdown menu.
    * Sort tasks by clicking on the column headers (Title, Due Date, Status).
    * Initiate task creation by clicking the "**Add New Task**" button.
    * Modify or remove existing tasks using the "Edit" (pencil icon) and "Delete" (trash icon) actions available for each task. Deletion operations require user confirmation.
6.  Terminate your session by selecting "**Logout**" from the sidebar.

## Screenshots

Here's a glimpse of TaskManager in action:

**Login Page:**
![Login Page](output%20images/login_page.png)

**Register Page:**
![Register Page](output%20images/register_page.png)

**Dashboard (Empty):**
![Empty Dashboard View](output%20images/DashBoard.png)

**Add/Edit Task Page:**
![Add/Edit Task Page](output%20images/task_adding_edit_page.png)

**Task Added to Dashboard:**
![Dashboard after a task is added](output%20images/task_added.png)

**Task Marked as Completed:**
![Dashboard showing a completed task](output%20images/task_completed.png)

**Logged Out Confirmation:**
![Logged out state / Login page after logout](output%20images/logged_out.png)

## Design Considerations and Future Enhancements

### Design Philosophy:

* **User Interface & Experience:** The primary goal was to create a clean, intuitive, and modern interface. The color scheme, inspired by the [Customer Insights AI](https://www.customerinsights.ai/) logo (`#0064A7` blue and `#F69522` orange/yellow), aims for a professional yet engaging aesthetic. A fixed sidebar ensures persistent navigation, while card-based layouts enhance content organization. User feedback is provided through flash messages.
* **Technology Choices:**
    * **Flask:** Selected for its lightweight nature and suitability for rapid development of small to medium-scale web applications.
    * **SQLAlchemy & SQLite:** Provide a straightforward and efficient solution for data persistence in a local development or small application context.
    * **Jinja2:** Leveraged for dynamic HTML page generation.
    * **Bootstrap 5:** Forms the basis of the responsive grid system and provides foundational component styles, which are then extensively customized via `custom.css`.

### Potential Future Enhancements:

* **Asynchronous Operations (AJAX):** Implement AJAX for task manipulations (create, update, delete, status changes) to provide a more fluid user experience by eliminating full-page reloads.
* **Advanced Search and Filtering:** Introduce keyword-based search functionality for task titles and descriptions, and potentially filtering by date ranges.
* **Responsive Sidebar Optimization:** For improved usability on smaller screens (mobile/tablet), implement a collapsible sidebar menu (e.g., "hamburger" menu).
* **User Profile Management:** Develop a dedicated section for users to manage their profile information, including password changes.
* **Extended Task Functionality:**
    * **Notifications/Reminders:** Integrate mechanisms for task due date reminders (e.g., email or in-app notifications).
    * **Categorization/Tagging:** Allow users to assign categories or tags to tasks for enhanced organization.
    * **Sub-tasks:** Introduce support for hierarchical task structures.
    * **Priority Assignment:** Implement task priority levels (e.g., Low, Medium, High).
* **API Development:** Create a set of RESTful API endpoints for core application functionalities, enabling potential integration with other services or client applications.
* **Automated Testing:** Develop a suite of unit and integration tests to ensure application robustness and maintainability.
* **Production Deployment Strategy:** For production environments, plan for deployment using appropriate WSGI servers (e.g., Gunicorn, uWSGI) and consider migrating to a more scalable database system (e.g., PostgreSQL, MySQL).

---

Thank you for reviewing TaskManager.

Sincerely,

Purnima Darsi
