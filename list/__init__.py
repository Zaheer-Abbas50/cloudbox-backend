import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        blob_service_client = BlobServiceClient.from_connection_string(os.environ["AzureWebJobsStorage"])
        container_client = blob_service_client.get_container_client("cloudfilescontainer")
        blobs = container_client.list_blobs()

        file_names = [blob.name for blob in blobs]
        return func.HttpResponse(json.dumps(file_names), mimetype="application/json")

    except Exception as e:
        logging.error(f"List error: {e}")
        return func.HttpResponse("Listing failed", status_code=500)
