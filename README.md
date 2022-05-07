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
RDS_SECRET_ID='YOUR_PARAM' python3 -m uvicorn main:app --host 0.0.0.0

# バックグラウンド起動+ログ
mkdir ~/log/
RDS_SECRET_ID='YOUR_PARAM' nohup python3 -m uvicorn main:app --host 0.0.0.0 > ~/log/fastapi.log &
# パスが通っていればこちらでも
uvicorn main:app --host 0.0.0.0
```


```sql
-- テーブル定義とサンプルデータINSERT
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

`EC2 Amazon Linux 2 のユーザーデータ`
```bash
#!/bin/bash

yum update -y
yum install git gcc -y
amazon-linux-extras install python3.8 postgresql12 -y
ln -fs /usr/bin/python3.8 /usr/bin/python3

sudo -u ec2-user python3 -m pip install pip --upgrade
sudo -u ec2-user python3 -m pip install wheel fastapi uvicorn[standard] boto3 Jinja2 sqlalchemy psycopg2-binary python-multipart

sudo -u ec2-user git clone https://github.com/sugikeitter/FastApi-Jinja-SQLAlchemy.git /home/ec2-user/FastApi-Jinja-SQLAlchemy/
sudo -u ec2-user mkdir /home/ec2-user/log

# systemdの設定
cat <<EOF > /etc/systemd/system/fastapi.service
[Unit]
Description=fastapi
After=network-online.target

[Service]
EnvironmentFile=/etc/sysconfig/fastapi_env
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/FastApi-Jinja-SQLAlchemy
ExecStart=/bin/python3 -m uvicorn main:app --host 0.0.0.0
ExecStop=/bin/kill -s TERM $MAINPID

[Install]
WantedBy=multi-user.target
EOF

# $YOUR_PARAM は書き換え
cat <<EOF > /etc/sysconfig/fastapi_env
RDS_SECRET_ID='$YOUR_PARAM'
EOF

systemctl start fastapi
```