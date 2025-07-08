from flask import Flask, render_template, jsonify, request
import json
import os
import configparser
import random
import webbrowser
import threading
import time

app = Flask(__name__)

class WebTimerConfig:
    def __init__(self):
        self.load_config()
        self.load_health_tips()
    
    def load_config(self):
        """設定ファイルを読み込む"""
        config = configparser.ConfigParser()
        config_file = "config.ini"
        
        # デフォルト設定
        self.timer_minutes = 60
        self.working_hours_enabled = True
        self.working_hours_start = "08:30"
        self.working_hours_end = "17:00"
        self.reminder_message = "座りすぎです！少しストレッチしましょう！"
        self.auto_close_seconds = 5
        self.app_title = "座りすぎタイマーV2"
        self.tips_file = "tips.txt"
        
        if os.path.exists(config_file):
            try:
                config.read(config_file, encoding='utf-8')
                
                if config.has_section('Timer'):
                    self.timer_minutes = config.getint('Timer', 'default_minutes', fallback=60)
                    self.auto_close_seconds = config.getint('Timer', 'auto_close_seconds', fallback=5)
                
                if config.has_section('WorkingHours'):
                    self.working_hours_enabled = config.getboolean('WorkingHours', 'enabled', fallback=True)
                    self.working_hours_start = config.get('WorkingHours', 'start_time', fallback="08:30")
                    self.working_hours_end = config.get('WorkingHours', 'end_time', fallback="17:00")
                
                if config.has_section('Messages'):
                    self.reminder_message = config.get('Messages', 'reminder_message', fallback="座りすぎです！少しストレッチしましょう！")
                    self.app_title = config.get('Messages', 'app_title', fallback="座りすぎタイマーV2")
                
                if config.has_section('Files'):
                    self.tips_file = config.get('Files', 'tips_file', fallback="tips.txt")
                    
            except Exception as e:
                print(f"設定ファイルの読み込みエラー: {e}")
    
    def load_health_tips(self):
        """健康ミニ知識を読み込む"""
        self.health_tips = []
        
        if os.path.exists(self.tips_file):
            try:
                with open(self.tips_file, 'r', encoding='utf-8') as f:
                    self.health_tips = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print(f"{self.tips_file}の読み込みエラー: {e}")
        
        # デフォルトの健康ミニ知識
        if not self.health_tips:
            self.health_tips = [
                "30分に1度は立ち上がって歩きましょう",
                "首を左右にゆっくり回してストレッチしましょう",
                "肩甲骨を寄せて胸を開くストレッチをしましょう",
                "目を閉じて30秒間リラックスしましょう",
                "深呼吸を3回して血流を改善しましょう",
                "足首を回してむくみを予防しましょう",
                "腰を左右にひねってストレッチしましょう",
                "水分補給を忘れずに行いましょう"
            ]

# グローバル設定インスタンス
config = WebTimerConfig()

@app.route('/')
def index():
    """メインページ"""
    return render_template('index.html', config=config)

@app.route('/api/config')
def get_config():
    """設定情報をJSON形式で返す"""
    return jsonify({
        'timer_minutes': config.timer_minutes,
        'working_hours_enabled': config.working_hours_enabled,
        'working_hours_start': config.working_hours_start,
        'working_hours_end': config.working_hours_end,
        'reminder_message': config.reminder_message,
        'auto_close_seconds': config.auto_close_seconds,
        'app_title': config.app_title,
        'health_tips': config.health_tips
    })

@app.route('/api/health_tip')
def get_health_tip():
    """ランダムな健康ミニ知識を返す"""
    tip = random.choice(config.health_tips)
    return jsonify({
        'tip': tip,
        'message': config.reminder_message
    })

@app.route('/api/check_working_hours')
def check_working_hours():
    """現在が稼働時間内かを判定"""
    if not config.working_hours_enabled:
        return jsonify({'is_working_hours': True})
    
    from datetime import datetime
    now = datetime.now()
    current_time_minutes = now.hour * 60 + now.minute
    
    try:
        start_hour, start_minute = map(int, config.working_hours_start.split(':'))
        end_hour, end_minute = map(int, config.working_hours_end.split(':'))
        start_time = start_hour * 60 + start_minute
        end_time = end_hour * 60 + end_minute
        
        is_working = start_time <= current_time_minutes <= end_time
    except ValueError:
        is_working = True
    
    return jsonify({
        'is_working_hours': is_working,
        'current_time': now.strftime('%H:%M'),
        'working_hours': f"{config.working_hours_start}-{config.working_hours_end}"
    })

def open_browser():
    """ブラウザを自動で開く"""
    time.sleep(1)  # サーバー起動を待つ
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # ブラウザを自動で開く
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("座りすぎタイマーV2 ブラウザ版を起動中...")
    print("ブラウザが自動で開きます。開かない場合は http://localhost:5000 にアクセスしてください")
    print("終了するには Ctrl+C を押してください")
    
    app.run(debug=False, host='localhost', port=5000)