# Moklet Care (Sarpras)

A production-ready Python Flask application for managing facilities and infrastructure (Sarpras) reports.

## Project Structure

The project uses the Flask Application Factory pattern to stay modular and scalable:

```text
MokletCare/
├── run.py                 # Main entry point for starting the server
├── requirements.txt       # Python dependencies
├── sarpras.db             # SQLite database (auto-generated)
└── app/                   # Core application logic
    ├── __init__.py        # App factory and logging configuration
    ├── config.py          # Environment and application configurations
    ├── db.py              # Database connection and lifecycle management
    ├── static/            # CSS, JavaScript, and images
    ├── templates/         # HTML templates
    └── routes/            # Blueprint routing
        ├── main.py        # Web views/pages
        └── api.py         # REST API endpoints
```

## Setup Instructions

1. **Navigate to the Project Directory**  
   Open your terminal or PowerShell and go to the project root:
   ```powershell
   cd A:\SchoolWork\MokletCare
   ```
   *(Adjust the path if you move the project to a different location)*

2. **Install Dependencies**  
   Install the required Python packages:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the Application**  
   Start the production-ready server:
   ```powershell
   python run.py
   ```
   *The server will start at `http://localhost:5000/`.*

## Features
- **Application Factory Pattern:** Highly modular and scalable folder structure.
- **Production-Ready Server:** Powered by `waitress` WSGI server (ideal for Windows environments).
- **Robust Error Handling & Logging:** Automatically records application logs in the `logs/` directory.
- **RESTful API:** Clean API endpoints built on Flask Blueprints.
