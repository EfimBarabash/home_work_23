from itertools import islice
import os


from flask import Flask, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def build_query(query, iterable):
    query_list = query.split('|')
    res = iterable
    for q in query_list:
        cmd = q.split(':')
        if cmd[0] == 'map':
            res = map(lambda line: line.split()[int(cmd[1])], res)
        elif cmd[0] == 'filter':
            res = filter(lambda line: cmd[1] in line, res)
        elif cmd[0] == 'sort':
            if cmd[1] == 'desc':
                res = sorted(iterable, reverse=True)
            else:
                res = sorted(iterable)
        elif cmd[0] == 'unique':
            res = set(res)
        elif cmd[0] == 'limit':
            res = islice(res, 0, int(cmd[1]))



@app.route("/perform_query", methods=['GET'])
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    try:
        file_name = request.args['file_name']
        query = request.args['query']
    except KeyError:
        return 'Key error', 400

    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    file = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file):
        return 'File not found', 400

    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    with open(file) as f:
        it = iter(f)
        res = build_query(query, it)
        res = list(res)
    return app.response_class(f'{res}', content_type="text/plain")

if __name__ == '__main__':
    app.run()