from datetime import datetime

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.test


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detail/<idx>')
def detail(idx):
    post = db.weekly01.find_one({'idx': int(idx)}, {'_id': False})
    return render_template('detail.html', post=post)


@app.route('/post', methods=['POST'])
def save_post():
    idx = len(list(db.weekly01.find({}, {}))) + 1

    title = request.form['title_give']
    content = request.form['content_give']
    pw = request.form['pw_give']
    reg_date = datetime.now()

    doc = {
        'idx': idx,
        'title': title,
        'content': content,
        'pw': pw,
        'reg_date': reg_date,
    }

    db.weekly01.insert_one(doc)

    return {"result": "success", 'msg': '포스팅 성공!'}


@app.route('/post', methods=['GET'])
def get_post():
    posts = list(db.weekly01.find({}, {'_id': False}).sort('reg_date', -1))

    return jsonify({"posts": posts})


@app.route('/post', methods=['DELETE'])
def delete_post():
    idx = request.args.get('idx')
    db.weekly01.delete_one({'idx': int(idx)})
    return {"result": "success", 'msg': '삭제 성공!'}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
