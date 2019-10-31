import os

from flask import Flask

app = Flask(__name__, static_url_path='/static')
host = os.getenv('HOST', '0.0.0.0')


@app.route('/')
def index():
    # name = request.args.get("name", "World")
    return app.send_static_file('index.html')


# Start the API
if __name__ == "__main__":
    app.run(host=host, debug=True)
