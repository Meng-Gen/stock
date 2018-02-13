from flask import Flask
from flask_caching import Cache
from data_fetcher import DataFetcher


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
data_fetcher = DataFetcher()


@app.route("/v1/stock/all/stocks")
@cache.cached(timeout=60)
def get_all_stocks():
	return data_fetcher.get_all_stocks()


@app.route("/v1/stock/analysis/<stock>")
@cache.cached(timeout=60)
def analysis(stock):
    return data_fetcher.analysis(stock)