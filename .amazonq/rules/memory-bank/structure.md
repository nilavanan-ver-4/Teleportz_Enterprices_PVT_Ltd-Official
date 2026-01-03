 # Teleportz Enterprises - Project Structure

## Directory Organization

### Root Level Structure
```
d:\Teleportz_Enterprices_PVT_Ltd-Official/
├── app.py                 # Main application factory and models
├── create_admin.py        # Admin user creation utility
├── admin/                 # Administrative interface module
├── official/              # Public website module
├── database/              # Database files storage
├── instance/              # Flask instance folder
├── logs/                  # Application logs
└── .amazonq/              # AI assistant rules and memory bank
```

### Core Components and Relationships

#### Application Factory Pattern (`app.py`)
- **Central Configuration**: Manages app settings and database configuration
- **Model Definitions**: User, Product, and Inquiry database models
- **Extension Initialization**: Flask-SQLAlchemy, Flask-Login setup
- **Blueprint Registration**: Connects admin and official modules

#### Administrative Module (`admin/`)
```
admin/
├── app.py                 # Admin-specific Flask app instance
├── routes.py              # Admin route handlers and views
├── passenger_wsgi.py      # WSGI deployment configuration
├── requirements.txt       # Python dependencies
├── static/                # Admin-specific CSS/JS assets
├── templates/admin/       # Admin HTML templates
└── logs/                  # Admin-specific logging
```

#### Official Website Module (`official/`)
```
official/
├── app.py                 # Official site Flask app instance
├── routes.py              # Public website route handlers
├── run.py                 # Development server runner
├── passenger_wsgi.py      # WSGI deployment configuration
├── requirements.txt       # Python dependencies
├── static/                # Public website assets (CSS, JS, images)
├── templates/official/    # Public website HTML templates
└── logs/                  # Official site logging
```

## Architectural Patterns

### Blueprint Architecture
- **Modular Design**: Separate blueprints for admin and official functionality
- **URL Prefixing**: Admin routes prefixed with `/admin`
- **Independent Deployment**: Each module can be deployed separately via WSGI

### Database Architecture
- **SQLite Backend**: Lightweight database for development and small-scale deployment
- **Shared Models**: Common data models accessible across both modules
- **Multiple Database Files**: Separate databases in `database/` and `instance/` folders

### Static Asset Organization
- **Module-Specific Assets**: Each blueprint maintains its own static files
- **Separation of Concerns**: Admin and official assets kept separate
- **Image Management**: Product images stored in appropriate static directories

### Logging Strategy
- **Distributed Logging**: Each module maintains its own log files
- **Rotating File Handler**: Prevents log files from growing too large
- **Centralized Configuration**: Logging setup in main application factory

## Development Patterns

### Configuration Management
- **Environment-Based Config**: Uses environment variables with fallbacks
- **Secret Key Management**: Configurable security keys
- **Database URI Flexibility**: Supports different database configurations

### Security Implementation
- **Password Hashing**: Werkzeug security for user authentication
- **Login Management**: Flask-Login for session handling
- **Protected Routes**: Admin routes require authentication

### Deployment Readiness
- **WSGI Configuration**: Ready for production deployment
- **Requirements Management**: Separate dependency files for each module
- **Instance Folder**: Proper Flask instance configuration