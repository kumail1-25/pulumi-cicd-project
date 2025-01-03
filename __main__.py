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

