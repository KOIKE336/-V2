@echo off
echo 座りすぎタイマーV2 完全ビルドスクリプト（ZIP作成込み）
echo ================================================

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

REM ZIP ファイルの作成
echo ZIPファイルを作成しています...
if exist "座りすぎタイマーV2.zip" del "座りすぎタイマーV2.zip"
powershell -command "Compress-Archive -Path 'dist_package' -DestinationPath '座りすぎタイマーV2.zip'"

echo.
echo ビルドが完了しました！
echo.
echo 作成されたファイル:
echo - dist_package/ フォルダ（配布用ファイル）
echo - 座りすぎタイマーV2.zip（配布用ZIPファイル）
echo.
echo このZIPファイルを他のPCに転送して使用してください。
echo.
pause