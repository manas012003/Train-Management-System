# Train-Management-System

Here's a detailed README.md for the Railway Management System project:

Railway Management System
Overview
This project implements a Railway Management System API similar to IRCTC, where users can check train availability between stations, book seats, and retrieve booking details. The system supports role-based access, with specific functionalities for admin users and general users.

Features
User registration and login
Role-based access control (Admin and User)
Admin functionalities:
Add new trains
Update train details
User functionalities:
View train availability between stations
Book seats on trains
Retrieve booking details

Tech Stack
Backend Framework: Flask
Database: PostgreSQL
Authentication: JWT (JSON Web Tokens)
Password Hashing: Bcrypt
Prerequisites
Python 3.6+
PostgreSQL
Virtual environment setup (recommended)

Setup and Installation
1. Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/railway-management-system.git
cd railway-management-system
2. Set Up Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory and add the following variables:

makefile
Copy code
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://yourusername:yourpassword@localhost/railwaydb
JWT_SECRET_KEY=your_jwt_secret_key
ADMIN_API_KEY=your_admin_api_key
5. Set Up the Database
Ensure PostgreSQL is running and execute the following commands:

bash
Copy code
psql
CREATE DATABASE railwaydb;
CREATE USER yourusername WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE railwaydb TO yourusername;
\q
6. Initialize and Migrate Database
bash
Copy code
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
7. Run the Application
bash
Copy code
flask run
The application will be available at http://127.0.0.1:5000.

API Endpoints
Authentication
Register a User

Endpoint: POST /register
Payload:
json
Copy code
{
  "username": "user1",
  "password": "password123"
}
Login User

Endpoint: POST /login
Payload:
json
Copy code
{
  "username": "user1",
  "password": "password123"
}
Response:
json
Copy code
{
  "token": "jwt_token_here"
}
Admin Operations (Protected by Admin API Key)
Add a New Train
Endpoint: POST /add_train
Headers:
json
Copy code
{
  "x-api-key": "your_admin_api_key"
}
Payload:
json
Copy code
{
  "source": "Station A",
  "destination": "Station B",
  "total_seats": 100
}
User Operations (Protected by JWT)
Get Seat Availability

Endpoint: GET /trains
Headers:
json
Copy code
{
  "Authorization": "Bearer jwt_token_here"
}
Query Parameters:
source: The source station
destination: The destination station
Book a Seat

Endpoint: POST /book_seat
Headers:
json
Copy code
{
  "Authorization": "Bearer jwt_token_here"
}
Payload:
json
Copy code
{
  "train_id": 1,
  "seats_requested": 1
}
Get Specific Booking Details

Endpoint: GET /booking_details/<int:booking_id>
Headers:
json
Copy code
{
  "Authorization": "Bearer jwt_token_here"
}
Handling Race Conditions
The seat booking functionality ensures that race conditions are handled by checking seat availability and updating it in a single transaction. This guarantees that only one user can book a seat at a time, even when multiple users attempt to book simultaneously.

Testing
To run the tests, you can use pytest. Ensure you have installed pytest and create test cases in a tests directory.

Contributing
Feel free to submit issues and enhancement requests.

License
