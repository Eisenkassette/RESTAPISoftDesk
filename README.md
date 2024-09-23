# RESTAPISoftDesk

A Django REST API for project management.

## Installation

1. Open your terminal.

2. Create a virtual environment:
   ```
   python -m venv env
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     env\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source env/bin/activate
     ```

4. Clone the repository:
   ```
   git clone https://github.com/Eisenkassette/RESTAPISoftDesk.git
   cd RESTAPISoftDesk
   ```

5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Start the Django development server:
   ```
   python manage.py runserver
   ```

The API should now be running at `http://127.0.0.1:8000/`.

## Superuser Credentials

- Username: admin
- Password: admin

## API Endpoints

- Users: `/api/users/`
- Projects: `/api/projects/`
- Issues: `/api/projects/<project_id>/issues/`
- Comments: `/api/projects/<project_id>/issues/<issue_id>/comments/`

## Technologies Used

- Django
- Django REST Framework
- Simple JWT for authentication
