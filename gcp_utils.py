import pickle

from google.cloud import storage
from tempfile import NamedTemporaryFile


def upload_blob(project_id, bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

def load_blob(project_id, bucket_name, destination_path, filename):
    storage_client = storage.Client(project=project_id)

    with NamedTemporaryFile(mode='rb') as tempfile:
        gcs_path = os.path.join(destination_path, f'{filename}')
        storage_client.bucket(bucket_name).blob(gcs_path).download_to_filename(tempfile.name)
        tempfile.seek(0)
        return pickle.load(tempfile)


def dump_and_upload(obj, filename, project_id, bucket_name, destination_file_name):
    # temp storage for lambda
    pickle.dump(obj, open(f"{filename}.pkl", "wb"))

    # util function to upload buy history to storage
    upload_blob(project_id=project_id,
                    bucket_name=bucket_name,
                    source_file_name=f"{filename}.pkl",
                    destination_blob_name=f"{destination_file_name}")
