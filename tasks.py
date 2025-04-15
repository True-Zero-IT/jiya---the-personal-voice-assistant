import mysql.connector
from mysql.connector import Error
from datetime import datetime
import re

def remember():

    #Find Tasks Into the database
    connection = None
    try:
        connection = mysql.connector.connect(
                                        host="localhost",
                                        user="root",
                                        password="",
                                        database="jiya")
        print("Connection to MySQL DB successful")

        today = datetime.now().date()

        cursor = connection.cursor()
        query = "SELECT * FROM remember"  # Replace with your table name
        try:
            if_no_task="Not defined"
            cursor.execute(query)
            results = cursor.fetchall()  # Fetch all records
            date = [row[1] for row in results]
                
        except Error as e:
            print(f"The error '{e}' occurred")
        
        for d in date:

            if today==d:

               tasks = [row[2] for row in results]
               return tasks
            else:
                return if_no_task
        
    except Error as e:
        print(f"The error '{e}' occurred")

def p_d_tasks(data):

    #Find tasks from database
    connection = None
    try:
        connection = mysql.connector.connect(
                                        host="localhost",
                                        user="root",
                                        password="",
                                        database="jiya")
        print("Connection to MySQL DB successful")

        cursor = connection.cursor()
        query = "SELECT * FROM remember"  # Replace with your table name
        try:
            cursor.execute(query)
            results = cursor.fetchall()  # Fetch all records
            date = [row[1] for row in results]
        
            for d in date:
        
                if data==d:

                   tasks = [row[2] for row in results]
                   return tasks

                else:
                    return "Task Not Found"

        except Error as e:
            print(f"The error '{e}' occurred")
        
    except Error as e:
        print(f"The error '{e}' occurred")


# unction to add tasks to the database
def addtask(date, tasks):
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jiya"
        )
        print("Connection to MySQL DB successful")

        cursor = connection.cursor()
        query = "INSERT INTO remember (date, tasks) VALUES (%s, %s)"
        values = (date, tasks)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

        return "Task added successfully!"

    except Error as e:
        print(f"The error '{e}' occurred")
        return "Error occurred while adding task"

# Function to update tasks in the database
def update_task(task_id, new_task):
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jiya"
        )
        cursor = connection.cursor()
        query = "UPDATE remember SET tasks=%s WHERE id=%s"
        cursor.execute(query, (new_task, task_id))
        connection.commit()
        cursor.close()
        connection.close()

        return "Task updated successfully!"

    except Error as e:
        print(f"The error '{e}' occurred")
        return "Error occurred while updating task"

# Function to delete task from the database
def delete_task(task_id):
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jiya"
        )
        cursor = connection.cursor()
        query = "DELETE FROM remember WHERE id=%s"
        cursor.execute(query, (task_id,))
        connection.commit()
        cursor.close()
        connection.close()

        return "Task deleted successfully!"

    except Error as e:
        print(f"The error '{e}' occurred")
        return "Error occurred while deleting task"

# Function to view all tasks in the database
def view_all_tasks():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jiya"
        )
        cursor = connection.cursor()
        query = "SELECT id, date, tasks FROM remember"
        cursor.execute(query)
        tasks = cursor.fetchall()
        connection.close()

        return tasks

    except Error as e:
        print(f"The error '{e}' occurred")
        return "Error occurred while fetching tasks"


        
