import mysql.connector
from random import choice
from mysql.connector import Error

# Function to create jokes table in the MySQL database if it doesn't exist
def create_jokes_table():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jiya"
        )
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jokes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                joke TEXT NOT NULL
            )
        ''')
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"The error '{e}' occurred")

# Function to add jokes into the database
def insert_joke(joke):
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="jiya")
        cursor = connection.cursor()
        query = "INSERT INTO jokes (joke) VALUES (%s)"  # Ensure consistency with column name
        cursor.execute(query, (joke,))
        connection.commit()
        cursor.close()
        connection.close()
        return "Joke added successfully!"
    except Error as e:
        return f"Error: {e}"

# Function to update a joke in the database
def update_joke(joke_id, new_joke):
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="jiya")
        cursor = connection.cursor()
        query = "UPDATE jokes SET joke=%s WHERE id=%s"  # Ensure consistency with column name
        cursor.execute(query, (new_joke, joke_id))
        connection.commit()
        cursor.close()
        connection.close()
        return "Joke updated successfully!"
    except Error as e:
        return f"Error: {e}"

# Function to delete a joke from the database
def delete_joke(joke_id):
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="jiya")
        cursor = connection.cursor()
        query = "DELETE FROM jokes WHERE id=%s"
        cursor.execute(query, (joke_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return "Joke deleted successfully!"
    except Error as e:
        return f"Error: {e}"

# Function to view all jokes in the database
def view_all_jokes():
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="jiya")
        cursor = connection.cursor()
        query = "SELECT id, joke FROM jokes"  # Ensure consistency with column name
        cursor.execute(query)
        jokes_data = cursor.fetchall()
        connection.close()
        return jokes_data
    except Error as e:
        return f"Error: {e}"

# Function to get a random joke from the database
def get_random_joke():
    try:
        create_jokes_table()
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jiya"
        )
        
        cursor = connection.cursor()
        
        cursor.execute("SELECT joke FROM jokes")  # Ensure consistency with column name
        jokes = cursor.fetchall()  # Fetch all rows from the query
        
        if jokes:
            random_joke = choice(jokes)[0]  # jokes is a list of tuples, so we access the first element [0]
        else:
            random_joke = "No jokes available in the database."
        
        cursor.close()
        connection.close()
        
        return random_joke

    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
        return "Error fetching joke from the database."
