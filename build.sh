#!/bin/bash
echo "座りすぎタイマーV2 ビルドスクリプト"
echo "================================"

# 必要なパッケージのインストール
echo "PyInstallerをインストールしています..."
pip install -r requirements.txt

# 実行ファイルの作成
echo "実行ファイルを作成しています..."
pyinstaller --onefile --windowed --name timer --add-data "config.ini:." --add-data "tips.txt:." timer.py

# 配布用フォルダの作成
echo "配布用フォルダを作成しています..."
rm -rf dist_package
mkdir dist_package

# ファイルのコピー
echo "必要なファイルをコピーしています..."
cp dist/timer dist_package/
cp config.ini dist_package/
cp tips.txt dist_package/
cp README.md dist_package/

echo ""
echo "ビルドが完了しました！"
echo "配布用ファイルは dist_package フォルダにあります。"
echo ""