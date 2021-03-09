import pulumi
from pulumi_aws import lambda_
from iam import lambda_role
from variables import SERVICE_NAME

lambda_fn = lambda_.Function(
  "this",
  name=SERVICE_NAME,
  handler="lambda_function.lambda_handler",
  runtime="python3.8",
  role=lambda_role.arn,
  code=pulumi.FileArchive("./lambda_function.zip")
)