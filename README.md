# python-aws-lambda-powertools-routing

AWS Lambda Powertools for Python(<https://awslabs.github.io/aws-lambda-powertools-python/2.2.0/)のツール群の内、event_handler>の使い方を確認するために作成したコードです.

## PCでの実行前提

docker が動作していること

## PCでの実行手順

### Step 1 - ビルド

```sh
$ cd sam-httpapi
$ sam build
```

### Step 2 - APIをローカルでホスト

```sh
$ sam local start-api
```

### Step 3 - Postmanで以下のリクエストを送信して、各responseが戻ってくる事を確認できる

- リクエスト
GET <http://127.0.0.1:3000/dev/sample/hello>

  - レスポンス
{
    "message": "Hello World!"
}

- リクエスト
GET <http://127.0.0.1:3000/dev/sample/names/taro>

  - レスポンス
{
    "success": true,
    "name": "taro"
}

- リクエスト
POST <http://127.0.0.1:3000/dev/sample/ids/10>

  - レスポンス
{
    "data": {
        "success": true,
        "id": "10"
    }
}
