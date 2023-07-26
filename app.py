from flask import Flask, render_template,request
import requests
from flask_cors import CORS,cross_origin
from scrapper import scrappe

app = Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def render():
    return render_template("index.html")

@app.route('/scrape',methods=['GET','POST'])
@cross_origin()
def scrape():
    if request.method == 'POST':
        searchQuery = request.form['content']
        video_url = searchQuery
        res = scrappe(video_url)
        print(res)
        return render_template('result.html',videos=res)


if __name__ == '__main__':
    app.run(debug=True)