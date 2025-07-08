from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "座りすぎタイマーV2 - 動作確認"

@app.route('/api/test')
def test():
    return jsonify({
        'status': 'ok',
        'message': 'Flask app is working!'
    })

if __name__ == '__main__':
    app.run(debug=True)