2026 Kyle-Atreyu Acker. All rights reserved.

Gigraphy - intro:
Gigraphy is a Python-based game with a graphical interface built using Flet. It includes backend logic for game mechanics and stores user data in a PostgreSQL database hosted on Neon. The project is designed to be modular, making it easy to expand, maintain, and test individual components independently.

System Requirements:
Python 3.9
macOS Catalina (or later)
Flet 0.25.2

Folder Structure:
* Gigraphy/ (root folder)
* frontend/ – GUI code using Flet
    components/ – reusable buttons, dialogs, menus
    pages/ – home screen, game screen, leaderboard
* backend/ – runtime logic and controllers
* database/ – table creation, migrations, initial data
* algorithms/ – game scoring, AI, pathfinding
* assets/ – images, sounds, fonts
* tests/ – unit tests


Setup Instructions if running code independantly:

- set up virtual environment with system requirements

- Install dependencies:
  pip install -r requirements.txt

- Create a .env file in the root folder with your database connection string:
  DATABASE_URL=postgresql://username:password@host/dbname?sslmode=require

- Run the application:
  python main.py