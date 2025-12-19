import boto3
import os

sns = boto3.client('sns')
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    processed_count = 0

    for record in event.get("Records", []):
        # Sprawdź, czy to event S3
        if "s3" in record:
            bucket = record["s3"]["bucket"]["name"]
            key = record["s3"]["object"]["key"]
            message = (
                f"An image has been uploaded!\n"
                f"Bucket: {bucket}\n"
                f"File: {key}\n"
                f"Download: https://{bucket}.s3.amazonaws.com/{key}"
            )
            try:
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=message,
                    Subject="New image uploaded"
                )
                processed_count += 1
                print(f"Wysłano notyfikację do SNS dla pliku: {key}")
            except Exception as exc:
                print(f"Błąd wysyłania powiadomienia do SNS: {exc}")
        else:
            print("To nie jest event S3, pomijam rekord.")

    print(f"Przetworzono {processed_count} plików z S3")
    return {"statusCode": 200, "body": f"Processed {processed_count} S3 records"}