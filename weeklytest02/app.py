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
    article = db.weekly02.find_one({'idx': int(idx)}, {'_id': False})
    return render_template('detail.html', article=article)


@app.route('/articleList', methods=['GET'])
def get_article_list():
    order = request.args.get('order')
    if order == 'desc':
        article_list = list(db.weekly02.find({}, {'_id': False}).sort('read_count', -1))
    else:
        # article_list = list(db.weekly02.find({}, {'_id': False}).sort('read_count'))
        article_list = list(db.weekly02.find({}, {'_id': False}).sort([("reg_date", -1)]))

    for article in article_list:
        article['reg_date'] = article['reg_date'].strftime('%Y.%m.%d %H:%M:%S')

    return jsonify({"article_list": article_list})


# Create
@app.route('/article', methods=['POST'])
def create_article():
    post_count = db.weekly02.estimated_document_count({})
    if post_count == 0:
        idx = 1
    else:
        idx = (list(db.weekly02.find({}).sort([("idx", -1)])))[0]['idx'] + 1

    title = request.form['title']
    content = request.form['content']
    pw = request.form['pw']
    reg_date = datetime.now()

    doc = {
        'idx': idx,
        'title': title,
        'content': content,
        'pw': pw,
        'read_count': 0,
        'reg_date': reg_date
    }

    db.weekly02.insert_one(doc)

    return {"result": "success"}


# Read
@app.route('/article', methods=['GET'])
def read_article():
    idx = request.args.get('idx')
    read_count = int(db.weekly02.find_one({'idx': int(idx)}, {'_id': False})['read_count']) + 1
    db.weekly02.update_one({'idx': int(idx)}, {'$set': {'read_count': int(read_count)}})
    article = db.weekly02.find_one({'idx': int(idx)}, {'_id': False})
    return jsonify({"article": article})


# Update
@app.route('/article', methods=['PUT'])
def update_article():
    idx = request.args.get('idx')
    title = request.form['title']
    content = request.form['content']
    db.weekly02.update_one({'idx': int(idx)}, {'$set': {'title': title, 'content': content}})
    return {"result": "success"}


# Delete
@app.route('/article', methods=['DELETE'])
def delete_article():
    idx = request.args.get('idx')
    db.weekly02.delete_one({'idx': int(idx)})
    return {"result": "success"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
