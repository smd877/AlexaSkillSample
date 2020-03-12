# 超簡単なAlexa Skillのサンプルをつくった

社内メンバーに向けたAmazon Alexa Skill開発の資料。  
なぜPythonなのかというと、慣れです。深い意味はない。(公式はnode.js推しかな？)

## 参考にしたもの

https://github.com/alexa/skill-sample-python-fact

こちらのサンプルがとてもシンプル。  
けれど、もっともっとシンプルにしてみました。

## 用意したもの

```
.
├── module
│   └── lambda_function.py
├── readme.md
└── skill.json
```

とりあえず用意したのは上のもの。  
Alexa Skills Kitとかは含んでいないので自前で用意する必要があります。  
その手順は以下の通り。

- python3系が使える環境にしておく。
- pipが使える環境にしておく。
- このリポジトリをcloneし、以下コマンドを実行する。

```
$ cd module/
$ pip install ask-sdk-core -t .
$ rm -rf certifi* chardet* idna* urllib3* six*
$ zip ../skill.zip -r .
```

Alexa Skills Kitのコアパッケージをインストールして今回のサンプルに不要そうなものを除去しています。  
(バックエンドをAWS Lambdaに上げる関係で、10MB以内にする必要がある。)

skill.jsonにスキルに設定する内容を書いています。  
invocationNameは 「体調気遣いさん」 です。

## 簡単な流れ

1. スキルを呼び出します 「アレクサ、体調気遣いさんを呼んで」
1. スキルが答えてくれます 「元気？「はい」か「いいえ」で答えてね！」
1. 「はい」か「いいえ」と答えましょう。
1. 答えた内容に応じてスキルが返答してくれます。
1. 標準ビルトインテントのいずれかを呼んだら「ヘルプかキャンセルかストップが呼ばれた！」と答えてくれます。

たったこれだけ。