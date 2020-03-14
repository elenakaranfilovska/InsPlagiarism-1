from flask import Flask, render_template, send_file

app = Flask(__name__)


@app.route("/heatmap")
def main():
    return send_file('static/img/output.png')


if __name__ == "__main__":
    app.run(port=4999)