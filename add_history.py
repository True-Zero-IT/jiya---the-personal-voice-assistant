import mysql.connector

def init_db():
    # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",  # Your MySQL host (usually 'localhost')
        user="root",       # Your MySQL username
        password="",  # Your MySQL password
        database="jiya"  # The name of the database you created
    )
    c = conn.cursor()

    # Create the conversations table if it does not exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_input TEXT,
            assistant_response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

def store_conversations_in_db(history,uid):
    init_db()
    conn = mysql.connector.connect(
        host="localhost",
        user="root",      
        password="",
        database="jiya" 
    )
    cursor = conn.cursor()

    for conversation in history:
        user_input = conversation['user_input']
        assistant_response = conversation['assistant_response']
        
        # Insert the conversation into the database
        cursor.execute("INSERT INTO conversations (user_input, assistant_response,user_id) VALUES (%s, %s)", 
                       (user_input, assistant_response,uid))
    
    conn.commit()
    conn.close()

def fetch_conversations(uid):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",      
        password="",
        database="jiya" 
    )
    c = conn.cursor()

    c.execute(f"SELECT * FROM conversations WHERE  user_id={uid} ORDER BY timestamp DESC LIMIT 10")
    conversations = c.fetchall()
    conn.close()
    
    return conversations

