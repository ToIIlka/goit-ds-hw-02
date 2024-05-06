import sqlite3

"""Отримати всі завдання певного користувача"""
def get_tasks_by_user(user_id):
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
    tasks = cur.fetchall()
    conn.close()
    return tasks

"""Вибрати завдання за певним статусом"""
def get_tasks_by_status(status):
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = ?)", (status,))
    tasks = cur.fetchall()
    conn.close()
    return tasks

"""Оновити статус конкретного завдання"""
def update_task_status(task_id, new_status):
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = ?) WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()

"""Отримати список користувачів, які не мають жодного завдання"""
def get_users_without_tasks():
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)")
    users = cur.fetchall()
    conn.close()
    return users

"""Додати нове завдання для конкретного користувача"""
def add_task(title, description, status_id, user_id):
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
                (title, description, status_id, user_id))
    conn.commit()
    conn.close()

"""Отримати всі завдання, які ще не завершено"""
def get_incomplete_tasks():
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed')")
    incomplete_tasks = cur.fetchall()
    conn.close()
    return incomplete_tasks

"""Видалити конкретне завдання"""
def delete_task(task_id):
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

"""Знайти користувачів з певною електронною поштою"""
def find_users_by_email(email_domain):
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email LIKE ?", ('%@' + email_domain,))
    users = cur.fetchall()
    conn.close()
    return users

"""Оновити ім'я користувача"""
def update_user_name(user_id, new_name):
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET fullname = ? WHERE id = ?", (new_name, user_id))
    conn.commit()
    conn.close()

"""Отримати кількість завдань для кожного статусу"""
def get_task_count_by_status():
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("SELECT s.name, COUNT(t.id) FROM status s LEFT JOIN tasks t ON s.id = t.status_id GROUP BY s.name")
    task_counts = cur.fetchall()
    conn.close()
    return task_counts

"""Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти"""
def get_tasks_assigned_to_domain(email_domain):
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks t JOIN users u ON t.user_id = u.id WHERE u.email LIKE ?", ('%@' + email_domain,))
    tasks = cur.fetchall()
    conn.close()
    return tasks

"""Отримати список завдань, що не мають опису"""
def get_tasks_without_description():
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE description IS NULL")
    tasks = cur.fetchall()
    conn.close()
    return tasks

"""Вибрати користувачів та їхні завдання, які є у статусі in progress"""
def get_users_and_tasks_in_progress():
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT u.fullname, t.title
        FROM users u
        INNER JOIN tasks t ON u.id = t.user_id
        INNER JOIN status s ON t.status_id = s.id
        WHERE s.name = 'in progress'
    """)
    results = cur.fetchall()
    conn.close()
    return results

"""Отримати користувачів та кількість їхніх завдань"""
def get_users_and_task_counts():
    conn = sqlite3.connect("hw1.dbb")
    cur = conn.cursor()
    cur.execute("SELECT u.fullname, COUNT(t.id) FROM users u LEFT JOIN tasks t ON u.id = t.user_id GROUP BY u.id")
    users_and_task_counts = cur.fetchall()
    conn.close()
    return users_and_task_counts

"""Видалення користувача"""
def delete_user(user_id):
    conn = sqlite3.connect("hw1.db")
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys=ON")
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Приклади використання запитів:
    print("Завдання користувача з ID 5:", get_tasks_by_user(5))
    print("Завдання зі статусом 'in progress':", get_tasks_by_status('in progress'))
    print("Ледарі:", get_users_without_tasks())
    user_id_to_delete = 2
    delete_user(user_id_to_delete)
    print(f"Користувач з ID {user_id_to_delete} успішно видалений.")
    # Інші запити також можна викликати тут
