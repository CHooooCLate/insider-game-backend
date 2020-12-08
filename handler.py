# coding: utf-8
import boto3
import datetime
import json
import random

# デバッグするときに使う
from pprint import pprint

from boto3.dynamodb.conditions import Key, Attr

# DynamoDBオブジェクトの作成
dynamodb = boto3.resource('dynamodb')
playerTable = dynamodb.Table('Player')
themeTable = dynamodb.Table('Theme')
sequenceTable = dynamodb.Table('Sequence')

def regist(event, context):
    # body部の取得
    body = event['body']
    players = body['players']

    sequenceKey = 'Theme'
    themeCount = sequenceTableget.get_item(
        Key = {
            'sequence_key' : sequenceKey
        }
    )

    # ランダムにテーマ取得
    num = random.randint(1, themeCount)
    theme = themeTable.get_item(
        Key = {
            'id' : str(num)
        }
    )

    roleList = {}
    for i in range(len(players)):
        if i == 0:
            roleList[i] = 'insider'
        elif i == 1:
            roleList[i] = 'master'
        else:
            roleList[i] = 'common'

    datetimeFormat = datetime.datetime.today()

    gameId = datetimeFormat.strftime("%Y%m%d%H%M%S");

    for player in players:
        # プレイヤーごとに役職選択
        role = random.choice(list(roleList.items()))

        del roleList[role[0]]

        # プレイヤーのレコードを追加
        playerTable.put_item(
            Item = {
                'id' : datetimeFormat.strftime("%Y%m%d%H%M%S") + player,
                'game_id' : gameId,
                'name' : player,
                'theme' : theme['Item']['name'],
                'role' : role[1],
                'stamp' : datetimeFormat.strftime("%Y/%m/%d %H:%M:%S")
            }
        )

    # レスポンスデータの作成
    response = {
        "statusCode": 200,
        "body": {'gameId': gameId}
    }

    return response

def confirm(event, context):
    pprint(event['query']['gameId'])

    players = playerTable.scan(
         FilterExpression=Attr('game_id').eq(event['query']['gameId'])
    )
    pprint(players)
    # レスポンスデータの作成
    response = {
        "statusCode": 200,
        "body": {'players': players['Items']}
    }

    return response

def addTheme(event, context):
    # リクエストからテーマの取得
    theme = event['body']['theme']

    sequenceKey = 'Theme'

    # プレイヤーのレコードを追加
    res = sequenceTable.update_item(
        Key= {
            'sequence_key': sequenceKey
        },
        UpdateExpression="ADD #name :increment",
        ExpressionAttributeNames={
            '#name':'sequence'
        },
        ExpressionAttributeValues={
            ":increment": int(1)
        },
        ReturnValues="UPDATED_NEW"
    )

    datetimeFormat = datetime.datetime.today()

    themeTable.put_item(
        Item = {
            'id' : str(res['Attributes']['sequence']),
            'name' : theme,
            'stamp' : datetimeFormat.strftime("%Y/%m/%d %H:%M:%S")
        }
    )

    # レスポンスデータの作成
    response = {
        "statusCode": 200,
        "body": {'id': str(res['Attributes']['sequence'])}
    }

    return response

class UnAuthorizationError(Exception):
    """
    認証失敗の独自Exceptionクラス
    @extends Exceptionクラスを継承
    """
    def __init__(self, code, data):
        """
        コンストラクタ
        @Param code レスポンスコード
        @Param data レスポンスデータ
        """
        self.code = code
        self.data = data

    def __str__(self):
        """
        文字列変換メソッド
        """
        response = {
           'status': 'HTTP/1.1 401 Unauthorized',
           'statusCode': self.code,
           'headers': {
               'Date': '2018/07/26 18:27:30',
               'Content-Type': 'application/octet-stream',
               'Accept-Charset': 'UTF8'
           },
           'body': {
               'result': self.code,
               'data': self.data
           }
        }
        return response
