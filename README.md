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
|JR東日本|WIFI_COMMON_EMAIL||メールに送付される認証URLは自身でクリックが必要|

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

ユーザ名とパスワードの入力が必要な公衆無線WiFi(例: マクドナルド)を利用する場合は、```~/.env```ファイルを作成して、下記の行を記述してください。
イコールの左側の文字列(環境変数)は、公衆無線WiFiごとに変わります。
[対応している公衆無線LAN](#%E5%AF%BE%E5%BF%9C%E3%81%97%E3%81%A6%E3%81%84%E3%82%8B%E5%85%AC%E8%A1%86%E7%84%A1%E7%B7%9Alan)を参照してください。

```
WIFI_MCD_EMAIL = your_email_adderess
WIFI_MCD_PASSWORD = your_password
```

## 使い方

公衆無線LANに接続したら、下記コマンドを実行してください。公衆無線LAN種別を自動的に検知して、ログインを行います。

```
wifi_login.py
```

## 1Passwordユーザー

[注意] 作者の環境では```op run```コマンドの動作が不安定で、想定通りに動作しないことが多々あります。

1Passwordユーザーは```~/.env```ファイルにパスワードを記述せずに、```op://``` から始まるリファレンスを設定してください。
1Password CLI経由でスクリプトを実行することで、パスワードをセキュアに保管できます。

```
WIFI_MCD_EMAIL = op://Private/Mcdonalds/username
WIFI_MCD_PASSWORD = op://Private/Mcdonalds/password
```

```
op run -- wifi_login.py
```

詳細は、1Password CLIの[マニュアル](https://developer.1password.com/docs/cli/reference/commands/run/)を参照ください。

## 注意

本スクリプトが未対応の公衆無線LANに接続したい場合は、ブラウザで http://captive.apple.com/ を開いてください。

無効にしたCaptive Network Assistantを再有効したい場合は下記を実行してください。

```
sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.captive.control Active -boolean true
```
