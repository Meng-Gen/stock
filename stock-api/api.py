from flask import Flask
from flask_caching import Cache

from analyzers import DupontAnalyzer


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route("/v1/stock/analysis/<stock>")
@cache.cached(timeout=60)
def analysis(stock):
    return "{stock}".format(stock=stock)


@app.route("/v1/stock/help")
@cache.cached(timeout=1800)
def help():
    return "help"