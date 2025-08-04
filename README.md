# 顔認証による打刻ツール（Face Recognition Attendance System）
## プロジェクト概要

本プロジェクトは、Pythonライブラリface_recognitionを用いて、顔認証による出勤・退勤の打刻処理を自動化するPoC（概念実証）ツールです。打刻情報はローカルのSQLiteデータベースに保存され、さらにGoogle SpreadsheetとSlackへの通知連携も可能です。

## 使用技術・ライブラリ

- **開発環境**: VSCode（MacOS / Windows 両対応）
- **言語**: Python3
- **主要ライブラリ・API**:  
  - `face_recognition`：顔検出・照合  
  - `opencv-python`：カメラ映像の取得と表示 
  - `sqlite3`：ローカルデータベース管理（出勤/退勤ログ）
  - `gspread`：Google Spreadsheet API 
  - `dotenv`：環境変数管理（APIキーなどの秘匿）
  - `requests`：Slack Webhook 経由での通知送信

## デモ

「動画は準備中」

## 機能一覧

  - 顔画像の自動登録・読み込み
  - カメラからリアルタイムで顔認証を実施
  - 出勤・退勤の切り替え自動判定（直前のステータスに応じて切替）
  - SQLiteへ打刻ログを保存
  - Google Spreadsheetへ打刻履歴を追記
  - Slack通知によるリアルタイム報告（Webhook）


## 拡張性・カスタマイズ例

本Pythonツールには、さらに改善・拡張できる余地があります。ご要望に応じて、以下のような対応が可能です。

  - 打刻データの他システム連携（例：Pleasanter、Salesforceなど）
  - 通知の送信先をSlack以外に変更（例：Chatwork、LINE公式アカウント、Discordなど）
  - モバイル端末や社内端末との連携
  - Dockerによるデプロイ構成の簡略化

## ご相談・お問い合わせ

##### 本ツールの導入・カスタマイズをご希望の方、または類似プロジェクトにご関心のある方は、お気軽にご相談ください。





