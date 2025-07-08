from flask import Flask, render_template, jsonify
import json
import os
import random
import configparser
from datetime import datetime

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

class WebTimerConfig:
    def __init__(self):
        self.load_config()
        self.load_health_tips()
    
    def load_config(self):
        """設定をデフォルト値または環境変数から読み込む"""
        # デフォルト設定
        self.timer_minutes = int(os.environ.get('TIMER_MINUTES', '60'))
        self.working_hours_enabled = os.environ.get('WORKING_HOURS_ENABLED', 'true').lower() == 'true'
        self.working_hours_start = os.environ.get('WORKING_HOURS_START', '08:30')
        self.working_hours_end = os.environ.get('WORKING_HOURS_END', '17:00')
        self.reminder_message = os.environ.get('REMINDER_MESSAGE', '座りすぎです！少しストレッチしましょう！')
        self.auto_close_seconds = int(os.environ.get('AUTO_CLOSE_SECONDS', '5'))
        self.app_title = os.environ.get('APP_TITLE', '座りすぎタイマーV2 - Web版')
        
        # ローカル環境では設定ファイルも読み込む
        config_file = "../config.ini"
        if os.path.exists(config_file):
            try:
                config = configparser.ConfigParser()
                config.read(config_file, encoding='utf-8')
                
                if config.has_section('Timer'):
                    self.timer_minutes = config.getint('Timer', 'default_minutes', fallback=self.timer_minutes)
                    self.auto_close_seconds = config.getint('Timer', 'auto_close_seconds', fallback=self.auto_close_seconds)
                
                if config.has_section('WorkingHours'):
                    self.working_hours_enabled = config.getboolean('WorkingHours', 'enabled', fallback=self.working_hours_enabled)
                    self.working_hours_start = config.get('WorkingHours', 'start_time', fallback=self.working_hours_start)
                    self.working_hours_end = config.get('WorkingHours', 'end_time', fallback=self.working_hours_end)
                
                if config.has_section('Messages'):
                    self.reminder_message = config.get('Messages', 'reminder_message', fallback=self.reminder_message)
                    self.app_title = config.get('Messages', 'app_title', fallback=self.app_title)
                    
            except Exception as e:
                print(f"設定ファイルの読み込みエラー: {e}")
    
    def load_health_tips(self):
        """健康ミニ知識をロード"""
        self.health_tips = []
        
        # 環境変数から読み込み（JSON形式）
        tips_env = os.environ.get('HEALTH_TIPS')
        if tips_env:
            try:
                self.health_tips = json.loads(tips_env)
            except json.JSONDecodeError:
                pass
        
        # ローカルファイルから読み込み
        tips_file = "../tips.txt"
        if not self.health_tips and os.path.exists(tips_file):
            try:
                with open(tips_file, 'r', encoding='utf-8') as f:
                    self.health_tips = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print(f"tips.txtの読み込みエラー: {e}")
        
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

# Vercel用のエクスポート
def handler(request):
    return app(request.environ, lambda s, h: None)

if __name__ == '__main__':
    app.run(debug=True)