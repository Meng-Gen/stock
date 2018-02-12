from flask import Flask


app = Flask(__name__)


@app.route("/v1/stock/analyzer/<analyzer>/<date_frame>/<stock>")
def analyzer(analyzer, date_frame, stock):
    return "/{analyzer}/{date_frame}/{stock}" \
        .format(analyzer=analyzer, date_frame=date_frame, stock=stock)


@app.route("/v1/stock/help")
def help():
    return "help"
