#coding:utf-8
"""
@file:      ExtendedSearch
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2018/2/11 下午8:42
@description:
            --
"""
import sys
import os
sys.path.append(os.path.join(os.getcwd().split('scholar')[0],'scholar'))

from flask import Flask, jsonify, current_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy, get_debug_queries
from flask import request
import simplejson
from sqlalchemy.sql import ClauseElement

from ScholarApi.model import History

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wyn:weiaizq1314@39.104.50.183:5432/extented_sc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASKY_SLOW_DB_QUERY_TIME'] = 2
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config["FLASKY_SLOW_DB_QUERY_TIME"]:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' %\
                    (query.statement, query.parameters, query.duration,query.context))
    return response

# from sqlalchemy.ext.declarative import DeclarativeMeta
# class AlchemyEncoder(simplejson.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj.__class__, DeclarativeMeta):
#             # an SQLAlchemy class
#             fields = {
#                 "id",
#                 "title",
#                 ""
#             }
#             for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                 data = obj.__getattribute__(field)
#                 try:
#                     simplejson.dumps(data) # this will fail on non-encodable values, like other classes
#                     fields[field] = data
#                 except TypeError:
#                     fields[field] = None
#         # a json-encodable dict
#             return fields
#         return simplejson.JSONEncoder.default(self, obj)

@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q")
    
    user_id = request.args.get("userId")
    
    result = db.engine.execute(\
        "select * from articles where authors ~ '{}'\
              limit 20"\
            .format(q)).fetchall()
    
    res = {}
    res["count"] = len(result)
    res["data"] = []
    
    for i in result:
        db.session.add(
            History(
                user_id = user_id,
                article_id = i.id
            )
        )
        if len(str(i.authors).replace("\u00a0", "").replace("\"\"","").split(",")) < 10:
            res["data"].append(
                {
                "id": i.id,
                "title": i.title,
                "year": i.year,
                "link": i.link,
                "bibtex": i.bibtex,
                "summary": i.summary,
                "google_id": i.google_id,
                "pdf_temp_url": i.pdf_temp_url,
                "keywords": i.keywords,
                "authors": i.authors,
                    }
                )
    
    return jsonify(res)

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, True
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, False

if __name__ == '__main__':
    app.run(debug=True)
    #manager.run()