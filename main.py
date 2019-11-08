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


@app.route('/logs')
def get_logs():
    # TODO: implement filters
    # date
    # user
    # stations
    resultList = repository.get_logs()
    data = {"data": resultList}
    return data, 200


@app.route('/train/<id>')
def get_train(id):
    return repository.get_train_by_id(id), 200


@app.route('/trains')
def get_trains():
    # TODO: implement filters
    # from - to
    # starting or arriving
    resultList = repository.get_all()
    data = {"data": resultList}
    return data, 200


@app.route('/log', methods=['POST'])
def add_log():
    req = request.form.to_dict(flat=True)
    # save train {from, to, should-have-started, should-have-arrived, count}
    train = {
        "from": req.get('from'),
        "to": req.get('to'),
        "start": req.get('should-have-started'),
        "arrive": req.get('should-have-arrived'),
    }
    train_res = repository.save_train(train)
    # save log {train_id, started, arrived}
    log = {
        "train_id": train_res['_id'],
        "started": req.get('started'),
        "arrived": req.get('arrived'),
    }
    log_res = repository.save_log(log)
    return request.form.to_dict(flat=True), 200


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
