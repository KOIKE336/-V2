@echo off
echo 座りすぎタイマーV2 ビルドスクリプト
echo ================================

REM 必要なパッケージのインストール
echo PyInstallerをインストールしています...
pip install -r requirements.txt

REM 実行ファイルの作成
echo 実行ファイルを作成しています...
pyinstaller --onefile --windowed --name timer --add-data "config.ini;." --add-data "tips.txt;." timer.py

REM 配布用フォルダの作成
echo 配布用フォルダを作成しています...
if exist dist_package rmdir /s /q dist_package
mkdir dist_package

REM ファイルのコピー
echo 必要なファイルをコピーしています...
copy dist\timer.exe dist_package\
copy config.ini dist_package\
copy tips.txt dist_package\
copy README.md dist_package\

echo.
echo ビルドが完了しました！
echo 配布用ファイルは dist_package フォルダにあります。
echo.
pause