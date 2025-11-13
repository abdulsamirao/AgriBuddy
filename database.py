import sqlite3
import hashlib

DB_PATH = "agribuddy.db"


def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows column access by name
    return conn


def init_database():
    """Initialize the database and create the users table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username: str, email: str, password: str) -> tuple[bool, str]:
    """
    Create a new user account.
    
    Args:
        username: The username
        email: The email address
        password: The plain text password
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False, "Username already exists"
        
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return False, "Email already registered"
        
        # Hash the password and insert the user
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        
        conn.commit()
        conn.close()
        return True, "Account created successfully"
        
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"
    except Exception as e:
        return False, f"Error creating account: {str(e)}"


def authenticate_user(email: str, password: str) -> tuple[bool, str]:
    """
    Authenticate a user with email and password.
    
    Args:
        email: The email address
        password: The plain text password
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Find user by email
        cursor.execute("SELECT id, username, password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        conn.close()
        
        if not user:
            return False, "Invalid email or password"
        
        # Verify password
        password_hash = hash_password(password)
        if password_hash == user["password_hash"]:
            return True, f"Welcome back, {user['username']}!"
        else:
            return False, "Invalid email or password"
            
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"
    except Exception as e:
        return False, f"Error during authentication: {str(e)}"