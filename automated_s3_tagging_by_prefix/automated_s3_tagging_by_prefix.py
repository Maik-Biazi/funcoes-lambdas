import boto3
import urllib.parse

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    # Verifica se tem prefixo (ex: Financeiro/arquivo.pdf)
    if '/' not in key:
        return {
            'statusCode': 200,
            'body': 'Objeto sem prefixo, nenhuma tag aplicada.'
        }

    prefix = key.split('/')[0]

    tags = {
        'TagSet': [
            {
                'Key': 'Departamento',
                'Value': prefix
            }
        ]
    }

    try:
        s3.put_object_tagging(Bucket=bucket, Key=key, Tagging=tags)
        return {
            'statusCode': 200,
            'body': f'Tag Departamento={prefix} aplicada ao objeto {key}'
        }
    except Exception as e:
        print(f"Erro ao aplicar tag: {e}")
        return {
            'statusCode': 500,
            'body': 'Erro ao aplicar tag.'
        }
