import os
import uuid
import ibm_boto3
from ibm_botocore.exceptions import ClientError
from ibm_botocore.client import Config
import ibm_s3transfer.manager

def log_done():
    print ("DONE!\n")
def log_client_error(e):
    print ("CLIENT ERROR: {0}\n".format(e))
def log_error(msg):
    print("UNKNOWN ERROR: {0}\n".format(msg))
def get_uuid():
    return str(uuid.uuid4().hex)
def get_buckets():
    print("Retrieving list of buckets")
    try:
        bucket_list=cos_cli.list_buckets()
        for bucket in bucket_list["Buckets"]:
            print("Bucket Name:{0}".format(bucket["Name"]))
        log_done()
    except ClientError as be:
        log_client_error(be)
    except Exception as e:
        log_error("Unable to retrieve list buckets: {0}".format(e))
def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        imagearr=[]
        file_list = cos_cli.list_objects(Bucket=bucket_name)
        for file in file_list.get("Contents",[]):
            print("Item: {0} ({1} bytes).".format(file["Key"], file["Size"]))
            imagearr.append(file["Key"])
        log_done()
    except ClientError as be:
        log_client_error(be)
    except Exception as e:
        log_error("Unable to retrieve bucket contents: {0}".format(e))
    return imagearr
# Constants for IBM COS values


COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "Sws0lA7GhofJiR93QqNPtVQPWem7JZaUURWm-dlb_E5v" # eg "W00YixxxxxxxxxxMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_SERVICE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/2d011f0f2d914303980e8121f6b3930c:29fee78a-3b0d-4091-a381-0ea36794128d::" # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003xxxxxxxxxx1c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"
COS_AUTH_ENDPOINT="https://iam.cloud.ibm.com/identity/token"
COS_STORAGE_CLASS="Smart Tier"
# Create client

cos_cli = ibm_boto3.client("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_SERVICE_CRN,
    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)
try:
    get_buckets()
    imagearr=get_bucket_contents("raspberrybucket")
    print(imagearr)
except Exception as e:
    log_error("Main Prog Error: {0}".format(e))


