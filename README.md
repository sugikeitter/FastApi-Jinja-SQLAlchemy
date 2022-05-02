```shell
# 環境設定+Python+FastAPI,boto3インストール
yum update -y
# PostgreSQLを利用する場合は'postgresql gcc python3-devel postgresql-devel'も必要
yum install python3 postgresql gcc python3-devel postgresql-devel -y

# Pythonの依存パッケージ
python3 -m pip install pip --upgrade    
python3 -m pip install fastapi uvicorn boto3 Jinja2 sqlalchemy
# python3 -m pip install psycopg2 pydantic

# 起動
uvicorn main:app --host 0.0.0.0
```