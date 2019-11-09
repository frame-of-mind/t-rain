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
    for log in resultList:
        train = repository.get_train_by_id(log['train_id'])
        if train is not None:
            log['from'] = train['from']
            log['to'] = train['to']
            log['should-have-started'] = log['started'].split()[0] + ' ' + train['start']
            log['should-have-arrived'] = log['arrived'].split()[0] + ' ' + train['arrive']
        else:
            log['from'] = 'Train not found'
            log['to'] = 'Train not found'
            log['should-have-started'] = 'Train not found'
            log['should-have-arrived'] = 'Train not found'
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
    start_datetime = req.get('should-have-started')
    start_time = start_datetime.split()[-1]
    arrive_datetime = req.get('should-have-arrived')
    arrive_time = arrive_datetime.split()[-1]
    train = {
        "from": req.get('from'),
        "to": req.get('to'),
        "start": start_time,
        "arrive": arrive_time,
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
