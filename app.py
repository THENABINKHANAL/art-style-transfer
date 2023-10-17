# Import the flask module and create an app using Flask as shown in the following example
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import getResult

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/upload', methods=['POST', 'OPTIONS'])
def submit_data():
    if request.method == 'OPTIONS':
        return '', 200
    # Get JSON data from the request body
    img_str = request.json.imageData.image.dataSource
    result = getResult(img_str)


    # You can process the data here (e.g., save it to a database or trigger another function)

    # Respond with a confirmation that data was received (or any other logic)
    return jsonify(result)

# Check if the executed script is the "main" application script, then run the app
if __name__ == '__main__':
    # The 'debug=True' option enables debug mode for development-friendly error messages and automatic reloading of server code.
    # 'host' is set to '0.0.0.0' to make the server publicly available; remove or change this as needed for your security considerations.
    app.run(debug=True, host='0.0.0.0', port=8000) 