# インサイダーゲームの裏側
## 概要
インサイダーゲームのバックエンドです。

## 開発について
### 環境構築
特にありません。
強いて言うなら、AWS環境があると良いです。

### 各ファイルについて
#### handler.py
Lambdaで実行されるファイルです。
メソッド単位で指定できるため、Lambda関数とPythonのメソッド名を揃えてあります。

### AWS環境について
#### DynamoDB
##### Player
プレイヤーの情報を保持するテーブル。
| カラム名 | 用途 |
|:|:-|
| id | 一意なID（datetime + player.name） |
| game_id | ゲームのID。同じ値のプレイヤーが同じ回の参加者。 |
| name | プレイヤー名 |
| role | 役職 |
| theme | お題 |
| stamp | 追加日時（Y-m-d H:i:s） |

##### Theme
お題の一覧を保持するテーブル。
| カラム名 | 用途 |
|:|:-|
| id | 一意なID。1〜カウントアップしていく。 |
| name | お題 |
| stamp | 追加日時（Y-m-d H:i:s） |

##### Sequence
AUTO INCREMENTを実現するためのシーケンステーブル。
| カラム名 | 用途 |
|:|:-|
| sequence_key | キー。対象とするテーブル名 |
| sequence | ID |

### デプロイについて
developへマージすると、Github Actionsによって自動的にデプロイ（ `serverless deploy -v` ）が行われます。
