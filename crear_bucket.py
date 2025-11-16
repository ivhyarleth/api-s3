import json
import boto3
import os

s3 = boto3.client("s3")


def build_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body, ensure_ascii=False)
    }


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")

        bucket_name = body.get("bucket")
        if not bucket_name:
            return build_response(400, {
                "message": "Falta el campo 'bucket' en el cuerpo de la petición"
            })

        region = os.environ.get("AWS_REGION", "us-east-1")

        # Caso especial us-east-1
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )

        return build_response(200, {
            "message": "Bucket creado correctamente",
            "bucket": bucket_name,
            "region": region
        })

    except Exception as e:
        return build_response(500, {
            "message": f"Error al crear el bucket: {str(e)}"
        })
