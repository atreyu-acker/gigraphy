import psycopg
import os
import bcrypt
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


def get_user(email):
    conn = psycopg.connect(db_url)
    cur = conn.cursor()

    cur.execute('SELECT * FROM users WHERE email = %s;', (email,))
    result = cur.fetchone() 
    print(result)

    cur.close()
    conn.close()
    return result 


def add_XP(username, amount):
    conn = psycopg.connect(db_url)
    cur = conn.cursor()

    cur.execute('UPDATE users SET XP = XP + %s WHERE username = %s', (amount, username))

    conn.commit()
    cur.close()
    conn.close()


def update_password(password, confirm_password, userID):
    conn = psycopg.connect(db_url)
    cur = conn.cursor()

    if password != confirm_password:
        return False, "password_mismatch"
    
    elif len(password) < 8:
        return False, "password_too_short"
    
    elif not any(char.isdigit() for char in password):
        return False, "password_no_number"
    
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    print(f"Updating password for userID {userID} to {hashed.decode()}")
    cur.execute('UPDATE users SET password = %s WHERE userID = %s', (hashed.decode(), userID))


    conn.commit()
    cur.close()
    conn.close()

    return True, "success"


def get_leaderboard(limit=10):
    conn = psycopg.connect(db_url)
    cur = conn.cursor()

    cur.execute('SELECT username, XP FROM users ORDER BY XP DESC LIMIT %s ', (limit,))
    result = cur.fetchall()

    cur.close()
    conn.close()
    return result


def get_XP(username):
    conn = psycopg.connect(db_url)
    cur = conn.cursor()

    cur.execute('SELECT XP FROM users WHERE username = %s;', (username,))
    new_XP = cur.fetchone()[0] # fetchone returns a tuple, so we take the first element which is the XP value

    cur.close()
    conn.close()

    return new_XP


def create_user(email, password, confirm_password, username, security_question, security_answer):

    security_answer = security_answer.lower().strip()
    if password != confirm_password:
        return False, "password_mismatch"
    
    elif security_answer == "" or security_question == "":
        return False, "security_info_missing"
    
    elif len(password) < 8:
        return False, "password_too_short"
    
    elif not any(char.isdigit() for char in password):
        return False, "password_no_number"
    
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

   

    
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    cur.execute(
        "INSERT INTO users (email, password, username, security_question, security_answer) VALUES (%s, %s, %s,%s,%s);",
        (email, hashed.decode(), username, security_question, security_answer)
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
            password VARCHAR(80),
            username VARCHAR(50) UNIQUE,
            security_question VARCHAR(50),
            security_answer VARCHAR(50),
            XP INTEGER DEFAULT 0            
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
            equationID SERIAL PRIMARY KEY,
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

if __name__ == "__main__":
    check_connection()
    create_every_table()
