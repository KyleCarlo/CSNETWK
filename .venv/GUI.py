from flask import Flask, render_template
from control.input import Console, Message
from model.client.client import Client

app = Flask(__name__)
app.config['SECRET_KEY'] = '27775abec6ae9ab48a0ec296e09b44bc'
client = Client()
cout = [""]

@app.route('/', methods=['GET', 'POST'])
def home():
    consoleInput = Console()
    messageInput = Message()
    global client
    global cout

    if consoleInput.validate_on_submit():
        if consoleInput.console_input_field.data:
            command = consoleInput.console_input_field.data
            cout.append(client.start_console(command))

    return render_template(
        'index.html',
        console=consoleInput,
        message=messageInput,
        cout=cout
    )

if __name__ == '__main__':
    app.run(debug=True)