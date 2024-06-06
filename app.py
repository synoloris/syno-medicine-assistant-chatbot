from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
import uuid
import configparser
from chatbot.chatbot import DoctorChatbot
import openai
import os

# Load configuration from application.properties
config = configparser.ConfigParser()
config.read('application.properties')

app = Flask(__name__)
CORS(app)

print("Starting Flask application...")

# MySQL configurations
app.config['MYSQL_HOST'] = config.get('DEFAULT', 'MYSQL_HOST')
app.config['MYSQL_PORT'] = config.getint('DEFAULT', 'MYSQL_PORT')
app.config['MYSQL_USER'] = config.get('DEFAULT', 'MYSQL_USER')
app.config['MYSQL_PASSWORD'] = config.get('DEFAULT', 'MYSQL_PASSWORD')
app.config['MYSQL_DB'] = config.get('DEFAULT', 'MYSQL_DB')

# Set OpenAI API key
openai.api_key = config.get('DEFAULT', 'OPENAI_API_KEY')

mysql = MySQL(app)
chatbot = DoctorChatbot()

@app.route('/', methods=['GET'])
def index():
    print("Listing users...")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT uuid, name FROM users ORDER BY name ASC")
    users = cursor.fetchall()
    cursor.close()
    
    print("Users listed.")
    return render_template('index.html', users=users)

@app.route('/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        print("Creating user...")
        data = request.json
        user_uuid = str(uuid.uuid4())
        name = data['name']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (uuid, name) VALUES (%s, %s)", (user_uuid, name))
        mysql.connection.commit()
        cursor.close()

        initial_prompt = chatbot.get_initial_prompt(name)

        print("User created!")
        return jsonify({"uuid": user_uuid, "name": name, "initial_prompt": initial_prompt}), 201
    else:
        print("Showing create user form.")
        return render_template('new_user.html')

@app.route('/chat/<string:user_uuid>', methods=['GET'])
def chat(user_uuid):
    print("Checking if user/chat exists...")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM messages WHERE user_uuid = %s", [user_uuid])
    message_count = cursor.fetchone()[0]
    cursor.close()
    
    if message_count == 0:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT name FROM users WHERE uuid = %s", [user_uuid])
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            name = user[0]
            initial_prompt = chatbot.get_initial_prompt(name)
            chatbot.reset()  # Reset the chatbot history
            print("User found, no messages yet!")
            return render_template('chat.html', initial_prompt=initial_prompt)
        else:
            print("User not found.")
            return "User not found", 404
    else:
        print("User found, loading chat history...")
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT sender, message FROM messages WHERE user_uuid = %s ORDER BY created_at", [user_uuid])
        messages = cursor.fetchall()
        cursor.close()

        chat_history = []
        for message in messages:
            role = 'assistant' if message[0] == 'bot' else 'user'
            chat_history.append({"role": role, "content": message[1]})

        chatbot.load_chat_history(chat_history)
        return render_template('chat.html', initial_prompt=None)
    
@app.route('/message', methods=['POST'])
def save_message():
    print("Saving message...")
    data = request.json
    user_uuid = data['chat_id']
    sender = data['sender']
    message = data['message']

    print(user_uuid, sender, message)
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO messages (user_uuid, sender, message) VALUES (%s, %s, %s)", (user_uuid, sender, message))
    mysql.connection.commit()
    
    response = chatbot.get_response(message)
    
    # Save the doctor's response
    cursor.execute("INSERT INTO messages (user_uuid, sender, message) VALUES (%s, %s, %s)", (user_uuid, 'bot', response))
    mysql.connection.commit()
    cursor.close()
    
    print("Message saved!")
    
    return jsonify({"status": "Message saved", "response": response}), 201

@app.route('/messages/<string:user_uuid>', methods=['GET'])
def get_messages(user_uuid):
    print("Getting Messages from " + user_uuid)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT sender, message, created_at FROM messages WHERE user_uuid = %s", [user_uuid])
    messages = cursor.fetchall()
    cursor.close()
    
    messages = [{"sender": row[0], "message": row[1], "created_at": row[2].strftime('%d.%m.%Y %H:%M:%S')} for row in messages]
    
    print("Messages fetched!")
    return jsonify(messages), 200

@app.route('/messages/<string:user_uuid>', methods=['DELETE'])
def clear_messages(user_uuid):
    print("Clearing chat history for " + user_uuid)
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM messages WHERE user_uuid = %s", [user_uuid])
    mysql.connection.commit()
    cursor.close()
    
    # Fetch user name and reset chatbot history
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name FROM users WHERE uuid = %s", [user_uuid])
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        name = user[0]
        initial_prompt = chatbot.get_initial_prompt(name)
        chatbot.reset()
        chatbot.get_initial_prompt(name)  # Add initial prompt to the chatbot history
        
        # Save initial prompt as the first message after clearing history
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO messages (user_uuid, sender, message) VALUES (%s, %s, %s)", (user_uuid, 'bot', initial_prompt))
        mysql.connection.commit()
        cursor.close()

        print("Chat history cleared!")

        return jsonify({"status": "Chat history cleared", "initial_prompt": initial_prompt}), 200
    else:
        return jsonify({"status": "User not found"}), 404

# Custom error handlers
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error="Resource not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="Internal server error"), 500


if __name__ == '__main__':
    print("Running the app...")
    app.run(port=8080, debug=True)
