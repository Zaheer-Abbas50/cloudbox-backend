import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        filename = req.params.get('filename')
        if not filename:
            return func.HttpResponse("Filename required", status_code=400)

        blob_service_client = BlobServiceClient.from_connection_string(os.environ["AzureWebJobsStorage"])
        container_client = blob_service_client.get_container_client("cloudfilescontainer")
        container_client.delete_blob(blob=filename)

        return func.HttpResponse("Deleted successfully", status_code=200)

    except Exception as e:
        logging.error(f"Delete error: {e}")
        return func.HttpResponse("Delete failed", status_code=500)
