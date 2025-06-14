import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files['file']
        filename = file.filename

        blob_service_client = BlobServiceClient.from_connection_string(os.environ["AzureWebJobsStorage"])
        container_client = blob_service_client.get_container_client("cloudfilescontainer")
        container_client.upload_blob(name=filename, data=file.stream, overwrite=True)

        return func.HttpResponse("Upload successful", status_code=200)

    except Exception as e:
        logging.error(f"Upload error: {e}")
        return func.HttpResponse("Upload failed", status_code=500)
