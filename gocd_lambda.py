import os
import boto3
from base64 import b64decode

from go_wrapper.gocd_wrapper import GoCdWrapper


def decrypt_env(name):
    encrypted = os.environ[name]
    return boto3.client('kms').decrypt(CiphertextBlob=b64decode(encrypted))['Plaintext']


def lambda_handler(event, context):
    url = os.environ['URL']
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    pipeline_groups = os.getenv('PIPELINE_GROUPS')

    #password = decrypt_env('PASSWORD')

    go = GoCdWrapper(url, username, password, pipeline_groups)
    result = go.get_build_status()

    return result
