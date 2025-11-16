import json
import boto3

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
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        elif body is None:
            body = {}

        bucket = body.get("bucket")
        directorio = body.get("directorio")

        if not bucket or not directorio:
            return build_response(400, {
                "message": "Faltan campos 'bucket' y/o 'directorio'"
            })

        if not directorio.endswith("/"):
            directorio = directorio + "/"

        s3.put_object(Bucket=bucket, Key=directorio)

        return build_response(200, {
            "message": "Directorio creado correctamente",
            "bucket": bucket,
            "directorio": directorio
        })

    except Exception as e:
        return build_response(500, {
            "message": f"Error al crear el directorio: {str(e)}"
        })
