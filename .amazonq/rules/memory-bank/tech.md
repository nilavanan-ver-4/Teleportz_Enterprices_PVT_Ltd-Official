# Teleportz Enterprises - Technology Stack

## Programming Languages and Versions

### Backend
- **Python**: Primary backend language
- **Flask 3.0.0**: Modern web framework with latest features
- **Jinja2**: Template engine (included with Flask)

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Styling and responsive design
- **JavaScript**: Client-side interactivity and dynamic behavior

### Database
- **SQLite**: Lightweight relational database
- **SQLAlchemy**: Python SQL toolkit and ORM

## Core Dependencies

### Flask Ecosystem
```
Flask==3.0.0                    # Core web framework
Flask-SQLAlchemy==3.1.1         # Database ORM integration
Flask-Login==0.6.3              # User session management
Werkzeug==3.0.1                 # WSGI utilities and security
```

### Additional Libraries
```
email_validator==2.1.0          # Email validation for forms
```

## Build System and Development

### Project Structure
- **Blueprint-based Architecture**: Modular Flask application design
- **Application Factory Pattern**: Configurable app creation
- **Dual Module System**: Separate admin and official applications

### Development Commands

#### Environment Setup
```bash
# Install dependencies for admin module
cd admin
pip install -r requirements.txt

# Install dependencies for official module  
cd official
pip install -r requirements.txt
```

#### Database Management
```bash
# Create admin user
python create_admin.py <username> <password>

# Database initialization handled automatically by application factory
```

#### Development Servers
```bash
# Run official website (development)
cd official
python run.py

# Run admin interface (development)
cd admin
python app.py
```

#### Production Deployment
```bash
# WSGI deployment files available:
# admin/passenger_wsgi.py
# official/passenger_wsgi.py
```

## Configuration Management

### Environment Variables
- `SECRET_KEY`: Application security key
- `DATABASE_URL`: Database connection string (optional)

### Default Configuration
- **Database**: SQLite in `instance/site.db`
- **Logging**: Rotating file handler in `logs/app.log`
- **Static Files**: Module-specific static directories

## Development Tools and Features

### Logging System
- **Rotating File Handler**: Prevents log file overflow
- **Configurable Levels**: INFO level by default
- **Module-Specific Logs**: Separate logs for admin and official

### Security Features
- **Password Hashing**: Werkzeug security implementation
- **Session Management**: Flask-Login integration
- **CSRF Protection**: Built into Flask forms

### Database Features
- **ORM Models**: SQLAlchemy model definitions
- **Automatic Table Creation**: Database initialization on first run
- **Migration Support**: Ready for Flask-Migrate integration

## Deployment Architecture

### WSGI Compatibility
- **Production Ready**: WSGI configuration files included
- **Separate Deployments**: Admin and official can be deployed independently
- **Shared Database**: Common data models across deployments

### Static Asset Handling
- **Module Separation**: Each blueprint manages its own assets
- **Image Upload Support**: Product image management system
- **CSS/JS Organization**: Structured asset directories