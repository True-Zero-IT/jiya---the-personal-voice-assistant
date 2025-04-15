import tkinter as tk
from tkinter import Button, ttk
from tkVideoPlayer import TkinterVideo
import subprocess
import jiya_duplicate
import add_history  # Assuming this module contains fetch_conversations() function
import mysql.connector
from mysql.connector import Error
import jokes
import tasks

def show(username,uid):

    # GUI code
    # Create the main application window
    root = tk.Tk()
    root.title("J.I.Y.A - The Personal Voice Assistant")
    root.geometry("600x400")  # Set the window size

    # Create a frame for the top label with a background color
    top_frame = tk.Frame(root)
    top_frame.pack(pady=10)  # Add some vertical padding

    # Display Username on the Right Side
    username_label = tk.Label(root, text=f"Logged in as: {username}", font=("Helvetica", 12), bg="white", fg="black")
    username_label.pack(padx=10, pady=10)  # Position on right side

    # Create and pack the top label
    top_label = tk.Label(top_frame, text="J.I.Y.A - The Personal Voice Assistance", font=("Helvetica", 16), bg="lightgray")
    top_label.pack()

    # Create a frame for the sidebar
    sidebar_frame = tk.Frame(root, width=200, bg="lightgray")
    sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

     # Create a content frame in the middle area
    content_frame = tk.Frame(root)
    content_frame.pack(expand=True, fill=tk.BOTH)

    # Define the function to run the second script
    def run_second_script():
        
        # Create a label in the content frame to display "Listening....."
        listening_label = tk.Label(content_frame, text="", font=("Helvetica", 14), bg="lightgray")
        listening_label.pack(pady=10)
        
        # Display the "Listening....." message on the label when the button is clicked
        listening_label.config(text="Listening.....")
        
        # Run the jiya_duplicate script
        num = jiya_duplicate.run(uid)
        
        if num == 2:
            listening_label.config(text="Execution Complete | Conversation saved successfully...")

    # Function to fetch conversation history from the database using add_history.fetch_conversations()
    def display_conversations():
        conversations = add_history.fetch_conversations(uid)  # Get conversations from the database
        
        # Create a new window to display conversation history
        history_window = tk.Toplevel(root)
        history_window.title("Conversation History")
        history_window.geometry("800x400")

        # Create a Treeview widget with 4 columns: ID, User Input, Assistant Response, Timestamp
        tree = ttk.Treeview(history_window, columns=("ID", "User Input", "Assistant Response", "Timestamp"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("User Input", text="User Input")
        tree.heading("Assistant Response", text="Assistant Response")
        tree.heading("Timestamp", text="Timestamp")

        # Insert conversation records into the Treeview
        for conversation in conversations:
            tree.insert("", tk.END, values=conversation)

        # Add a vertical scrollbar to the Treeview widget
        scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the Treeview widget
        tree.pack(expand=True, fill=tk.BOTH)

     # Function to show the tasks management interface
    def show_tasks_buttons():
        for widget in content_frame.winfo_children():
            widget.destroy()

        add_button = tk.Button(content_frame, text="Add", command=show_add_task_form)
        update_button = tk.Button(content_frame, text="Update", command=show_update_task_form)
        delete_button = tk.Button(content_frame, text="Delete", command=show_delete_task_form)
        view_button = tk.Button(content_frame, text="View All", command=show_view_all_tasks)

        add_button.pack(pady=10)
        update_button.pack(pady=10)
        delete_button.pack(pady=10)
        view_button.pack(pady=10)

    # Function to show the add task form
    def show_add_task_form():
        def submit_task():
            date = date_entry.get()
            task = task_entry.get()
            if date and task:
                result = tasks.addtask(date, task)
                result_label.config(text=result)
                date_entry.delete(0, tk.END)
                task_entry.delete(0, tk.END)
            else:
                result_label.config(text="Please fill in both fields.")

        add_task_window = tk.Toplevel(root)
        add_task_window.title("Add New Task")
        add_task_window.geometry("400x300")

        date_label = tk.Label(add_task_window, text="Date (YYYY-MM-DD):")
        date_label.pack(pady=5)
        date_entry = tk.Entry(add_task_window)
        date_entry.pack(pady=5)

        task_label = tk.Label(add_task_window, text="Task Description:")
        task_label.pack(pady=5)
        task_entry = tk.Entry(add_task_window)
        task_entry.pack(pady=5)

        submit_button = tk.Button(add_task_window, text="Add Task", command=submit_task)
        submit_button.pack(pady=10)

        result_label = tk.Label(add_task_window, text="")
        result_label.pack(pady=5)

    # Function to show the update task form
    def show_update_task_form():
        def submit_update():
            task_id = int(task_id_entry.get())
            new_task = new_task_entry.get()
            if task_id and new_task:
                result = tasks.update_task(task_id, new_task)
                result_label.config(text=result)
            else:
                result_label.config(text="Please fill in both fields.")

        update_window = tk.Toplevel(root)
        update_window.title("Update Task")
        update_window.geometry("400x300")

        tasks = tasks.view_all_tasks()
        tasks_list = "\n".join([f"ID: {task[0]}, Task: {task[2]}" for task in tasks])

        tasks_label = tk.Label(update_window, text=f"Available Tasks:\n{tasks_list}")
        tasks_label.pack(pady=10)

        task_id_label = tk.Label(update_window, text="Enter Task ID to update:")
        task_id_label.pack(pady=5)
        task_id_entry = tk.Entry(update_window)
        task_id_entry.pack(pady=5)

        new_task_label = tk.Label(update_window, text="Enter New Task Description:")
        new_task_label.pack(pady=5)
        new_task_entry = tk.Entry(update_window, width=40)
        new_task_entry.pack(pady=5)

        submit_button = tk.Button(update_window, text="Update Task", command=submit_update)
        submit_button.pack(pady=10)

        result_label = tk.Label(update_window, text="")
        result_label.pack(pady=5)

    # Function to show the delete task form
    def show_delete_task_form():
        def submit_delete():
            task_id = int(task_id_entry.get())
            if task_id:
                result = tasks.delete_task(task_id)
                result_label.config(text=result)
            else:
                result_label.config(text="Please provide a valid Task ID.")

        delete_window = tk.Toplevel(root)
        delete_window.title("Delete Task")
        delete_window.geometry("400x250")

        tasks = tasks.view_all_tasks()
        tasks_list = "\n".join([f"ID: {task[0]}, Task: {task[2]}" for task in tasks])

        tasks_label = tk.Label(delete_window, text=f"Available Tasks:\n{tasks_list}")
        tasks_label.pack(pady=10)

        task_id_label = tk.Label(delete_window, text="Enter Task ID to delete:")
        task_id_label.pack(pady=5)
        task_id_entry = tk.Entry(delete_window)
        task_id_entry.pack(pady=5)

        submit_button = tk.Button(delete_window, text="Delete Task", command=submit_delete)
        submit_button.pack(pady=10)

        result_label = tk.Label(delete_window, text="")
        result_label.pack(pady=5)

    # Function to show all tasks
    def show_view_all_tasks():
        tasks_window = tk.Toplevel(root)
        tasks_window.title("All Tasks")
        tasks_window.geometry("400x300")

        tasks = tasks.view_all_tasks()

        tasks_list = "\n".join([f"ID: {task[0]}, Date: {task[1]}, Task: {task[2]}" for task in tasks])

        tasks_label = tk.Label(tasks_window, text=f"All Tasks:\n{tasks_list}")
        tasks_label.pack(pady=10)

    # Function to handle the 'Add Joke' button
    def show_joke_buttons():
        # Clear the content frame before displaying new buttons
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Show the buttons for managing jokes
        add_button = tk.Button(content_frame, text="Add", command=show_add_joke_form)
        update_button = tk.Button(content_frame, text="Update", command=show_update_joke_form)
        delete_button = tk.Button(content_frame, text="Delete", command=show_delete_joke_form)
        view_button = tk.Button(content_frame, text="View All", command=show_view_all_jokes)

        add_button.pack(pady=10)
        update_button.pack(pady=10)
        delete_button.pack(pady=10)
        view_button.pack(pady=10)

    def show_add_joke_form():
        # Add new joke to the database
        def submit_joke():
            joke = joke_entry.get()
            if joke:
                result = jokes.insert_joke(joke)
                result_label.config(text=result)
                joke_entry.delete(0, tk.END)
            else:
                result_label.config(text="Please fill in the joke field.")

        # Create the add joke form
        joke_window = tk.Toplevel(root)
        joke_window.title("Add New Joke")
        joke_window.geometry("400x250")

        joke_label = tk.Label(joke_window, text="Enter Joke:")
        joke_label.pack(pady=10)
        joke_entry = tk.Entry(joke_window, width=40)
        joke_entry.pack(pady=10)

        submit_button = tk.Button(joke_window, text="Add Joke", command=submit_joke)
        submit_button.pack(pady=10)

        result_label = tk.Label(joke_window, text="")
        result_label.pack(pady=5)

    def show_update_joke_form():
        def submit_update():
            joke_id = int(joke_id_entry.get())
            new_joke = new_joke_entry.get()
            if joke_id and new_joke:
                result = jokes.update_joke(joke_id, new_joke)
                result_label.config(text=result)
            else:
                result_label.config(text="Please fill in both fields.")

        # Create the update joke form
        update_window = tk.Toplevel(root)
        update_window.title("Update Joke")
        update_window.geometry("400x300")

        # Fetch all jokes to display with IDs
        all_jokes = jokes.view_all_jokes()
        jokes_list = "\n".join([f"ID: {j[0]}, Joke: {j[1]}" for j in all_jokes])

        jokes_label = tk.Label(update_window, text=f"Available Jokes:\n{jokes_list}")
        jokes_label.pack(pady=10)

        joke_id_label = tk.Label(update_window, text="Enter Joke ID to update:")
        joke_id_label.pack(pady=5)
        joke_id_entry = tk.Entry(update_window)
        joke_id_entry.pack(pady=5)

        new_joke_label = tk.Label(update_window, text="Enter New Joke:")
        new_joke_label.pack(pady=5)
        new_joke_entry = tk.Entry(update_window, width=40)
        new_joke_entry.pack(pady=5)

        submit_button = tk.Button(update_window, text="Update Joke", command=submit_update)
        submit_button.pack(pady=10)

        result_label = tk.Label(update_window, text="")
        result_label.pack(pady=5)

    def show_delete_joke_form():
        def submit_delete():
            joke_id = int(joke_id_entry.get())
            if joke_id:
                result = jokes.delete_joke(joke_id)
                result_label.config(text=result)
            else:
                result_label.config(text="Please provide a valid Joke ID.")

        # Create the delete joke form
        delete_window = tk.Toplevel(root)
        delete_window.title("Delete Joke")
        delete_window.geometry("400x250")

        # Fetch all jokes to display with IDs
        all_jokes = jokes.view_all_jokes()
        jokes_list = "\n".join([f"ID: {j[0]}, Joke: {j[1]}" for j in all_jokes])

        jokes_label = tk.Label(delete_window, text=f"Available Jokes:\n{jokes_list}")
        jokes_label.pack(pady=10)

        joke_id_label = tk.Label(delete_window, text="Enter Joke ID to delete:")
        joke_id_label.pack(pady=5)
        joke_id_entry = tk.Entry(delete_window)
        joke_id_entry.pack(pady=5)

        submit_button = tk.Button(delete_window, text="Delete Joke", command=submit_delete)
        submit_button.pack(pady=10)

        result_label = tk.Label(delete_window, text="")
        result_label.pack(pady=5)

    def show_view_all_jokes():
        # Create a new window to show all jokes
        jokes_window = tk.Toplevel(root)
        jokes_window.title("All Jokes")
        jokes_window.geometry("400x300")

        all_jokes = jokes.view_all_jokes()

        jokes_list = "\n".join([f"ID: {j[0]}, Joke: {j[1]}" for j in all_jokes])

        jokes_label = tk.Label(jokes_window, text=f"All Jokes:\n{jokes_list}")
        jokes_label.pack(pady=10)

    # Function to insert new QA entry into the database
    def insert_qa(question, answer):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="jiya")
            cursor = connection.cursor()
            query = "INSERT INTO qa_data (question, answer) VALUES (%s, %s)"
            cursor.execute(query, (question, answer))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Question-Answer added successfully!")
        except Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to update QA entry in the database
    def update_qa(q_id, column, new_value):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="jiya")
            cursor = connection.cursor()
            query = f"UPDATE qa_data SET {column} = %s WHERE id = %s"
            cursor.execute(query, (new_value, q_id))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", f"Question-Answer with ID {q_id} updated successfully!")
        except Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to delete QA entry from the database
    def delete_qa(q_id):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="jiya")
            cursor = connection.cursor()
            query = "DELETE FROM qa_data WHERE id = %s"
            cursor.execute(query, (q_id,))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", f"Question-Answer with ID {q_id} deleted successfully!")
        except Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to fetch all QA data
    def fetch_all_qa():
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="jiya")
            cursor = connection.cursor()
            query = "SELECT * FROM qa_data"
            cursor.execute(query)
            all_qa = cursor.fetchall()
            cursor.close()
            connection.close()
            return all_qa
        except Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []

    # UI Elements and Functionality
    def show_train_model_buttons():
        for widget in content_frame.winfo_children():
            widget.destroy()
        add_button = tk.Button(content_frame, text="Add", command=show_add_qa_form)
        update_button = tk.Button(content_frame, text="Update", command=show_update_qa_form)
        delete_button = tk.Button(content_frame, text="Delete", command=show_delete_qa_form)
        view_button = tk.Button(content_frame, text="View All", command=show_view_all_qa)
        add_button.pack(pady=10)
        update_button.pack(pady=10)
        delete_button.pack(pady=10)
        view_button.pack(pady=10)

    # Function to show the add Q&A form
    def show_add_qa_form():
        def submit_qa():
            question = question_entry.get()
            answer = answer_entry.get()
            if question and answer:
                insert_qa(question, answer)
                question_entry.delete(0, tk.END)
                answer_entry.delete(0, tk.END)
                result_label.config(text="Question-Answer added!")
            else:
                result_label.config(text="Please fill in both fields.")
        
        add_qa_window = tk.Toplevel(root)
        add_qa_window.title("Add Question-Answer")
        add_qa_window.geometry("400x300")
        tk.Label(add_qa_window, text="Enter Question:").pack(pady=5)
        question_entry = tk.Entry(add_qa_window, width=40)
        question_entry.pack(pady=5)
        tk.Label(add_qa_window, text="Enter Answer:").pack(pady=5)
        answer_entry = tk.Entry(add_qa_window, width=40)
        answer_entry.pack(pady=5)
        tk.Button(add_qa_window, text="Add Q&A", command=submit_qa).pack(pady=10)
        result_label = tk.Label(add_qa_window, text="")
        result_label.pack(pady=5)

    # Function to show the update Q&A form
    def show_update_qa_form():
        def submit_update():
            q_id = int(q_id_entry.get())
            column = column_entry.get()
            new_value = new_value_entry.get()
            if q_id and column and new_value:
                update_qa(q_id, column, new_value)
                q_id_entry.delete(0, tk.END)
                column_entry.delete(0, tk.END)
                new_value_entry.delete(0, tk.END)
            else:
                result_label.config(text="Please fill in all fields.")

        update_qa_window = tk.Toplevel(root)
        update_qa_window.title("Update Question-Answer")
        update_qa_window.geometry("400x300")
        tk.Label(update_qa_window, text="Enter ID to update:").pack(pady=5)
        q_id_entry = tk.Entry(update_qa_window)
        q_id_entry.pack(pady=5)
        tk.Label(update_qa_window, text="Column to update (question/answer):").pack(pady=5)
        column_entry = tk.Entry(update_qa_window)
        column_entry.pack(pady=5)
        tk.Label(update_qa_window, text="Enter new value:").pack(pady=5)
        new_value_entry = tk.Entry(update_qa_window)
        new_value_entry.pack(pady=5)
        tk.Button(update_qa_window, text="Update Q&A", command=submit_update).pack(pady=10)
        result_label = tk.Label(update_qa_window, text="")
        result_label.pack(pady=5)

    # Function to show the delete Q&A form
    def show_delete_qa_form():
        def submit_delete():
            q_id = int(q_id_entry.get())
            if q_id:
                delete_qa(q_id)
                q_id_entry.delete(0, tk.END)
            else:
                result_label.config(text="Please enter a valid ID.")
        
        delete_qa_window = tk.Toplevel(root)
        delete_qa_window.title("Delete Question-Answer")
        delete_qa_window.geometry("400x250")
        tk.Label(delete_qa_window, text="Enter ID to delete:").pack(pady=5)
        q_id_entry = tk.Entry(delete_qa_window)
        q_id_entry.pack(pady=5)
        tk.Button(delete_qa_window, text="Delete Q&A", command=submit_delete).pack(pady=10)
        result_label = tk.Label(delete_qa_window, text="")
        result_label.pack(pady=5)

    # Function to show all Q&A entries
    def show_view_all_qa():
        qa_data = fetch_all_qa()
        qa_window = tk.Toplevel(root)
        qa_window.title("All Question-Answers")
        qa_window.geometry("400x300")
        if qa_data:
            for q in qa_data:
                qa_label = tk.Label(qa_window, text=f"ID: {q[0]}, Question: {q[1]}, Answer: {q[2]}")
                qa_label.pack(pady=5)
        else:
            tk.Label(qa_window, text="No data available").pack(pady=10)

    # Create buttons in the sidebar
    button1 = tk.Button(sidebar_frame, text="Execute", command=run_second_script)  # Call the function here
    button1.pack(pady=10)

    # Button 2 to add jokes
    button2 = tk.Button(sidebar_frame, text="Joke", command=show_joke_buttons)
    button2.pack(pady=10)

    # Button to add new task
    button3 = tk.Button(sidebar_frame, text="Tasks",  command=show_tasks_buttons)  # Open add task form
    button3.pack(pady=10)

    # Button to add Q&A
    button4 = tk.Button(sidebar_frame, text="Train Model", command=show_train_model_buttons)  # Open add Q&A form
    button4.pack(pady=10)

    # Button to display history
    button5 = tk.Button(sidebar_frame, text="History", command=display_conversations)  # Open add joke form
    button5.pack(pady=10)

    # Create labels for bottom-left and bottom-right corners
    bottom_left_label = tk.Label(root, text="DM | Enterprise", font=("Helvetica", 10))
    bottom_left_label.pack(side=tk.LEFT, anchor=tk.SW, padx=10, pady=10)  # Bottom-left corner

    bottom_right_label = tk.Label(root, text="TrueZero", font=("Helvetica", 10))
    bottom_right_label.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)  # Bottom-right corner

    # Start the Tkinter event loop
    root.mainloop()

