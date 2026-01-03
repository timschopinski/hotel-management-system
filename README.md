
# HOTEL MANAGEMENT SYSTEM

A simple hotel room reservation system focused on frontend functionality.
This project was created as a university application project.

----------------------------------------------------
ABOUT THE PROJECT
----------------------------------------------------

This application implements a calendar-based reservation system for hotel rooms.
The main goal of the project is to focus on frontend architecture, user experience
and reservation flow rather than complex backend business logic.

----------------------------------------------------
TECH STACK
----------------------------------------------------

Backend:
- Python FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (database migrations)

Frontend:
- Vue 3
- TypeScript
- Tailwind CSS
- Pinia

----------------------------------------------------
RUN LOCALLY
----------------------------------------------------

To run the project locally:

1. Make sure Docker and Docker Compose are installed
2. Run:

   docker compose up

3. Open in browser:

   http://localhost:5173/
![App start](docs/images/app-start.png)
----------------------------------------------------
DEMO FEATURES
----------------------------------------------------

1. Hotel owner registration
![App start](docs/images/register.png)
2. User login (JWT authentication)
![App start](docs/images/login.png)
3. Creating hotel rooms
![App start](docs/images/dashboard.png)
4. Viewing reservations
![App start](docs/images/my-reservations.png)
5. Public room listing for customers
![App start](docs/images/rooms.png)
6. Room details page with availability calendar
![App start](docs/images/reservation.png)
