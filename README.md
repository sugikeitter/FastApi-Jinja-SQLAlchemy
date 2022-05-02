```shell
# 環境設定+Python+FastAPI,boto3インストール
yum update -y
# PostgreSQLを利用する場合は'postgresql gcc python3-devel postgresql-devel'も必要
yum install git gcc -y
### Amazon Linux 2
amazon-linux-extras install python3.8 postgresql12 -y
ln -fs /usr/bin/python3.8 /usr/bin/python3

# Pythonの依存パッケージ
python3 -m pip install pip --upgrade    
python3 -m pip install wheel fastapi uvicorn[standard] boto3 Jinja2 sqlalchemy psycopg2-binary python-multipart

# 起動
python3 -m uvicorn main:app --host 0.0.0.0
# パスが通っていればこちらでも
uvicorn main:app --host 0.0.0.0
```


```sql
CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR ( 100 ) NOT NULL,
    created_on TIMESTAMP NOT NULL,
    updated_on TIMESTAMP NOT NULL
    );

INSERT INTO books (
    title,
    created_on,
    updated_on
)
VALUES (
    'モブプログラミング・ベストプラクティス ソフトウェアの品質と生産性をチームで高める',
    current_timestamp,
    current_timestamp
),
(
    'リーダブルコード ―より良いコードを書くためのシンプルで実践的なテクニック',
    current_timestamp,
    current_timestamp
);
```