"""Helper functions to download files from the GCP bucket where they are stored"""

import os
from google.cloud import storage

bucket_name = os.getenv("GCP_BUCKET_NAME")

def list_files_in_storage() -> list[str]:
    """List all available files in bucket. Assumes the data in the bucket is public

    Returns
    -------
    list[str]
        List of filenames in bucket
    """
    storage_client = storage.Client.create_anonymous_client()
    blobs = storage_client.list_blobs(bucket_name)
    return [blob.name for blob in blobs]

def download_file_as_bytes(filename: str) -> bytes:
    """Download a given blob and store in memory as bytes.

    Parameters
    ----------
    filename : str
        File to download from bucket

    Returns
    -------
    bytes
        Downloaded file
    """
    storage_client = storage.Client.create_anonymous_client()
    bucket = storage_client.bucket(bucket_name)
    file = bucket.blob(filename)
    data_bytes = file.download_as_bytes()
    return data_bytes