import sqlite3
import hashlib
import streamlit as st

# Create and connect to SQLite database
def create_database():
    conn = sqlite3.connect("calories.db")
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                 )''')

    # Create food log table
    c.execute('''CREATE TABLE IF NOT EXISTS food_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    food_name TEXT,
                    calories INTEGER,
                    protein INTEGER,
                    fats INTEGER,
                    fiber INTEGER,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(username) REFERENCES users(username)
                 )''')
    conn.commit()
    conn.close()

# Function to create user
def create_user(username, password):
    conn = sqlite3.connect("calories.db")
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists, return False
    finally:
        conn.close()


# Function to check user login
def check_login(username, password):
    conn = sqlite3.connect("calories.db")
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pw))
    user = c.fetchone()
    conn.close()

    if st.button("Login"):
        if check_login(username, password):
            st.session_state.username = username
            st.experimental_rerun()  # Reload to show the calorie tracker
        else:
            st.error("Invalid login credentials. Please try again.")
    return user is not None


# Function to log food entry
def log_food(username, food_name, calories, protein, fats, fiber):
    conn = sqlite3.connect("calories.db")
    c = conn.cursor()
    c.execute("INSERT INTO food_log (username, food_name, calories, protein, fats, fiber) VALUES (?, ?, ?, ?, ?, ?)",
              (username, food_name, calories, protein, fats, fiber))
    conn.commit()
    conn.close()

# Function to get user food logs
def get_food_log(username):
    conn = sqlite3.connect("calories.db")
    c = conn.cursor()
    c.execute("SELECT food_name, calories, protein, fats, fiber FROM food_log WHERE username=? ORDER BY date DESC", (username,))
    data = c.fetchall()
    conn.close()
    return data

# Initialize database
create_database()
