import boto3
import json
import base64
import os
import gzip

def lambda_handler(event, context):
    # ログイベントからメッセージを取得
    log_event = event['awslogs']['data']
    
    # Base64デコード後、gzipデコード
    compressed_data = base64.b64decode(log_event)
    uncompressed_data = gzip.decompress(compressed_data).decode('utf-8')
    
    # デコードしたデータをJSONとしてロード
    log_data = json.loads(uncompressed_data)
    
    # ログメッセージを取得
    log_message = log_data['logEvents'][0]['message']
    
    # エラーメッセージをチェック
    if 'ERROR' in log_message:
        # SNSトピックを指定して通知を送信
        sns = boto3.client('sns')
        sns.publish(
            TopicArn = os.environ['SNS_TOPIC_ARN'],
            Message = f'Error log detected: {log_message}',
            Subject = 'Error Log Notification'
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent successfully')
    }