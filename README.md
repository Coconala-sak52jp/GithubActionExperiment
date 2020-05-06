
# github actionsを用いてissue/wiki更新をSlackとtodoistへ通知する

## リリースパッケージの構成
ツリー構成を下記に示します。

```
GithubActionExperiment
|-- .github
|   `-- workflows
|       |-- todoist-notification.yml
|       |-- slack-notification.yml
|       `-- my-workflow.yml.bak
|-- CheckList.xlsx
|-- QA.txt
`-- README.md
```

主なコンテンツについて説明します。
### workflow
`.github/workflows`には、slack通知及びtosoist通知に用いる`slack-notification.yml`及び`todoist-notification.yml`があり、これらに関しては後述します。  
my-workflow.yml.bakは、開発用に用いたworkflowのバックアップであり、参考資料として入れてあります。githubのactionとworkflowで参照出来る*Context Information*を収集する機能を持っており、workflowの機能を拡張する際に、どのような情報を用いるべきか判断する等の目的で使用できます。
### CheckList.xlsx
`slack-notification.yml`及び`todoist-notification.yml`の動作テスト結果です。

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

![slack通知表示例](https://user-images.githubusercontent.com/16172761/81192944-c69a9380-8ff5-11ea-814d-a9e1a93f2468.png)

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
+ 新規ページの作成
+ 既存ページの編集

それぞれの事象に対する通知内容は下表の通りです。

|ユースケース |タイトル欄の内容  |メッセージ欄の内容|
|--|--|--|
| 新規ページの作成 |Wiki:Created  |ページのタイトル  |
| 既存ページの編集 |Wiki:Edited  |ページのタイトル |



### カスタマイズ
`slack-notification.yml`においてカスタマイズが必須または可能な箇所は、`env:`のみです。

```
    # -- action == open --
    - name: If action is open
      if: ${{github.event.action == 'opened'}}
      uses: rtCamp/action-slack-notify@v2.0.0
      env:
        SLACK_CHANNEL: github-actions-experiment
        SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
        SLACK_TITLE: Issue:Opened
        SLACK_MESSAGE: ${{github.event.issue.title}}
```
上記は一例として、issueイベントのOpen actionが発生した時のslack通知設定を示しています。上記においてカスタマイズが必須なのは`SLACK_CHANNEL`であり、Quick Startで説明した通り、通知の宛先となるSlackのチャンネルを指定する必要があります。一方、`SLACK_WEBHOOK`は基本的に変更禁止です（github-reposに設定するsecretのNameを、`SLACK_WEBHOOK`以外に変更した場合を除く）。  
それ以外の変数はその目的を逸しない限り特に制約はないので、自由に設定することが出来ます。詳細は、[Slack Notify - GitHub Action](https://github.com/marketplace/actions/slack-notify#environment-variables)をご参照願います。

## todoistへの通知
### Quick Start
1. 対象とするgithubリポジトリ（以降、github-reposと呼ぶ）に`.github/workflows`（以降wfディレクトリと呼ぶ）を準備する。
2. wfディレクトリに`todoist-notification.yml`を配置する。
3. 宛先となるtodoistのプロジェクト（以降、todo-prjと呼ぶ）を用意する。
4. todo-prjのAPIトークンを下記のように取得する。
   1. todo-prjのフロントページで「歯車アイコン→設定」を選ぶ
   2. 左側のメニューペインから「連携機能」を選ぶ
   3. 最下部のAPIトークンを記録する
5. 再びgithub-reposへ戻り、シークレット変数を登録する。
   1. 'Settings->Secret'をポイントする。
   2. 'Add a new secret'をポイントし、`Name:TODOIST_TOKEN`、`Value:APIトークン（手順４．で記録したもの）`を設定する。
3. github-reposで新しいissueをopenしてみて、下記のような通知がtodoistに届けば成功。


### issue更新仕様
githubのissueユースケース視点における通知のサポート範囲は、下記の通りです。
+ 新規issueのopen (New issue)

> 理想的にはgithub-repos上で行われるissueのオペレーションに同期して、todoistのタスクの状態が更新されていくべきですが、現在手に入るgithub actionsのリソースには、このような機能を提供するものは残念ながら存在しないようです。   

通知は、todo-prjのインボックスに入ります。githiub-reposで作成したissueのタイトルが、そのままtodo-prjのタスク名になります。

### カスタマイズ
todoist通知仕様にはカスタマイズできる部分はありません。

