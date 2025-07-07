import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import os
import configparser

class SittingTimer:
    def __init__(self, root):
        self.root = root
        
        # 設定ファイルの読み込み
        self.config = configparser.ConfigParser()
        self.load_config()
        
        # アプリケーションの初期設定
        self.root.title(self.app_title)
        self.root.geometry("400x320")
        self.root.resizable(False, False)
        
        # 実行時設定
        self.is_running = False
        self.timer_thread = None
        self.health_tips = []
        
        # 健康ミニ知識の読み込み
        self.load_health_tips()
        
        # UI作成
        self.create_widgets()
        
        # 稼働時間チェック用タイマー
        if self.working_hours_enabled:
            self.check_working_hours()
        
    def load_config(self):
        """設定ファイルを読み込む"""
        config_file = "config.ini"
        
        # デフォルト設定
        self.timer_minutes = 60
        self.working_hours_enabled = True
        self.working_hours_start = "08:30"
        self.working_hours_end = "17:00"
        self.reminder_message = "座りすぎです！少しストレッチしましょう！"
        self.auto_close_seconds = 5
        self.popup_width = 350
        self.popup_height = 200
        self.app_title = "座りすぎタイマーV2"
        self.tips_file = "tips.txt"
        
        if os.path.exists(config_file):
            try:
                self.config.read(config_file, encoding='utf-8')
                
                # [Timer]セクションの設定
                if self.config.has_section('Timer'):
                    self.timer_minutes = self.config.getint('Timer', 'default_minutes', fallback=60)
                    self.auto_close_seconds = self.config.getint('Timer', 'auto_close_seconds', fallback=5)
                
                # [WorkingHours]セクションの設定
                if self.config.has_section('WorkingHours'):
                    self.working_hours_enabled = self.config.getboolean('WorkingHours', 'enabled', fallback=True)
                    self.working_hours_start = self.config.get('WorkingHours', 'start_time', fallback="08:30")
                    self.working_hours_end = self.config.get('WorkingHours', 'end_time', fallback="17:00")
                
                # [Messages]セクションの設定
                if self.config.has_section('Messages'):
                    self.reminder_message = self.config.get('Messages', 'reminder_message', fallback="座りすぎです！少しストレッチしましょう！")
                    self.app_title = self.config.get('Messages', 'app_title', fallback="座りすぎタイマーV2")
                
                # [Display]セクションの設定
                if self.config.has_section('Display'):
                    self.popup_width = self.config.getint('Display', 'popup_width', fallback=350)
                    self.popup_height = self.config.getint('Display', 'popup_height', fallback=200)
                
                # [Files]セクションの設定
                if self.config.has_section('Files'):
                    self.tips_file = self.config.get('Files', 'tips_file', fallback="tips.txt")
                    
            except Exception as e:
                print(f"設定ファイルの読み込みエラー: {e}")
                messagebox.showwarning("設定ファイルエラー", 
                                     f"設定ファイルの読み込みに失敗しました。\nデフォルト設定を使用します。\n\nエラー: {e}")
    
    def load_health_tips(self):
        """健康ミニ知識を読み込む"""
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
    
    def create_widgets(self):
        """UI要素を作成"""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # タイトル
        title_label = ttk.Label(main_frame, text=self.app_title, 
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
        if self.working_hours_enabled:
            working_hours_text = f"稼働時間: {self.working_hours_start}-{self.working_hours_end}"
        else:
            working_hours_text = "稼働時間制限: 無効"
        
        self.working_hours_label = ttk.Label(main_frame, 
                                           text=working_hours_text,
                                           font=("Arial", 9), 
                                           foreground="gray")
        self.working_hours_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        # 設定ファイル情報
        config_info = ttk.Label(main_frame, 
                               text="設定変更: config.ini を編集してください",
                               font=("Arial", 8), 
                               foreground="blue")
        config_info.grid(row=7, column=0, columnspan=2, pady=(5, 0))
    
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
        if self.working_hours_enabled and not self.is_working_hours():
            messagebox.showwarning("稼働時間外", 
                                 f"現在は稼働時間外です（{self.working_hours_start}-{self.working_hours_end}）")
            return
        
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
            # 稼働時間チェック
            if self.working_hours_enabled and not self.is_working_hours():
                self.root.after(0, self.stop_timer)
                self.root.after(0, lambda: messagebox.showinfo("稼働時間終了", 
                                                              "稼働時間が終了しました"))
                break
            
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
        message = f"{self.reminder_message}\n\n💡 {tip}"
        
        # ポップアップウィンドウを作成
        popup = tk.Toplevel(self.root)
        popup.title("リマインダー")
        popup.geometry(f"{self.popup_width}x{self.popup_height}")
        popup.resizable(False, False)
        
        # 画面右上に配置
        popup.geometry(f"+{self.root.winfo_screenwidth() - self.popup_width - 20}+50")
        
        # 常に最前面に表示
        popup.attributes('-topmost', True)
        
        # メッセージ表示
        message_label = ttk.Label(popup, text=message, wraplength=300, 
                                justify=tk.CENTER, font=("Arial", 11))
        message_label.pack(pady=20)
        
        # OKボタン
        ok_button = ttk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)
        
        # 設定された秒数後に自動で閉じる
        popup.after(self.auto_close_seconds * 1000, popup.destroy)
    
    def is_working_hours(self):
        """稼働時間内かどうかを判定"""
        if not self.working_hours_enabled:
            return True
        
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min
        
        # 開始時間と終了時間をパース
        try:
            start_hour, start_minute = map(int, self.working_hours_start.split(':'))
            end_hour, end_minute = map(int, self.working_hours_end.split(':'))
        except ValueError:
            # 設定が不正な場合はデフォルト値を使用
            start_hour, start_minute = 8, 30
            end_hour, end_minute = 17, 0
        
        # 分単位に変換
        start_time = start_hour * 60 + start_minute
        end_time = end_hour * 60 + end_minute
        current_time_minutes = current_hour * 60 + current_minute
        
        return start_time <= current_time_minutes <= end_time
    
    def check_working_hours(self):
        """稼働時間チェック（定期実行）"""
        if self.working_hours_enabled and self.is_running and not self.is_working_hours():
            self.stop_timer()
            messagebox.showinfo("稼働時間終了", "稼働時間が終了しました")
        
        # 1分ごとにチェック
        self.root.after(60000, self.check_working_hours)

def main():
    root = tk.Tk()
    app = SittingTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()