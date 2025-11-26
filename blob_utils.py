import os
from azure.storage.blob import BlobServiceClient

storage_conn_str = os.environ["STORAGE_CONN_STRING"]
blob_service_client = BlobServiceClient.from_connection_string(storage_conn_str)

def upload_file_to_blob(container: str, file_data: bytes, blob_name: str):
    blob_client = blob_service_client.get_blob_client(container=container, blob=blob_name)
    blob_client.upload_blob(file_data, overwrite=True)

def download_blob_to_bytes(container: str, blob_name: str) -> bytes:
    blob_client = blob_service_client.get_blob_client(container=container, blob=blob_name)
    return blob_client.download_blob().readall()  
