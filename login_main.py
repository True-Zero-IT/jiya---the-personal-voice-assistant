import tkinter as tk
from tkinter import messagebox
import mysql.connector
import jiya_main

# Function to validate login against MySQL database
def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",     
            user="root",          
            password="",           
            database="jiya"      
        )

        cursor = conn.cursor()
        
        # Query to check if the username and password match
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()  # Fetch the first result

        if user:  # If user exists
            root.destroy()
            messagebox.showinfo("Login Success", "You have successfully logged in!")
            uid=user[0]
            jiya_main.show(username,uid)
        else:  # If no user found
            messagebox.showerror("Login Error", "Invalid username or password.")
        
        # Close the cursor and the connection   
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        # Handle any database errors
        messagebox.showerror("Database Error", f"Error connecting to the database: {err}")

# Function to open the registration popup
def open_registration_popup():
    # Create the registration popup
    reg_popup = tk.Toplevel(root)
    reg_popup.title("Register")
    reg_popup.geometry("300x250")
    reg_popup.config(bg="#2c3e50")

    # Username Label and Entry
    label_reg_username = tk.Label(reg_popup, text="Username", font=("Helvetica", 12), fg="#ecf0f1", bg="#34495e")
    label_reg_username.grid(row=0, column=0, pady=10, sticky="w")
    entry_reg_username = tk.Entry(reg_popup, font=("Helvetica", 12))
    entry_reg_username.grid(row=0, column=1, pady=10)

    # Password Label and Entry
    label_reg_password = tk.Label(reg_popup, text="Password", font=("Helvetica", 12), fg="#ecf0f1", bg="#34495e")
    label_reg_password.grid(row=1, column=0, pady=10, sticky="w")
    entry_reg_password = tk.Entry(reg_popup, font=("Helvetica", 12), show="*")
    entry_reg_password.grid(row=1, column=1, pady=10)

    # Confirm Password Label and Entry
    label_reg_conf_password = tk.Label(reg_popup, text="Confirm Password", font=("Helvetica", 12), fg="#ecf0f1", bg="#34495e")
    label_reg_conf_password.grid(row=2, column=0, pady=10, sticky="w")
    entry_reg_conf_password = tk.Entry(reg_popup, font=("Helvetica", 12), show="*")
    entry_reg_conf_password.grid(row=2, column=1, pady=10)

    # Function to register user in the database
    def register_user():
        username = entry_reg_username.get()
        password = entry_reg_password.get()
        confirm_password = entry_reg_conf_password.get()

        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Password Error", "Passwords do not match!")
            return

        try:
            # Connect to MySQL database
            conn = mysql.connector.connect(
                host="localhost",  # Change to your MySQL host (e.g., localhost, IP)
                user="root",       # MySQL username (default is 'root')
                password="",       # Your MySQL password
                database="jiya"    # Database name
            )

            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                messagebox.showerror("Registration Error", "Username already exists!")
            else:
                # Insert new user into the database
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                conn.commit()

                messagebox.showinfo("Registration Success", "You have successfully registered!")
                reg_popup.destroy()  # Close the registration popup
                conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to the database: {err}")

    # Register Button
    register_button = tk.Button(reg_popup, text="Register", font=("Helvetica", 12, "bold"), fg="white", bg="#27ae60", command=register_user)
    register_button.grid(row=3, column=0, columnspan=2, pady=20)

# Create the main window
root = tk.Tk()
root.title("Login Page")
root.geometry("400x350")
root.config(bg="#2c3e50")

# Add a frame for the content
frame = tk.Frame(root, bg="#34495e", width=300, height=300)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title Label
title_label = tk.Label(frame, text="TrueZero", font=("Helvetica", 20, "bold"), fg="#ecf0f1", bg="#34495e")
title_label.grid(row=0, column=0, pady=20, columnspan=2)

# Username Label and Entry
label_username = tk.Label(frame, text="Username", font=("Helvetica", 12), fg="#ecf0f1", bg="#34495e")
label_username.grid(row=1, column=0, pady=10, sticky="w")
entry_username = tk.Entry(frame, font=("Helvetica", 12))
entry_username.grid(row=1, column=1, pady=10)

# Password Label and Entry
label_password = tk.Label(frame, text="Password", font=("Helvetica", 12), fg="#ecf0f1", bg="#34495e")
label_password.grid(row=2, column=0, pady=10, sticky="w")
entry_password = tk.Entry(frame, font=("Helvetica", 12), show="*")
entry_password.grid(row=2, column=1, pady=10)

# Login Button
login_button = tk.Button(frame, text="Login", font=("Helvetica", 12, "bold"), fg="white", bg="#27ae60", command=validate_login)
login_button.grid(row=3, column=0, columnspan=2, pady=20)

# Register Link (this will open the registration popup)
register_link = tk.Button(frame, text="Don't have an account? Register here", font=("Helvetica", 10), fg="white", bg="#34495e", relief="flat", command=open_registration_popup)
register_link.grid(row=4, column=0, columnspan=2, pady=10)

# Run the main loop
root.mainloop()
