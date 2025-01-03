import pulumi
from pulumi_aws import s3, Provider

localstack_provider = Provider(
    "localstack",
    skip_credentials_validation=True,
    skip_requesting_account_id=True,
    s3_use_path_style=True,  # Force path-style addressing
    endpoints=[{
        "s3": "http://localhost:4566",  # LocalStack S3 endpoint
        "sts": "http://localhost:4566",  # LocalStack STS endpoint
    }],
)


 #Create an S3 bucket
bucket = s3.Bucket(
    "csv-bucket",
    bucket="csv-bucket",
    opts=pulumi.ResourceOptions(provider=localstack_provider),
)
pulumi.export("bucket_name", bucket.id)
