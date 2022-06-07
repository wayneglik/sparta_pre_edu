from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

# Flask
app = Flask(__name__)
# .env
load_dotenv()
ID = os.environ.get('DB_ID')
PW = os.environ.get('DB_PW')
# DB
client = MongoClient("mongodb+srv://"+ID+":"+PW+"@cluster0.mzxll.mongodb.net/?retryWrites=true&w=majority")
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    # bs4 and requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    description = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'title':title,
        'image':image,
        'description':description,
        'star':star_receive,
        'comment':comment_receive
    }
    db.movies.insert_one(doc)
    return jsonify({'msg':'저장 완료!!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movies = list(db.movies.find({},{'_id':False}))
    return jsonify({'movies':movies})

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)