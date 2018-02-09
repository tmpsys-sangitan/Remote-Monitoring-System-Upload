Upload for Remote Monitoring System
====

Overview


## Description
<!-- 説明 簡潔に -->
Raspberry Piで動作し、Monostickからの受信データを[Remote Monitoring System](https://github.com/tmpsys-sangitan/Remote-Monitoring-System-H29)にアップロードする。

## Demo
<!-- 動作デモ アニメーションGIFがよく使われる -->
![demo](https://github.com/tmpsys-sangitan/Remote-Monitoring-System-Upload/blob/master/wiki/demo.gif)

## Usage
<!-- 使用方法 これ要る？ -->
    $ python upload.py [mode]

動作モードは二つある
- upload: クラウドにデータを送信する
- 指定なし: 画面に受信データを出力する

## Install
<!-- インストール方法 この場合はGAEにソースをクローンして稼働するまで -->
    $ git clone https://github.com/tmpsys-sangitan/Remote-Monitoring-System-Upload.git

## Author
<!-- 著者 卒業研究なので学校名義で -->
[Ibaraki Prefectural Junior College of Industrial Technology](http://www.ibaraki-it.ac.jp/)
