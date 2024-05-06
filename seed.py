from faker import Faker
import random
from connect import create_connection, database

fake = Faker()

def seed_users(conn, num_users):
    """Seed the users table with random data."""
    cursor = conn.cursor()
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.email()
        cursor.execute("INSERT INTO users (fullname, email) VALUES (?, ?)", (fullname, email))
    conn.commit()

def seed_status(conn):
    """Seed the status table with unique values."""
    cursor = conn.cursor()
    statuses = [('new',), ('in progress',), ('completed',)]
    for status in statuses:
        cursor.execute("INSERT OR IGNORE INTO status (name) VALUES (?)", status)
    conn.commit()

def seed_tasks(conn, num_tasks, num_users, num_status):
    """Seed the tasks table with random data."""
    cursor = conn.cursor()
    for _ in range(num_tasks):
        title = fake.sentence()
        description = fake.paragraph()
        status_id = random.randint(1, num_status)
        user_id = random.randint(1, num_users) if num_users > 0 else None
        cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)", (title, description, status_id, user_id))
    conn.commit()

if __name__ == '__main__':
    num_users = 10
    num_tasks = 20
    

    with create_connection(database) as conn:
        if conn is not None:
            seed_users(conn, num_users)
            seed_status(conn)
            seed_tasks(conn, num_tasks, num_users, 3)  # 3 statuses: 'new', 'in progress', 'completed'
        else:
            print("Error! cannot create the database connection.")
