# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Server Management
- `python3 manage.py runserver` - Start the Django development server
- `python3 manage.py shell` - Open Django shell for interactive development
- `python3 manage.py check` - Check for project issues

### Database Operations
- `python3 manage.py migrate` - Apply database migrations
- `python3 manage.py makemigrations` - Create new migrations based on model changes
- `python3 manage.py showmigrations` - Display migration status
- `python3 manage.py flush` - Clear all data from database

### User Management
- `python3 manage.py createsuperuser` - Create Django admin superuser
- `python3 manage.py changepassword <username>` - Change user password

### Portfolio-Specific Commands
- `python3 manage.py setup_initial_data` - Setup initial skill categories and sample data

### Testing
- `python3 manage.py test` - Run Django test suite
- `python3 manage.py test portfolio` - Run tests for portfolio app only

### Static Files
- `python3 manage.py collectstatic` - Collect static files for production

## Architecture Overview

This is a Django portfolio application with the following key components:

### Project Structure
- `portfolio_project/` - Main Django project configuration
- `portfolio/` - Main Django app containing portfolio functionality
- `static/` - Static files (CSS, JavaScript, images)
- `media/` - User-uploaded files (avatars, project images)

### Core Models (portfolio/models.py)
- `Profile` - User profile information with UUID primary key
- `SkillCategory` - Predefined skill categories (frontend, backend, etc.)
- `Skill` - Individual skills with experience years and proficiency levels
- `Experience` - Work experience/project history
- `Project` - Portfolio projects with images and links
- `GitHubProfile` - GitHub integration for fetching user stats

### URL Structure
- `/portfolio/login/` - Authentication
- `/portfolio/dashboard/` - Admin dashboard (requires login)
- `/portfolio/profile/edit/` - Profile editing
- `/portfolio/skills/`, `/portfolio/experiences/`, `/portfolio/projects/`, `/portfolio/github/` - Management interfaces
- `/portfolio/<uuid:profile_id>/` - Public portfolio view

### Key Features
- User authentication with custom login/logout
- Profile management with image uploads
- Skill categorization and proficiency tracking
- Experience/project portfolio display
- GitHub API integration for live stats
- Japanese localization (LANGUAGE_CODE = 'ja')

### Database
- Uses SQLite for development (`db.sqlite3`)
- Models use UUIDs for Profile primary keys
- Configured for Asia/Tokyo timezone

### Dependencies
- Django 4.2+
- Pillow (image processing)
- requests (GitHub API calls)
- python-dotenv (environment variables)

### Authentication Flow
- Custom login form at `/portfolio/login/`
- Redirects to dashboard after login
- Login required for all management views
- Public portfolio accessible without authentication

### GitHub Integration
- Fetches user stats from GitHub API
- Updates repository, follower, and following counts
- Handles API errors gracefully

## File Organization

Templates are in `portfolio/templates/portfolio/` and include:
- `base_admin.html` - Admin interface base template
- `dashboard.html` - Main dashboard
- `detail.html` - Public portfolio view
- Management templates for each data type

The application uses Django's built-in admin interface and custom management views for portfolio content.