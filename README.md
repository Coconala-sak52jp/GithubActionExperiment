# github actionsを用いてissue/wiki更新をSlackとtodoistへ通知する

## Slackへの通知
### Quick Start
1. 対象とするgithubリポジトリ（以降、github-reposと呼ぶ）に`.github/workflows`（以降wfディレクトリと呼ぶ）を準備する。
2. wfディレクトリに`slack-notification.yml`を配置する。
3. 宛先となるslackのワークスペース（以降、slack-wsと呼ぶ）を用意し、Incoming Webhookを登録する。
4. Incoming Webhookの設定ページで、あて先となるチャンネルを設定する。次に、Webhook URLを記録しておく。最後に「設定を保存する」を押して、保存する。
5. 再びgithub-reposへ戻り、シークレット変数を登録する。
   1. 'Settings->Secret'をポイントする。
   2. 'Add a new secret'をポイントし、`Name:SLACK_WEBHOOK`、`Value:Webhook URL（手順４．で記録したもの）`を設定する。
6.  `github-repos/.github/workflows/slack-notification.yml`を編集し、`SLACK_CHANNEL: github-actions-experiment`に、4. で設定したものと同じチャンネルを設定する。    
	e.g.) `SLACK_CHANNEL: my-favorite-chnnel`   
	＊＊ generalは接続時のパーミッションで跳ねられることがあるため注意 ＊＊
7. github-reposで新しいissueをopenしてみて、下記のような通知がslackに届けば成功。

![enter image description here](https://photos.app.goo.gl/5jnriYLHG7amAp1TA)

### issue更新仕様
githubのissueユースケース視点における通知のサポート範囲は、下記の通りです。
+ 新規issueのopen (New issue)
+ 新規issue発行時コメントの更新・変更
+ issueタイトル更新・変更
+ 担当者割当 (Assignees操作)
+ issueのクローズ ("Close issue" or "Close and comment")
+ issueの再オープン ("Reopen issue" or "Reopen and comment")


それぞれの事象が起きた時、設定した`SLACK_CHANNEL`に対して事象特有の通知が発行されます。  
それぞれの事象に対する通知内容は下記の通りです。

|ユースケース |タイトル欄の内容  |メッセージ欄の内容|
|--|--|--|
| 新規issueのopen |Issue:Opened  |issueのタイトル  |
| 新規issue発行時コメントの更新・変更 |Issue:Edited:body  |issueのタイトル   |
| issueタイトル更新・変更 |Issue:Edited:title  | issueのタイトル（更新・変更後の内容） |
|  issueのクローズ | Issue:Closed |issueのタイトル  |
|  issueの再オープン | Issue:Reopened |issueのタイトル  |

上表において、「タイトル欄」及び「メッセージ欄」の配置に関しては、[Slack Notify - GitHub Action](https://github.com/marketplace/actions/slack-notify#environment-variables)を参照下さい。

### issue comment更新仕様
issue commentは広い意味でissue操作の一種ですが、github actionsでのハンドリングはイベントレベルで区別されています。そのため、本workflow実装でもissue本体とは処理を分けています。
issue本体と同様にユースケース視点から見た通知のサポート範囲は下記の通りです。
+ 新規コメント追加 ("Comment" or  "Close and comment" or  "Reopen and comment")
+ コメント削除 (CommentMenu->Delete)
+ コメントの変更・更新 (CommentMenu->Edit)

それぞれの事象に対する通知内容は下表の通りです。

|ユースケース |タイトル欄の内容  |メッセージ欄の内容|
|--|--|--|
| 新規コメント追加 |Issue:comment:Created  |issueのタイトル  |
| コメント削除 |Issue:comment:Deleted  |issueのタイトル   |
| コメントの変更・更新 |Issue:comment:Edited  | issueのタイトル|

### wiki更新仕様
wiki更新に関し、ユースケース視点での通知サポート範囲は下記の通りです。
+ aaa

### カスタマイズ

## todoistへの通知


> Written with [StackEdit](https://stackedit.io/).

