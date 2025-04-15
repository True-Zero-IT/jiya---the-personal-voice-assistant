import os

#add or append into file
def create_file(filename, content=""):
    with open(filename, 'w') as file:
        file.write(content)
    return f"File {filename} has been created"

def append_to_file(filename, content):
    with open(filename, 'a') as file:
        file.write(content)
    return f"Content has been added to {filename}."


#read a file
def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return f"Reading content of {filename}."
        return content
    except FileNotFoundError:
        return f"Sorry, the file {filename} does not exist."


#delete the file
def delete_file(filename):
    try:
        os.remove(filename)
        return f"File {filename} has been deleted."
    except FileNotFoundError:
        return "Sorry, the file {filename} does not exist."

