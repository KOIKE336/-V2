from flask import Flask, render_template, jsonify
import json
import os
import random
from datetime import datetime
import traceback

# Vercel用のパス設定
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# デバッグ情報を出力
print(f"Current working directory: {os.getcwd()}")
print(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")
print(f"Python path: {sys.path}")

app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'),
           static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'))

# デバッグ情報を出力
print(f"Template folder: {app.template_folder}")
print(f"Static folder: {app.static_folder}")
print(f"Template folder exists: {os.path.exists(app.template_folder)}")
print(f"Static folder exists: {os.path.exists(app.static_folder)}")

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
    
    def load_health_tips(self):
        """健康ミニ知識をロード"""
        # デフォルトの健康ミニ知識（tips.txtの内容を直接埋め込み）
        self.health_tips = [
            "お菓子とファストフードは家に「買い置きしない」で断つ",
            "水は１日コップ６〜８杯を小分けに",
            "３色そろった皿（赤＝たんぱく質・緑＝野菜・黄＝主食）を目安に盛る",
            "朝食のパンを「オートミール＋フルーツ」に置き換える",
            "加工肉より「ゆで卵・納豆」を常備",
            "コンビニでは「素焼きナッツ」を最初に手に取る",
            "夜９時以降はカフェインを避ける",
            "甘味飲料は「炭酸入り無糖水」にチェンジ",
            "１週間に１度は「まるごと魚」を食卓へ",
            "調味料はまず塩・胡椒・酢で薄味に慣れる",
            "食物繊維を足すときは「皮つきリンゴ」だけでも OK",
            "１日１回、ヨーグルト100 gで腸活",
            "ラーメンは「スープ半分残し」をデフォルトに",
            "ハイカカオチョコを"おやつの定番"にする",
            "食べる順番は「野菜→たんぱく質→主食」",
            "外食は「定食屋」で一汁三菜を意識",
            "空腹で買い物に行かない（余計な買い物防止）",
            "「ゆっくり20回噛む」を最初の３口だけでも実行",
            "皿を小さめに替えて自然に適量化",
            "週１回の"ノンアル日"をつくる",
            "プロテインは１ g/kg 以上足りていない日にだけ使う",
            "毎朝レモン水でビタミンＣをチャージ",
            "冷凍野菜をストックして「忙しい＝野菜ゼロ」を防ぐ",
            "調理油はオリーブオイルか菜種油を基本に",
            "イスに60分座ったら必ず１分立つ",
            "階段は"下り"だけでも歩く",
            "スマホを持ったらスクワット５回をセット",
            "歩くときは「耳・肩・くるぶしが一直線」を意識",
            "朝の歯みがき中にカーフレイズ20回",
            "テレビを見ながらプランク30秒",
            "湯上がりに肩回し30回で猫背予防",
            "１日合計 8,000 歩を目標に（通勤＋昼休み散歩で到達可）",
            "ペットボトルをダンベルにして肩トレ２分",
            "週２回は３つの大筋群（胸・背中・脚）を動かす",
            "筋トレは「あと２回できる」で止めても十分伸びる",
            "時間がない日は腕立て１セットだけでも◎",
            "ウォームアップ代わりにジャンピングジャック30秒",
            "ランチ前に５分の速歩で血糖コントロール",
            "仕事中はかかと上げ下げで血流アップ",
            "通話は立って行う",
            "買い物袋は左右で持ち替えて左右差を減らす",
            "就寝前ストレッチで深部体温を下げる",
            "休日は「徒歩15分圏」を徒歩で済ませる",
            "軽い運動でも"楽しい音楽"を流すと継続率↑",
            "寝室温度は16〜19 ℃がベスト",
            "就寝１時間前にスマホのブルーライトオフ",
            "眠れない日は呼吸を「４秒吸う-７秒止める-８秒吐く」",
            "ベッドでの動画視聴は禁止して"眠る場所"と覚えさせる",
            "昼食後の15-20分仮眠で集中力を回復",
            "入浴は就寝90分前・40 ℃以下で15分",
            "休日でも起床時刻は±１時間以内",
            "枕元に水を置き夜間の脱水を防ぐ",
            "寝る前の部屋片づけで"視覚ノイズ"を減らす",
            "アルコールは就寝３時間前まで",
            "昼休みに自然光を浴びて体内時計をリセット",
            "眠気覚ましは「窓を開けて深呼吸」から",
            "寝る前の重たい議論・ニュースチェックは避ける",
            "CO₂がこもらないよう就寝前に３分換気",
            "休日の「寝だめ」は２時間以内にとどめる",
            "加湿器で湿度40-60 %をキープ",
            "挨拶はグータッチの方が握手より細菌が少ない",
            "手洗いは「石けん＋20秒」で指先・親指も念入りに",
            "外出後はうがいより"鼻うがい"の方が上気道ケアに◎",
            "デスク周りを１日１回アルコール拭き",
            "歯間ブラシ or フロスを毎晩使用",
            "公共トイレのドアはペーパーを介して開閉",
            "冬場の加湿でインフル感染リスクを下げる",
            "眼精疲労対策に「20分作業→20秒遠くを見る」を徹底",
            "体調メモを付けて"自分の異変"を早期キャッチ"
        ]

# グローバル設定インスタンス - 安全に初期化
try:
    print("Initializing WebTimerConfig...")
    config = WebTimerConfig()
    print("WebTimerConfig initialized successfully")
except Exception as e:
    print(f"Error initializing config: {str(e)}")
    print(f"Traceback: {traceback.format_exc()}")
    # フォールバック設定
    class FallbackConfig:
        def __init__(self):
            self.timer_minutes = 60
            self.working_hours_enabled = True
            self.working_hours_start = '08:30'
            self.working_hours_end = '17:00'
            self.reminder_message = '座りすぎです！少しストレッチしましょう！'
            self.auto_close_seconds = 5
            self.app_title = '座りすぎタイマーV2 - Web版'
            self.health_tips = ['定期的に休憩を取りましょう']
    
    config = FallbackConfig()
    print("Using fallback configuration")

@app.route('/')
def index():
    """メインページ"""
    try:
        print("Accessing index route...")
        print(f"Config object: {config}")
        print(f"Template folder: {app.template_folder}")
        result = render_template('index.html', config=config)
        print("Template rendered successfully")
        return result
    except Exception as e:
        error_msg = f"Error in index route: {str(e)}"
        print(error_msg)
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': error_msg, 'traceback': traceback.format_exc()}), 500

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

@app.route('/api/debug')
def debug():
    """デバッグ情報を返す"""
    return jsonify({
        'status': 'working',
        'cwd': os.getcwd(),
        'template_folder': app.template_folder,
        'static_folder': app.static_folder,
        'template_exists': os.path.exists(app.template_folder),
        'static_exists': os.path.exists(app.static_folder),
        'config_type': type(config).__name__
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

# Vercel用のエクスポート - 正確な関数名を使用
def handler(request):
    return app

# Vercel用のエクスポート
app_handler = app

if __name__ == '__main__':
    app.run(debug=True)