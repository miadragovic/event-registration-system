import os
from azure.storage.blob import BlobServiceClient

storage_conn_str = os.environ.get("STORAGE_CONN_STRING", "")

if storage_conn_str:
    blob_service_client = BlobServiceClient.from_connection_string(storage_conn_str)
else:
    blob_service_client = None  

def upload_file_to_blob(container: str, file_data: bytes, blob_name: str):
    if not blob_service_client:
        raise RuntimeError("Blob storage client not configured; set STORAGE_CONN_STRING")
    blob_client = blob_service_client.get_blob_client(container=container, blob=blob_name)
    blob_client.upload_blob(file_data, overwrite=True)

def download_blob_to_bytes(container: str, blob_name: str) -> bytes:
    if not blob_service_client:
        raise RuntimeError("Blob storage client not configured; set STORAGE_CONN_STRING")
    blob_client = blob_service_client.get_blob_client(container=container, blob=blob_name)
    return blob_client.download_blob().readall()
