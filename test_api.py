from flask import Flask, request, jsonify
from pymongo import MongoClient
from database_test import Connection
from bson import json_util
import json


app = Flask(__name__)


# Instantiate the Connection class
#db_connection = Connection()
#db_connection.connect("admin", "Stevencantremember", "admin")

@app.route('/save_chat', methods=['POST'])
def save_chat():
    #xdata = request.get_json()
    with app.app_context():
        #data = {"user_inputs":["Hi steven"],"bot_inputs":["Who is steven?"]}
        data = request.get_json()
        user_inputs = data.get('user_inputs', [])
        bot_inputs = data.get('bot_inputs', [])
        if not user_inputs or not bot_inputs:
            return jsonify({'error': 'Missing required parameters'}), 400
        try:
            db_connection = Connection()
            db_connection.connect("admin", "Stevencantremember", "admin")
            #connection = Connection()
            chat_log = ''
            for user_input, bot_input in zip(user_inputs, bot_inputs):
                chat_log += f'User: {user_input}\nBot: {bot_input}\n\n'

            print(chat_log)
            user_id = 1
            response_flag_1 = 0
            response_flag_2 = 0
            response_flag_3 = 0
            save_flag = 1
            db_connection.insert_chat_log(user_id, chat_log, response_flag_1, response_flag_2, response_flag_3, save_flag)
            db_connection.close()
            return jsonify({'message': 'Chat log saved successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    

#will look to see if save chat actually worked
@app.route('/find_chatlog', methods=['GET'])
def find_chatlog():
    with app.app_context():
        db_connection = Connection()
        db_connection.connect("admin", "Stevencantremember", "admin")
        users = db_connection.read("chatbot", "chatlog")
        #returns list [] with results need to jsonify this
        #print(f'api end users: {users}')
        db_connection.close()
        
        if users:
            # below line fixes object_id so it can be processed
            users_json = json_util.dumps(users)
            #loads gets rid of \\ in front of every variable
            parsed_data = json.loads(users_json)
            return jsonify(parsed_data), 200
        return jsonify({'error': 'chatlog not found'}), 404

#response = save_chat()
#print(response)

#check = find_chatlog()
#print(check)


@app.route('/find_users', methods=['GET'])
def find_users():
    with app.app_context():
        db_connection = Connection()
        db_connection.connect("admin", "Stevencantremember", "admin")
        users = db_connection.read("chatbot", "users")
        #returns list [] with results need to jsonify this
        #print(f'api end users: {users}')
        db_connection.close
        if users:
            # below line fixes object_id so it can be processed
            users_json = json_util.dumps(users)
            #loads gets rid of \\ in front of every variable
            parsed_data = json.loads(users_json)
            return jsonify(parsed_data), 200
        return jsonify({'error': 'User not found'}), 404

#JUST FOR TESTING FRONTEND PART
# Call find_users to get the JSON response
#response, status_code = find_users()

# Check if the request was successful (status code 200)
#if status_code == 200:
    # Access the JSON data from the response tuple
    #print(response.data)
#else:
    # Print the error message if the request was not successful
   # print(response.json())


if __name__ == '__main__':
   app.run(debug=True)
"""
##other stuff!
app = Flask(__name__)

# Instantiate the Connection class
db_connection = Connection()
db_connection.connect("admin", "Stevencantremember", "admin")

@app.route('/')
def index():
    return jsonify({'message': 'API is running'})

@app.route('/insert_user', methods=['POST'])
def insert_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    result = db_connection.insert_users(name, email)
    if result == 1:
        return jsonify({'error': 'Duplicate email found'}), 400
    return jsonify({'message': 'User inserted successfully'})

@app.route('/find_users', methods=['GET'])
def find_users():
    users = db_connection.read(test,"chatbot", "users")

    if users:
        return jsonify({'users': users}), 200
    return jsonify({'error': 'User not found'}), 404

# Add more routes for other operations as needed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""


"""
NEED TO INSERT THIS LATER

@app.route('/save_chat', methods=['POST'])
def save_chat():
    with app.app_context():
        #data = {"user_inputs":["Hi steven"],"bot_inputs":["Who is steven?"]}
        data = request.get_json()
        user_inputs = data.get('user_inputs', [])
        bot_inputs = data.get('bot_inputs', [])
        if not user_inputs or not bot_inputs:
            return jsonify({'error': 'Missing required parameters'}), 400
        try:
            db_connection = Connection()
            db_connection.connect("admin", "Stevencantremember", "admin")
            chat_log = ''
            for user_input, bot_input in zip(user_inputs, bot_inputs):
                chat_log += f'User: {user_input}\nBot: {bot_input}\n\n'

            user_id = 1
            response_flag_1 = 0
            response_flag_2 = 0
            response_flag_3 = 0
            save_flag = 1
            db_connection.insert_chat_log(user_id, chat_log, response_flag_1, response_flag_2, response_flag_3, save_flag)
            return jsonify({'message': 'Chat log saved successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return jsonify({'message': 'API is running'})


@app.route('/chat', methods=['POST'])
def chat():
    try:
        logging.info("Received request at /chat endpoint")

        data = request.get_json()
        user_input = data.get('user_input')
        if not user_input:
            logging.warning("User input is missing")
            return jsonify({'error': 'No user_input provided'}), 400

        # Use the HSU class for response generation
        output = HSU.rag(user_input)
        test = output.get('answer')
        logging.info(f"Generated response: {test}")
        return jsonify({'reply': test})

    except Exception as e:
        logging.exception(f"An error occurred during chat processing: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


            
"""