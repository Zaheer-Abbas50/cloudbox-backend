import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import os
from datetime import datetime, timedelta

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        filename = req.params.get('filename')
        if not filename:
            return func.HttpResponse("Filename required", status_code=400)

        conn_str = os.environ["AzureWebJobsStorage"]
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        blob_client = blob_service_client.get_blob_client(container="cloudfilescontainer", blob=filename)

        sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name="cloudfilescontainer",
            blob_name=filename,
            account_key=blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(minutes=10)
        )

        url = f"https://{blob_service_client.account_name}.blob.core.windows.net/cloudfilescontainer/{filename}?{sas_token}"
        return func.HttpResponse(url)

    except Exception as e:
        logging.error(f"Download error: {e}")
        return func.HttpResponse("Download failed", status_code=500)
