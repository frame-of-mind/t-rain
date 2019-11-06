from flask import Flask, request

import repository

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/load')
def get_all():
    resultList = repository.get_all()
    data = {"data": resultList}
    return data, 200


@app.route('/hour', methods=['POST'])
def hour():
    train = request.form.to_dict(flat=True)
    print(request.form.to_dict(flat=True))
    # save to db
    train_id = repository.insert(train)
    return request.form.to_dict(flat=True), 200


# Start the API
if __name__ == "__main__":
    app.run(debug=True)
