@echo off
echo 座りすぎタイマーV2 ブラウザ版パッケージ作成
echo =====================================

REM 配布用フォルダの作成
echo 配布用フォルダを作成しています...
if exist browser_package rmdir /s /q browser_package
mkdir browser_package
mkdir browser_package\templates
mkdir browser_package\static
mkdir browser_package\static\css
mkdir browser_package\static\js

REM ファイルのコピー
echo 必要なファイルをコピーしています...
copy app.py browser_package\
copy config.ini browser_package\
copy tips.txt browser_package\
copy requirements.txt browser_package\
copy run_browser.bat browser_package\
copy run_browser.sh browser_package\

REM テンプレートとスタティックファイルのコピー
copy templates\index.html browser_package\templates\
copy static\css\style.css browser_package\static\css\
copy static\js\timer.js browser_package\static\js\

REM README作成
echo ブラウザ版用のREADMEを作成しています...
(
echo # 座りすぎタイマーV2 ブラウザ版
echo.
echo ## 起動方法
echo.
echo ### Windows
echo ```
echo run_browser.bat をダブルクリック
echo ```
echo.
echo ### Linux/macOS
echo ```
echo ./run_browser.sh
echo ```
echo.
echo ## 使用方法
echo 1. スクリプトを実行するとブラウザが自動で開きます
echo 2. http://localhost:5000 でアクセス可能です
echo 3. 終了するには Ctrl+C を押してください
echo.
echo ## 設定変更
echo config.ini ファイルを編集後、アプリを再起動してください
) > browser_package\README_BROWSER.md

REM ZIP ファイルの作成
echo ZIPファイルを作成しています...
if exist "座りすぎタイマーV2_ブラウザ版.zip" del "座りすぎタイマーV2_ブラウザ版.zip"
powershell -command "Compress-Archive -Path 'browser_package' -DestinationPath '座りすぎタイマーV2_ブラウザ版.zip'"

echo.
echo ブラウザ版パッケージが完成しました！
echo.
echo 作成されたファイル:
echo - browser_package/ フォルダ（配布用ファイル）
echo - 座りすぎタイマーV2_ブラウザ版.zip（配布用ZIPファイル）
echo.
pause