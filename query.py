import os
from tkinter import *
from tkinter import messagebox
import sqlite3


desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')



db_path = os.path.join(desktop_path, "users.db")


def create_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fname TEXT NOT NULL,
                        lname TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()


def sign_up():
    fname = entry_fname.get().strip()
    lname = entry_lname.get().strip()
    email = entry_email.get().strip()
    password = entry_password.get().strip()

    if not (fname and lname and email and password):
        messagebox.showwarning("خطا", "همه فیلدها را پر کنید!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (fname, lname, email, password) VALUES (?, ?, ?, ?)", 
                       (fname, lname, email, password))
        conn.commit()
        messagebox.showinfo("موفق", "ثبت‌نام با موفقیت انجام شد!")
    except sqlite3.IntegrityError:
        messagebox.showerror("خطا", "ایمیل قبلاً ثبت شده است!")
    finally:
        conn.close()


def sign_in():
    email = entry_email.get().strip()
    password = entry_password.get().strip()

    if not (email and password):
        messagebox.showwarning("خطا", "ایمیل و رمز عبور را وارد کنید!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("ورود موفق", f"خوش آمدید {user[1]} {user[2]}!")
    else:
        messagebox.showerror("خطا", "ایمیل یا رمز عبور اشتباه است!")


Win = Tk()
Win.title("فرم ورود و ثبت‌نام")
Win.geometry("400x300")

Label(Win, text="Login Form", font=("Arial", 14, "bold")).pack(pady=10)

frame = Frame(Win)
frame.pack(pady=10)

Label(frame, text="Fname:").grid(row=0, column=0, padx=5, pady=5)
entry_fname = Entry(frame)
entry_fname.grid(row=0, column=1, padx=5, pady=5)

Label(frame, text="Lname:").grid(row=1, column=0, padx=5, pady=5)
entry_lname = Entry(frame)
entry_lname.grid(row=1, column=1, padx=5, pady=5)

Label(frame, text="* Email:").grid(row=2, column=0, padx=5, pady=5)
entry_email = Entry(frame)
entry_email.grid(row=2, column=1, padx=5, pady=5)

Label(frame, text="* Password:").grid(row=3, column=0, padx=5, pady=5)
entry_password = Entry(frame, show="*")
entry_password.grid(row=3, column=1, padx=5, pady=5)

btn_frame = Frame(Win)
btn_frame.pack(pady=10)

Button(btn_frame, text="Sign Up", command=sign_up).grid(row=0, column=0, padx=10)
Button(btn_frame, text="Sign In", command=sign_in).grid(row=0, column=1, padx=10)


create_db()

Win.mainloop()