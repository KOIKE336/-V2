#!/bin/bash
echo "座りすぎタイマーV2 ブラウザ版 起動スクリプト"
echo "======================================"

# 必要なパッケージのインストール
echo "必要なパッケージをインストールしています..."
pip install flask>=2.3.0

# Flaskアプリケーション起動
echo "ブラウザ版アプリケーションを起動しています..."
echo "ブラウザが自動で開きます..."
echo "終了するには Ctrl+C を押してください"
echo ""
python3 app.py