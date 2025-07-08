// 座りすぎタイマーV2 ブラウザ版 JavaScript

class SittingTimer {
    constructor() {
        this.config = null;
        this.isRunning = false;
        this.isPaused = false;
        this.timerInterval = null;
        this.remainingSeconds = 0;
        this.totalSeconds = 0;
        this.workingHoursInterval = null;
        
        this.init();
    }
    
    async init() {
        await this.loadConfig();
        this.setupEventListeners();
        this.updateDisplay();
        this.checkWorkingHours();
        this.startWorkingHoursCheck();
    }
    
    async loadConfig() {
        try {
            const response = await fetch('/api/config');
            this.config = await response.json();
            this.totalSeconds = this.config.timer_minutes * 60;
            this.remainingSeconds = this.totalSeconds;
        } catch (error) {
            console.error('設定の読み込みエラー:', error);
        }
    }
    
    setupEventListeners() {
        // ボタンイベント
        document.getElementById('set-timer').addEventListener('click', () => this.setTimer());
        document.getElementById('start-stop').addEventListener('click', () => this.toggleTimer());
        document.getElementById('reset').addEventListener('click', () => this.resetTimer());
        
        // モーダル関連
        document.getElementById('close-reminder').addEventListener('click', () => this.closeReminder());
        document.querySelector('.close').addEventListener('click', () => this.closeReminder());
        
        // モーダル外クリックで閉じる
        document.getElementById('reminder-modal').addEventListener('click', (e) => {
            if (e.target.id === 'reminder-modal') {
                this.closeReminder();
            }
        });
        
        // Enterキーでタイマー設定
        document.getElementById('timer-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.setTimer();
            }
        });
        
        // ページ離脱時の確認（タイマー動作中の場合）
        window.addEventListener('beforeunload', (e) => {
            if (this.isRunning) {
                e.preventDefault();
                e.returnValue = 'タイマーが動作中です。ページを離れますか？';
            }
        });
    }
    
    setTimer() {
        const input = document.getElementById('timer-input');
        const minutes = parseInt(input.value);
        
        if (isNaN(minutes) || minutes < 1 || minutes > 999) {
            alert('1から999の数値を入力してください');
            return;
        }
        
        if (this.isRunning) {
            if (!confirm('タイマーが動作中です。設定を変更しますか？')) {
                return;
            }
            this.stopTimer();
        }
        
        this.totalSeconds = minutes * 60;
        this.remainingSeconds = this.totalSeconds;
        this.updateDisplay();
        this.showNotification(`タイマーを${minutes}分に設定しました`);
    }
    
    toggleTimer() {
        if (this.isRunning) {
            this.stopTimer();
        } else {
            this.startTimer();
        }
    }
    
    async startTimer() {
        // 稼働時間チェック
        if (this.config.working_hours_enabled) {
            const workingHoursCheck = await this.checkWorkingHours();
            if (!workingHoursCheck.is_working_hours) {
                alert(`現在は稼働時間外です（${workingHoursCheck.working_hours}）`);
                return;
            }
        }
        
        this.isRunning = true;
        this.isPaused = false;
        
        // UI更新
        document.getElementById('start-stop').textContent = '停止';
        document.getElementById('start-stop').className = 'btn btn-secondary';
        document.getElementById('status').textContent = '動作中';
        document.getElementById('status').className = 'status running';
        
        // タイマー開始
        this.timerInterval = setInterval(() => {
            this.tick();
        }, 1000);
        
        this.updateProgressRing();
    }
    
    stopTimer() {
        this.isRunning = false;
        this.isPaused = false;
        
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
        
        // UI更新
        document.getElementById('start-stop').textContent = '開始';
        document.getElementById('start-stop').className = 'btn btn-primary';
        document.getElementById('status').textContent = '停止中';
        document.getElementById('status').className = 'status stopped';
        
        this.updateProgressRing();
    }
    
    resetTimer() {
        this.stopTimer();
        this.remainingSeconds = this.totalSeconds;
        this.updateDisplay();
        this.updateProgressRing();
    }
    
    tick() {
        this.remainingSeconds--;
        this.updateDisplay();
        this.updateProgressRing();
        
        if (this.remainingSeconds <= 0) {
            this.onTimerComplete();
        }
    }
    
    async onTimerComplete() {
        this.stopTimer();
        this.remainingSeconds = this.totalSeconds; // リセット
        this.updateDisplay();
        
        // リマインダー表示
        await this.showReminder();
        
        // 通知音再生（ブラウザが許可している場合）
        this.playNotificationSound();
    }
    
    async showReminder() {
        try {
            const response = await fetch('/api/health_tip');
            const data = await response.json();
            
            document.getElementById('reminder-message').textContent = data.message;
            document.getElementById('health-tip-text').textContent = data.tip;
            
            const modal = document.getElementById('reminder-modal');
            modal.style.display = 'block';
            
            // 自動閉じカウントダウン
            this.startAutoCloseCountdown();
            
        } catch (error) {
            console.error('リマインダーの表示エラー:', error);
        }
    }
    
    startAutoCloseCountdown() {
        let countdown = this.config.auto_close_seconds;
        const countdownElement = document.getElementById('auto-close-countdown');
        
        const countdownInterval = setInterval(() => {
            countdown--;
            countdownElement.textContent = countdown;
            
            if (countdown <= 0) {
                clearInterval(countdownInterval);
                this.closeReminder();
            }
        }, 1000);
        
        // モーダルが閉じられた時にカウントダウンを停止
        this.autoCloseInterval = countdownInterval;
    }
    
    closeReminder() {
        const modal = document.getElementById('reminder-modal');
        modal.style.display = 'none';
        
        if (this.autoCloseInterval) {
            clearInterval(this.autoCloseInterval);
            this.autoCloseInterval = null;
        }
        
        // カウントダウンをリセット
        document.getElementById('auto-close-countdown').textContent = this.config.auto_close_seconds;
    }
    
    updateDisplay() {
        const minutes = Math.floor(this.remainingSeconds / 60);
        const seconds = this.remainingSeconds % 60;
        
        // タイマー表示更新
        document.getElementById('timer-minutes').textContent = Math.floor(this.totalSeconds / 60);
        
        // カウントダウン表示更新
        document.getElementById('countdown').textContent = 
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    updateProgressRing() {
        const progressRing = document.querySelector('.progress-ring-progress');
        const circumference = 2 * Math.PI * 90; // r = 90
        
        const progress = (this.totalSeconds - this.remainingSeconds) / this.totalSeconds;
        const offset = circumference - (progress * circumference);
        
        progressRing.style.strokeDashoffset = offset;
        
        // 色の変更
        if (this.isRunning) {
            progressRing.style.stroke = '#4CAF50';
        } else {
            progressRing.style.stroke = '#e0e0e0';
        }
    }
    
    async checkWorkingHours() {
        try {
            const response = await fetch('/api/check_working_hours');
            const data = await response.json();
            
            const statusElement = document.getElementById('working-hours-status');
            if (data.is_working_hours) {
                statusElement.textContent = `✅ 稼働時間内（現在時刻: ${data.current_time}）`;
                statusElement.style.color = '#27ae60';
            } else {
                statusElement.textContent = `⏰ 稼働時間外（現在時刻: ${data.current_time}）`;
                statusElement.style.color = '#e74c3c';
            }
            
            return data;
        } catch (error) {
            console.error('稼働時間チェックエラー:', error);
            return { is_working_hours: true };
        }
    }
    
    startWorkingHoursCheck() {
        // 1分ごとに稼働時間をチェック
        this.workingHoursInterval = setInterval(async () => {
            const workingHoursCheck = await this.checkWorkingHours();
            
            // 稼働時間外になったらタイマーを停止
            if (this.config.working_hours_enabled && 
                this.isRunning && 
                !workingHoursCheck.is_working_hours) {
                this.stopTimer();
                alert('稼働時間が終了しました');
            }
        }, 60000);
    }
    
    playNotificationSound() {
        const audio = document.getElementById('notification-sound');
        if (audio) {
            audio.play().catch(error => {
                console.log('通知音の再生に失敗:', error);
            });
        }
    }
    
    showNotification(message) {
        // 簡易通知表示
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            z-index: 9999;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            animation: slideIn 0.3s ease-out;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// アプリケーション初期化
document.addEventListener('DOMContentLoaded', () => {
    new SittingTimer();
});

// CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);