import json
import celery.states as states
from flask import Flask, Response, request
from flask import url_for, jsonify
from worker import celery

dev_mode = True
app = Flask(__name__)

def task_parser(question_id):
    question_id = int(question_id.split('_')[1])
    question_solve_matching = { 
        6: 'tasks.solve_wsd', 7: 'tasks.solve_wsd',
        8: 'tasks.solve_cc_tselect', 9: 'tasks.cc_uselect',
        10: 'tasks.solve_translate', 11: 'tasks.solve_cc_shortanswer',
        12: 'tasks.solve_analects', 
        13: 'tasks.poem_uselect', 14: 'tasks.poem_uselect',
        15: 'tasks.solve_poem_shortanswer', 16: 'tasks.solve_dictation',
        17: 'tasks.solve_wholebookreading', 23: 'tasks.solve_microwrite'
    }
    return question_solve_matching[question_id]


@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.json
    # data = dict(request.form.lists())
    # for k in data:
    #     if len(data[k]) == 1:
    #         data[k] = data[k][0]
    task_name = task_parser(data['question_id'])
    task = celery.send_task(task_name, args=[data], kwargs={})
    return {
        "question_id": data['question_id'],
        "process_id": task.id,
        "status": "success"
    }

@app.route('/api/check_result', methods=['POST'])
def check_task():
    data = request.json
    question_id = data.get('question_id', '')
    process_id = data.get('process_id', '')
    # question_id = request.args.get('question_id', '')
    # process_id = request.args.get('process_id', None)
    if process_id is None:
        return {
            "question_id": question_id,
            "process_id": '',
            "status": "notexist",
            "answer": "",
            "explain": ""
        }
    else:
        res = celery.AsyncResult(process_id)
        if res.state == states.PENDING:
            return {
                "question_id": question_id,
                "process_id": process_id,
                "status": "processing",
                "answer": "",
                "explain": ""
            }
        else:
            result = {
                "question_id": question_id,
                "process_id": process_id,
                "status": "answered"
            }
            result.update(**res.result)
            return result


@app.route('/health_check')
def health_check() -> Response:
    return jsonify("OK")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
