from flask import Flask, render_template, jsonify
import os
import random

app = Flask(__name__)

# 健康ミニ知識
health_tips = [
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
    "ハイカカオチョコを『おやつの定番』にする",
    "食べる順番は「野菜→たんぱく質→主食」",
    "外食は「定食屋」で一汁三菜を意識",
    "空腹で買い物に行かない（余計な買い物防止）",
    "「ゆっくり20回噛む」を最初の３口だけでも実行",
    "皿を小さめに替えて自然に適量化",
    "週１回の『ノンアル日』をつくる",
    "プロテインは１ g/kg 以上足りていない日にだけ使う",
    "毎朝レモン水でビタミンＣをチャージ",
    "冷凍野菜をストックして「忙しい＝野菜ゼロ」を防ぐ",
    "調理油はオリーブオイルか菜種油を基本に",
    "イスに60分座ったら必ず１分立つ",
    "階段は『下り』だけでも歩く",
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
    "軽い運動でも『楽しい音楽』を流すと継続率↑",
    "寝室温度は16〜19 ℃がベスト",
    "就寝１時間前にスマホのブルーライトオフ",
    "眠れない日は呼吸を「４秒吸う-７秒止める-８秒吐く」",
    "ベッドでの動画視聴は禁止して『眠る場所』と覚えさせる",
    "昼食後の15-20分仮眠で集中力を回復",
    "入浴は就寝90分前・40 ℃以下で15分",
    "休日でも起床時刻は±１時間以内",
    "枕元に水を置き夜間の脱水を防ぐ",
    "寝る前の部屋片づけで『視覚ノイズ』を減らす",
    "アルコールは就寝３時間前まで",
    "昼休みに自然光を浴びて体内時計をリセット",
    "眠気覚ましは「窓を開けて深呼吸」から",
    "寝る前の重たい議論・ニュースチェックは避ける",
    "CO₂がこもらないよう就寝前に３分換気",
    "休日の『寝だめ』は２時間以内にとどめる",
    "加湿器で湿度40-60 %をキープ",
    "挨拶はグータッチの方が握手より細菌が少ない",
    "手洗いは「石けん＋20秒」で指先・親指も念入りに",
    "外出後はうがいより『鼻うがい』の方が上気道ケアに◎",
    "デスク周りを１日１回アルコール拭き",
    "歯間ブラシ or フロスを毎晩使用",
    "公共トイレのドアはペーパーを介して開閉",
    "冬場の加湿でインフル感染リスクを下げる",
    "眼精疲労対策に「20分作業→20秒遠くを見る」を徹底",
    "体調メモを付けて『自分の異変』を早期キャッチ"
]

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>座りすぎタイマー</title>
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
            <h1>座りすぎタイマー</h1>
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