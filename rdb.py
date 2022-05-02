import json
import os

import boto3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import const

ssm = boto3.client('ssm', region_name=const.AWS_REGION)
secmgr = boto3.client('secretsmanager', region_name=const.AWS_REGION)


def get_rdb_url_and_pass():
    response = ssm.get_parameters(
        Names=['rds-pass'],
        WithDecryption=True
    )
    for parameter in response['Parameters']:
        return parameter['Value']


def get_rdb_url_and_pass_from_secmgr():
    secrets_value = secmgr.get_secret_value(SecretId=os.getenv('RDS_SECRET_ID', ''))
    secstr_dict = json.loads(secrets_value.get('SecretString', '{}'))
    return "postgresql://{username}:{password}@{host}/{dbname}".format(
        username=secstr_dict.get('username'),
        password=secstr_dict.get('password'),
        host=secstr_dict.get('host'),
        dbname=secstr_dict.get('username'),
    )


def get_rdb_url_and_pass_read():
    response = ssm.get_parameters(
        Names=['rds-pass-read'],
        WithDecryption=True
    )
    for parameter in response['Parameters']:
        return parameter['Value']


# ex) "postgresql://postgres:XXX@sandbox-aurora-postgres-02.cluster-c1glrtlijepc.ap-northeast-1.rds.amazonaws.com/sandbox"
SQLALCHEMY_DATABASE_URL = get_rdb_url_and_pass_from_secmgr()
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 別のDBエンドポイントを利用する場合
# SQLALCHEMY_DATABASE_URL_READ = get_rdb_url_and_pass_read()
# engine_read = create_engine(
#     SQLALCHEMY_DATABASE_URL_READ, connect_args={}
# )
# SessionLocal_read = sessionmaker(autocommit=False, autoflush=False, bind=engine_read)

Base = declarative_base()
