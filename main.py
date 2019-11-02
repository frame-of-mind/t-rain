import os

from flask import Flask, jsonify, request

import repository

app = Flask(__name__, static_url_path='/static')
host = os.getenv('HOST', '0.0.0.0')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/hour', methods=['POST'])
def hour():
    train = request.form.to_dict(flat=True)
    print(request.form.to_dict(flat=True))
    # save to db
    train_id = repository.insert(train)
    return request.form.to_dict(flat=True), 200


# Start the API
if __name__ == "__main__":
    app.run(host=host, debug=True)
