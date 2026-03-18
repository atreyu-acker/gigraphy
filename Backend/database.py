import psycopg
import os
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv("DATABASE_URL")

def check_connection(): 
    try:
        conn = psycopg.connect(db_url)
        conn.close()  
        print("Connected")
    except Exception as e:
        print(f"Connection failed: {e}")
    

def get_password(email):
    conn = psycopg.connect(db_url)
    cur = conn.cursor()

    cur.execute("SELECT users.password FROM users WHERE email = %s;", (email,))
    password = cur.fetchone()

    cur.close()
    conn.close()

    return password

def create_user(email, password, confirm_password, username):

    if password != confirm_password:
        return False, "password_mismatch"

    conn = psycopg.connect(db_url)
    cur = conn.cursor()


    cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
    if cur.fetchone():
        conn.close()
        return False, "email_exists"


    cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
    if cur.fetchone():
        conn.close()
        return False, "username_exists"


    cur.execute(
        "INSERT INTO users (email, password, username) VALUES (%s, %s, %s);",
        (email, password, username)
    )
    conn.commit()
    cur.close()
    conn.close()
    

    return True, "success"



def create_every_table():
    conn = psycopg.connect(db_url)
    cur = conn.cursor()


    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            userID SERIAL PRIMARY KEY,
            email VARCHAR(50) UNIQUE,
            password VARCHAR(20),
            username VARCHAR(50) UNIQUE            
        );
    """)
    print("Table users now exists!")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS levels (
            levelID SERIAL PRIMARY KEY,
            level_number INTEGER NOT NULL,
            difficulty TEXT NOT NULL,
            max_points INTEGER
            
        );
    """)

    print("Table levels now exists!")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS equations (
            euationID SERIAL PRIMARY KEY,
            levelID INTEGER NOT NULL,
            equation_type TEXT NOT NULL,
            a INTEGER,
            b INTEGER,
            c INTEGER,
            d INTEGER,
            FOREIGN KEY (levelID) REFERENCES levels(levelID)            
        );
    """)
    print("Table equations now exists!")


    cur.execute("""
        CREATE TABLE IF NOT EXISTS attempts (
            attemptID SERIAL PRIMARY KEY,
            userID INTEGER NOT NULL,
            levelID INTEGER NOT NULL,
            score INTEGER,
            time_taken REAL,
            success BOOLEAN,
            attempt_date TIMESTAMP,
            FOREIGN KEY (userID) REFERENCES users(userID),
            FOREIGN KEY (levelID) REFERENCES levels(levelID)
                        
        );
    """)


    conn.commit()
    cur.close()
    conn.close()
    print("Table attempts now exists!")

check_connection()


create_every_table()
