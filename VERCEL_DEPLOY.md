# Vercelデプロイガイド

## 座りすぎタイマーV2 をVercelにデプロイする方法

### 🚀 自動デプロイ（推奨）

1. **GitHubリポジトリをVercelに接続**
   - [Vercel](https://vercel.com) にアクセス
   - GitHubアカウントでログイン
   - 「New Project」をクリック
   - このリポジトリ（KOIKE336/-V2）を選択
   - 「Import」をクリック

2. **自動設定**
   - Vercelが自動的に設定を検出します
   - そのまま「Deploy」をクリック

3. **デプロイ完了**
   - 数分でデプロイが完了
   - 提供されたURLでアクセス可能

### ⚙️ 環境変数設定（オプション）

Vercelの「Settings」→「Environment Variables」で以下を設定可能：

| 変数名 | デフォルト値 | 説明 |
|--------|-------------|------|
| `TIMER_MINUTES` | `60` | デフォルトタイマー時間（分） |
| `WORKING_HOURS_ENABLED` | `true` | 稼働時間制限の有効/無効 |
| `WORKING_HOURS_START` | `08:30` | 稼働開始時間 |
| `WORKING_HOURS_END` | `17:00` | 稼働終了時間 |
| `REMINDER_MESSAGE` | `座りすぎです！少しストレッチしましょう！` | リマインダーメッセージ |
| `AUTO_CLOSE_SECONDS` | `5` | 自動閉じ秒数 |
| `APP_TITLE` | `座りすぎタイマーV2 - Web版` | アプリタイトル |

### 🛠️ 手動デプロイ

```bash
# Vercel CLIのインストール
npm i -g vercel

# プロジェクトディレクトリで実行
vercel

# 初回設定
# - Set up and deploy? [Y/n] → Y
# - Which scope? → 個人アカウント選択
# - Link to existing project? [y/N] → N
# - Project name → 任意の名前
# - In which directory is your code located? → ./

# 以降の更新
vercel --prod
```

### 📁 ファイル構成（Vercel用）

```
座りすぎタイマーV2/
├── api/
│   └── index.py          # Vercel用Flaskアプリ
├── templates/
│   └── index.html        # HTMLテンプレート
├── static/
│   ├── css/style.css     # スタイルシート
│   └── js/timer.js       # JavaScript
├── vercel.json           # Vercel設定
├── requirements-vercel.txt # Python依存関係
└── .vercelignore         # 除外ファイル
```

### 🔧 設定の特徴

- **サーバーレス**: Flask アプリが Vercel Functions として動作
- **静的ファイル**: CSS/JS が自動的に配信
- **環境変数**: Vercel 環境変数で設定変更可能
- **自動HTTPS**: Vercelが自動的にHTTPS化
- **CDN**: 世界中のエッジロケーションから高速配信

### 🌍 デプロイ後のURL例

```
https://your-project-name.vercel.app
```

### 📱 機能

- ✅ タイマー機能
- ✅ リマインダー表示
- ✅ 健康ミニ知識
- ✅ 稼働時間制限
- ✅ レスポンシブデザイン
- ✅ リアルタイム進捗表示

### 🆓 無料枠

- Vercelの無料枠で十分動作
- 月間100GBまでの帯域幅
- 制限なしのプロジェクト数

### 🔄 更新方法

GitHubにプッシュするだけで自動的にデプロイされます：

```bash
git add .
git commit -m "更新内容"
git push origin main
```

### 💡 トラブルシューティング

**Q: デプロイエラーが発生する**
A: 
- `vercel.json` の設定を確認
- `requirements-vercel.txt` の依存関係を確認
- Vercelのログを確認

**Q: 静的ファイルが読み込まれない**
A:
- `vercel.json` のルーティング設定を確認
- ファイルパスが正しいか確認

**Q: 環境変数が反映されない**
A:
- Vercelダッシュボードで環境変数を確認
- デプロイを再実行