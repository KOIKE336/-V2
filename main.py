import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import os

class SittingTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("座りすぎタイマーV2")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # 設定
        self.timer_minutes = 60
        self.is_running = False
        self.timer_thread = None
        self.health_tips = []
        
        # 健康ミニ知識の読み込み
        self.load_health_tips()
        
        # UI作成
        self.create_widgets()
        
        # 稼働時間チェック用タイマー
        self.check_working_hours()
        
    def load_health_tips(self):
        """健康ミニ知識を読み込む"""
        tips_file = "tips.txt"
        if os.path.exists(tips_file):
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
    
    def create_widgets(self):
        """UI要素を作成"""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # タイトル
        title_label = ttk.Label(main_frame, text="座りすぎタイマーV2", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 現在の設定時間表示
        self.current_time_label = ttk.Label(main_frame, 
                                           text=f"現在の設定時間: {self.timer_minutes}分",
                                           font=("Arial", 12))
        self.current_time_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # 時間設定フレーム
        time_frame = ttk.Frame(main_frame)
        time_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Label(time_frame, text="時間設定(分):").grid(row=0, column=0, padx=(0, 5))
        self.time_entry = ttk.Entry(time_frame, width=10)
        self.time_entry.grid(row=0, column=1, padx=(0, 5))
        self.time_entry.insert(0, str(self.timer_minutes))
        
        set_button = ttk.Button(time_frame, text="設定", command=self.set_timer)
        set_button.grid(row=0, column=2)
        
        # 開始/停止ボタン
        self.start_stop_button = ttk.Button(main_frame, text="開始", 
                                          command=self.toggle_timer)
        self.start_stop_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        # ステータス表示
        self.status_label = ttk.Label(main_frame, text="停止中", 
                                    font=("Arial", 10))
        self.status_label.grid(row=4, column=0, columnspan=2, pady=(0, 20))
        
        # 終了ボタン
        exit_button = ttk.Button(main_frame, text="終了", command=self.root.quit)
        exit_button.grid(row=5, column=0, columnspan=2)
        
        # 稼働時間表示
        self.working_hours_label = ttk.Label(main_frame, 
                                           text="稼働時間: 8:30-17:00",
                                           font=("Arial", 9), 
                                           foreground="gray")
        self.working_hours_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
    
    def set_timer(self):
        """タイマー時間を設定"""
        try:
            new_time = int(self.time_entry.get())
            if new_time > 0:
                self.timer_minutes = new_time
                self.current_time_label.config(text=f"現在の設定時間: {self.timer_minutes}分")
                messagebox.showinfo("設定完了", f"タイマーを{self.timer_minutes}分に設定しました")
            else:
                messagebox.showerror("エラー", "1以上の数値を入力してください")
        except ValueError:
            messagebox.showerror("エラー", "正しい数値を入力してください")
    
    def toggle_timer(self):
        """タイマーの開始/停止を切り替え"""
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()
    
    def start_timer(self):
        """タイマーを開始"""
        # テスト用に稼働時間チェックを無効化
        # if not self.is_working_hours():
        #     messagebox.showwarning("稼働時間外", "現在は稼働時間外です（8:30-17:00）")
        #     return
        
        self.is_running = True
        self.start_stop_button.config(text="停止")
        self.status_label.config(text="動作中")
        
        # タイマースレッドを開始
        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()
    
    def stop_timer(self):
        """タイマーを停止"""
        self.is_running = False
        self.start_stop_button.config(text="開始")
        self.status_label.config(text="停止中")
    
    def run_timer(self):
        """タイマーのメインループ"""
        while self.is_running:
            # テスト用に稼働時間チェックを無効化
            # if not self.is_working_hours():
            #     self.root.after(0, self.stop_timer)
            #     self.root.after(0, lambda: messagebox.showinfo("稼働時間終了", 
            #                                                   "稼働時間が終了しました"))
            #     break
            
            # 設定時間待機
            for i in range(self.timer_minutes * 60):
                if not self.is_running:
                    break
                time.sleep(1)
            
            # タイマー終了時の処理
            if self.is_running:
                self.root.after(0, self.show_reminder)
    
    def show_reminder(self):
        """リマインダーを表示"""
        # ランダムに健康ミニ知識を選択
        tip = random.choice(self.health_tips)
        message = f"座りすぎです！少しストレッチしましょう！\n\n💡 {tip}"
        
        # ポップアップウィンドウを作成
        popup = tk.Toplevel(self.root)
        popup.title("リマインダー")
        popup.geometry("350x200")
        popup.resizable(False, False)
        
        # 画面右上に配置
        popup.geometry("+{}+{}".format(self.root.winfo_screenwidth() - 370, 50))
        
        # 常に最前面に表示
        popup.attributes('-topmost', True)
        
        # メッセージ表示
        message_label = ttk.Label(popup, text=message, wraplength=300, 
                                justify=tk.CENTER, font=("Arial", 11))
        message_label.pack(pady=20)
        
        # OKボタン
        ok_button = ttk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)
        
        # 5秒後に自動で閉じる
        popup.after(5000, popup.destroy)
    
    def is_working_hours(self):
        """稼働時間内かどうかを判定"""
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min
        
        # 8:30から17:00の間
        start_time = 8 * 60 + 30  # 8:30を分に変換
        end_time = 17 * 60        # 17:00を分に変換
        current_time_minutes = current_hour * 60 + current_minute
        
        return start_time <= current_time_minutes <= end_time
    
    def check_working_hours(self):
        """稼働時間チェック（定期実行）"""
        # テスト用に稼働時間チェックを無効化
        # if self.is_running and not self.is_working_hours():
        #     self.stop_timer()
        #     messagebox.showinfo("稼働時間終了", "稼働時間が終了しました")
        
        # 1分ごとにチェック
        self.root.after(60000, self.check_working_hours)

def main():
    root = tk.Tk()
    app = SittingTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()