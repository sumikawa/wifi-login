## これは何

公衆無線LAN(Public WiFi)に自動ログインするスクリプトです。SSIDに接続後、本コマンドを実行してください。

GUIでログイン認証画面をクリックするより素早くログインが完了します。

## 対応している公衆無線LAN

2025/12時点で下記の公衆無線LANに対応しています。

|店舗|ユーザ名|パスワード|備考|
|--|--|--|--|
|スターバックス||||
|すかいらーくグループ|||ガストで動作確認|
|マクドナルド|WIFI_MCD_EMAIL|WIFI_MCD_PASSWORD||

これ以外は対応していません。Pull Requestをお待ちしています。

## 事前準備

下記のコマンドを実行してください。システムに対する設定変更のためroot権限が必要です。

```
sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.captive.control Active -boolean false
```

これはCaptive Network Assistant (画面中央に認証画面を表示するミニブラウザ)を無効にするためのコマンドです。Captive Network Assistant が有効に場合、無線LANの認証が完了するまで、MacOSは自身以外の通信を全てブロックするため、本スクリプトが動作しません。

また、依存ライブラリを下記のコマンドでインストールしてください。

```
pip install -r requirements.txt
```

スクリプトを適当な実行パスにコピーしてください

```
cp wifi_login.py /somewhere/path/bin/
```

## 使い方

公衆無線LANに接続したら、下記コマンドを実行してください。公衆無線LAN種別を自動的に検知して、ログインを行います。

```
wifi_login.py
```

## 注意

無効にしたCaptive Network Assistantを再有効したい場合は下記を実行してください。

```
sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.captive.control Active -boolean true
```
