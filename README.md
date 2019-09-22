# Twitter に掲載されている漫画を読みやすくするwebサービス

- [リリースしました](https://twmangaview.herokuapp.com)

## できてる
- スレッド形式の連載の先頭ツイートから画像を取得
- 引用形式の連載の先頭ツイートから画像を取得
- 書籍ビューワ
- サムネイル表示
- タイトル/URL/作者ID 検索
- ユーザ認証
- お気に入り機能
- ユーザの取り込んだ書籍の一覧

## たぶんできてる
- 非画像つきスレッド対策
- 非画像つき引用対策

## 考える
- ビューワの出来が悪いのでもっと良くする
- 書籍の削除

## モチベがあれば
- スレッドの途中からでも取得
- 引用の途中からでも取得
- その他の連載形式に対応

## わからない
- API 上限対策

___

## 利用したもの

### Python Twitter tools
一部関数を引用  
Copyright (c) 2008 Mike Verdone  
Released under the MIT license  
https://github.com/sixohsix/twitter/blob/master/LICENSE