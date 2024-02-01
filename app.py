from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
from gpt4all import GPT4All


app = Flask(__name__)
CORS(app)

model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")



@app.route('/')
def index():
    # Render the HTML file from the 'templates' folder
    return render_template('flask_front.html')
    #return render_template('./Hardin-Helper-AI/src/index.html', js_file=url_for('static', filename='Hardin-Helper-AI/src/App.js'))
    #return render_template('./Hardin-Helper-AI/src/App.js')
    #return render_template('./Hardin-Helper-AI/src/index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data['user_input']

    output = model.generate(prompt = user_input, max_tokens=100)

    #bot_response = response['choices'][0]['text']
    bot_response = output

    # Return the bot's response to the front-end
    return jsonify({'bot_response': bot_response})

#u_in = input("Enter something: ")
#chat(u_in)

if __name__ == '__main__':
    app.run(debug=True)


