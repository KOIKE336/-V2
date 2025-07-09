from flask import Flask, render_template, jsonify
import os
import random

app = Flask(__name__)

# 健康ミニ知識
health_tips = [
    "座りすぎは体に良くありません。定期的に立ち上がりましょう！",
    "1時間に1回は立ち上がって軽いストレッチをしましょう。",
    "深呼吸をして肩の力を抜きましょう。",
    "水分補給を忘れずに！",
    "目を休めるため、20秒間遠くを見つめましょう。"
]

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>座りすぎタイマーV2</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f0f0f0;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
            }
            .timer-display {
                font-size: 48px;
                font-weight: bold;
                color: #333;
                margin: 20px 0;
            }
            .controls {
                margin: 20px 0;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin: 5px;
            }
            .start-btn {
                background-color: #4CAF50;
                color: white;
            }
            .stop-btn {
                background-color: #f44336;
                color: white;
            }
            .reset-btn {
                background-color: #2196F3;
                color: white;
            }
            .health-tip {
                margin-top: 30px;
                padding: 15px;
                background-color: #e8f5e8;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>座りすぎタイマーV2</h1>
            <div class="timer-display" id="timer">60:00</div>
            <div class="controls">
                <button class="start-btn" onclick="startTimer()">スタート</button>
                <button class="stop-btn" onclick="stopTimer()">ストップ</button>
                <button class="reset-btn" onclick="resetTimer()">リセット</button>
            </div>
            <div class="health-tip">
                <h3>💡 健康ミニ知識</h3>
                <p id="health-tip-text">定期的に休憩を取りましょう！</p>
            </div>
        </div>

        <script>
            let timeLeft = 60 * 60; // 60分
            let timerId = null;
            let isRunning = false;

            function updateDisplay() {
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                document.getElementById('timer').textContent = 
                    minutes.toString().padStart(2, '0') + ':' + 
                    seconds.toString().padStart(2, '0');
            }

            function startTimer() {
                if (!isRunning) {
                    isRunning = true;
                    timerId = setInterval(() => {
                        timeLeft--;
                        updateDisplay();
                        
                        if (timeLeft <= 0) {
                            stopTimer();
                            showReminder();
                        }
                    }, 1000);
                }
            }

            function stopTimer() {
                if (isRunning) {
                    isRunning = false;
                    clearInterval(timerId);
                }
            }

            function resetTimer() {
                stopTimer();
                timeLeft = 60 * 60;
                updateDisplay();
                getHealthTip();
            }

            function showReminder() {
                alert('⏰ 座りすぎです！\\n\\n少しストレッチしましょう！');
                getHealthTip();
            }

            function getHealthTip() {
                fetch('/api/health_tip')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('health-tip-text').textContent = data.tip;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }

            // 初期化
            updateDisplay();
            getHealthTip();
        </script>
    </body>
    </html>
    '''

@app.route('/api/health_tip')
def get_health_tip():
    tip = random.choice(health_tips)
    return jsonify({'tip': tip})

@app.route('/api/test')
def test():
    return jsonify({
        'status': 'ok',
        'message': 'Flask app is working!'
    })

if __name__ == '__main__':
    app.run(debug=True)