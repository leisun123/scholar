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

import time

sys.path.append(os.path.join(os.getcwd().split('scholar')[0],'scholar'))

from flask import Flask, jsonify, current_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy, get_debug_queries
from flask import request
import simplejson
from sqlalchemy.sql import ClauseElement

from ScholarApi.model import History
from jinjasql import JinjaSql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wyn:weiaizq1314@47.254.34.29:5432/extented_sc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASKY_SLOW_DB_QUERY_TIME'] = 2

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

j = JinjaSql()


@app.route("/api/search", methods=["GET"])
def search():
    
        res = {}
        res["state"] = {}
        
        data = request.args.to_dict()
        print(data)
        
        template = """
                  SELECT  id, title, year, link, bibtex, resource_type, resource_link, summary, google_id, pdf_temp_url, site, keywords, authors,
                  {% if author is defined %}
                    similarity(authors, {{ author }} ) AS dist
                  {% elif thesis is defined %}
                    similarity(thesis, {{ thesis }} ) AS dist
                  {% elif keywords is defined %}
                    similarity(keywords, {{ keywords }} ) AS dist
                  {% endif %}
                  
                  FROM articles WHERE
                  LENGTH(authors) < 100
                  
                  AND year BETWEEN
                  
                  {% if year_begin is defined %}
                    {{ year_begin | sqlsafe }}
                  {% else %}
                    1900
                  {% endif %}
                  
                  {% if year_end is defined %}
                  AND {{ year_end | sqlsafe }}
                  {% else %}
                  AND  2020
                  {% endif %}
                  
                  {% if author is defined %}
                  AND authors ~ \'{{ author | sqlsafe }}\'
                  {% endif %}
                  
                  {% if thesis is defined %}
                  AND thesis ~ {{ thesis | sqlsafe}}
                  {% endif %}
                  
                  {% if keywords is defined %}
                  AND keywords ~ {{ keywords | sqlsafe }}
                  {% endif %}
                  
                  ORDER BY dist
                  {% if offset and limit %}
                  DESC OFFSET {{ offset | sqlsafe }} LIMIT {{ limit | sqlsafe }}
                  {% endif %}
                  ;
                   """
        
        
        
        query, bind_params = j.prepare_query(template, data)
        result = db.engine.execute(query, *bind_params).fetchall()

        count = 0
        for index, line in enumerate(result):
            count += 1
            
        return simplejson.dumps(
            {
                "count": count,
                "data": [dict(i) for i in result]
            }
        )
   
        
        

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
    app.run(debug=True, port=2000)
    
