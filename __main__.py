#import pulumi
#from pulumi_aws import s3, Provider

#localstack_provider = Provider(
 #   "localstack",
  #  skip_credentials_validation=True,
   # skip_requesting_account_id=True,
    #s3_use_path_style=True,  # Force path-style addressing
    #endpoints=[{
     #   "s3": "http://localhost:4566",  # LocalStack S3 endpoint
      #  "sts": "http://localhost:4566",  # LocalStack STS endpoint
    #}],
#)


# Create an S3 bucket
#bucket = s3.Bucket(
 #   "csv-bucket",
  #  bucket="csv-bucket",
   # opts=pulumi.ResourceOptions(provider=localstack_provider),
#)
#pulumi.export("bucket_name", bucket.id)

import pandas as pd
import boto3
from pulumi import FileAsset

# Sample CSV content
csv_content = """Name,Age,City
Alice,30,New York
Bob,25,San Francisco
Charlie,35,Chicago
"""

# Write to a local file
file_path = "sample.csv"
with open(file_path, "w") as f:
    f.write(csv_content)

# Upload the file to the S3 bucket
s3_object = s3.BucketObject(
    "csv-file",
    bucket=bucket.id,
    source=FileAsset(file_path),
    key="sample.csv",
    opts=pulumi.ResourceOptions(provider=localstack_provider),
)

# Process the CSV after deployment
def process_csv(bucket_name, object_key):
    s3_client = boto3.client("s3", endpoint_url="http://localhost:4566")
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    csv_data = response["Body"].read().decode("utf-8")
    df = pd.read_csv(pd.compat.StringIO(csv_data))
    df["Age"] = df["Age"] + 1
    print(df)

# Resolve Pulumi outputs
bucket.id.apply(lambda b: process_csv(b, "sample.csv"))

