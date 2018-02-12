from flask import Flask
from analyzers import DupontAnalyzer


app = Flask(__name__)

@app.route("/v1/stock/analysis/<stock>")
def analysis(stock):
    return "{stock}".format(stock=stock)

@app.route("/v1/stock/help")
def help():
    return "help"
