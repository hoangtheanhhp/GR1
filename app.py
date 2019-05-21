# -*- encoding: utf-8 -*-
import os
import logging
import random

from flask import Flask, jsonify, render_template
import numpy as np
import pymongo
from crawl.crawler import crawler

import settings

client = pymongo.MongoClient(settings.MONGODB_SETTINGS["host"])
db = client[settings.MONGODB_SETTINGS["db"]]
mongo_col = db[settings.MONGODB_SETTINGS["collection"]]
related = db['related']
app = Flask(__name__)

news = crawler()

def categories():
    x = mongo_col.delete_many({})
    mongo_col.insert_many([
        {'category' : u'XÃ HỘI', 'cat' : 'xa-hoi', 'view' : 0},
        {'category' : u'THẾ GIỚI', 'cat' : 'the-gioi', 'view' : 0},
        {'category' : u'VĂN HÓA', 'cat' : 'van-hoa', 'view' : 0},
        {'category' : u'KINH TẾ', 'cat' : 'kinh-te', 'view' : 0},
        {'category' : u'GIÁO DỤC', 'cat' : 'giao-duc', 'view' : 0},
        {'category' : u'THỂ THAO', 'cat' : 'the-thao', 'view' : 0},
        {'category' : u'GIẢI TRÍ', 'cat' : 'giai-tri', 'view' : 0},
        {'category' : u'PHÁP LUẬT', 'cat' : 'phap-luat', 'view' : 0},
        {'category' : u'CÔNG NGHỆ', 'cat' : 'khoa-hoc-cong-nghe', 'view' : 0},
        {'category' : u'KHOA HỌC', 'cat' : 'khoa-hoc', 'view' : 0},
        {'category' : u'ĐỜI SỐNG', 'cat' : 'doi-song', 'view' : 0},
        {'category' : u'XE CỘ', 'cat' : 'xe-co', 'view' : 0},
        {'category' : u'NHÀ ĐẤT', 'cat' : 'nha-dat', 'view' : 0},
    ]);

@app.route('/', methods=["GET"])
def home_page():
    homepage = news.get_homepage()
    urls = news.parser_homepage(homepage)
    cate = mongo_col.find()
    return render_template('index.html', urls=urls, cate=cate)

@app.route('/<cat>', methods=["GET"])
def home(cat):
    homepage = news.get_homepage(cat)
    urls = news.parser_homepage(homepage)
    cate = mongo_col.find()
    return render_template('index.html', urls=urls, cate=cate)

@app.route('/get_related/<related>')
def get_related(related):
    related = news.parser_related(related)
    return render_template('related.html', related=related)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
