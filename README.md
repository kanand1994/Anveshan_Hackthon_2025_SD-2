# Life-In-Weeks Timeline Application

This application visualizes a user's life in weeks, allowing them to add personal milestones and see them in the context of world events.

## Features

- User authentication (signup/login)
- Visual timeline showing each week of the user's life
- Add, edit, and delete personal events
- Responsive design for all devices
- Secure API with JWT authentication

## Technologies

- **Frontend**: React
- **Backend**: FastAPI (Python)
- **Database**: SQLite

## Setup Instructions

### Backend Setup

1. Create a virtual environment:

python -m venv venv
 
2. Activate the virtual environment:

Windows: venv\Scripts\activate

Mac/Linux: source venv/bin/activate

3. Navigate to the backend directory:
   
   cd backend

4. Install dependencies:

pip install -r requirements.txt

pip install -r requirements.txt --use-deprecated=legacy-resolver

cd ..

5. Run the backend server:

python run.py 

or

uvicorn backend.app:app --reload

###Frontend Setup

1. Navigate to the frontend directory:

cd frontend

2. Install dependencies:

npm install

3. Start the development server:

npm start

###API Endpoints

1. POST /auth/signup - User registration

2. POST /auth/login - User login

3. GET /timeline - Get user timeline

4. POST /events - Create new event

5. PUT /events/{id} - Update event

6. DELETE /events/{id} - Delete event

### Additional Notes

1. **Backend Requirements (backend/requirements.txt):**

fastapi==0.110.0
uvicorn==0.29.0
sqlalchemy==2.0.28
python-dotenv==1.0.1
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0

2. **Database Initialization:**

The SQLite database will be automatically created when you first run the backend server.

3. **CORS Configuration:**

Make sure to enable CORS in the backend to allow requests from the frontend. This is already handled in the `app.py` implementation provided earlier.

4. **Frontend Environment:**

The `.env` file in the frontend directory sets the base API URL that the frontend will use to communicate with the backend.

5. **Security Note:**

For production use, you should:
- Use a more secure secret key
- Implement HTTPS
- Use a production-grade database like PostgreSQL
- Add proper input validation
- Implement rate limiting