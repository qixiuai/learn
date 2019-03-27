import flask
import tensorflow as tf

from flask import (
    Flask,
    render_template
)

# Create the application instance
app = Flask(__name__)

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return "hello"

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
