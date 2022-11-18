# python-aws-lambda-powertools-routing

AWS Lambda Powertools for Python(<https://awslabs.github.io/aws-lambda-powertools-python/2.2.0/>)のツール群の内、event_handler(routting)の使い方を確認するために作成したコードです.
また、エラーレスポンスの返し方の例も確認できるようにコードを入れています。
(エラーレスポンスの返し方はPowertoolsとは関係ありません)

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

- GET (path パラメータなし) のリクエストの例
  - <http://127.0.0.1:3000/dev/v1/sample/hello>
  - レスポンス

    ```json
    {
        "message": "Hello World!"
    }
    ```

- GET (path パラメータあり) のリクエスト
  - フォーマット: <http://127.0.0.1:3000/dev/v1/sample/names/{parameter}>
  - リクエスト例: <http://127.0.0.1:3000/dev/v1/sample/names/taro>
  - レスポンス

    ```json
    {
        "success": true,
        "name": "taro"
    }
    ```

- POST (path パラメータあり) のリクエストの例
  - フォーマット: <http://127.0.0.1:3000/dev/v1/sample/ids/{id}>
  - リクエスト例: <http://127.0.0.1:3000/dev/v1/sample/names/99>
  - レスポンス

    ```json
    {
        "data": {
            "success": true,
            "id": "99"
        }
    }
    ```

- POST (path パラメータあり) のリクエストにて、エラーレスポンスを返す例
  - idが1000以上の時は、404エラーレスポンスを返すサンプルコードになっている
  - リクエスト例: <http://127.0.0.1:3000/dev/v1/sample/ids/2000>
  - レスポンス

    ```json
    {
        "statusCode": 404,
        "message": "Not found",
        "detail": "Unsent Data for the specified ID does not exist."
    }  
    ```

