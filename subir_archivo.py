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
        archivo = body.get("archivo")
        contenido = body.get("contenido")

        if not bucket or not directorio or not archivo or contenido is None:
            return build_response(400, {
                "message": (
                    "Faltan campos: 'bucket', 'directorio', "
                    "'archivo' o 'contenido'"
                )
            })

        if not directorio.endswith("/"):
            directorio = directorio + "/"

        key = f"{directorio}{archivo}"

        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=contenido.encode("utf-8")
        )

        return build_response(200, {
            "message": "Archivo subido correctamente",
            "bucket": bucket,
            "key": key
        })

    except Exception as e:
        return build_response(500, {
            "message": f"Error al subir el archivo: {str(e)}"
        })
