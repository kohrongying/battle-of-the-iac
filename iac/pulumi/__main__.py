"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import apigateway, lambda_
from lambda_fn import lambda_fn
from variables import SERVICE_NAME

rest_api = apigateway.RestApi("this",
  name=f'apigw-{SERVICE_NAME}',
  endpoint_configuration=apigateway.RestApiEndpointConfigurationArgs(types="REGIONAL")
)


rest_api_policy = apigateway.RestApiPolicy("this",
    rest_api_id=rest_api.id,
    policy=rest_api.execution_arn.apply(lambda execution_arn: f"""{{
  "Version": "2012-10-17",
  "Statement": [
    {{
      "Effect": "Allow",
      "Principal": {{
        "AWS": "*"
      }},
      "Action": "execute-api:Invoke",
      "Resource": "{execution_arn}/*/*/*"
    }}
  ]
}}
"""))

method = apigateway.Method(
    'proxy_root',
    rest_api=rest_api,
    resource_id=rest_api.root_resource_id,
    http_method='ANY',
    authorization='NONE'
)

response200 = apigateway.MethodResponse("response200",
    rest_api=rest_api.id,
    resource_id=method.resource_id,
    http_method=method.http_method,
    status_code="200")

integration = apigateway.Integration(
    'lambda_root',
    rest_api=rest_api,
    resource_id=method.resource_id,
    http_method=method.http_method,
    integration_http_method='POST',
    type='AWS_PROXY',
    request_templates={
      "application/json": "{\"statusCode\": 200}"
    },
    uri=lambda_fn.invoke_arn
)

integration_response = apigateway.IntegrationResponse("integrationResponse",
    rest_api=rest_api.id,
    resource_id=method.resource_id,
    http_method=method.http_method,
    status_code=response200.status_code,
    response_templates={
       "text/plain": "Empty",
    })

deployment = apigateway.Deployment(
    'first',
    rest_api=rest_api,
    stage_name="dev",
    opts=pulumi.ResourceOptions(depends_on=[integration])
)

"""
error: aws:lambda/permission:Permission resource 'apigateway_invoke_lambda_permission' has a problem: "source_arn" (<pulumi.output.Output object at 0x1136f43d0>/*/*/*) is an invalid ARN: arn: invalid prefix
"""
lambda_permission = lambda_.Permission(
  "apigateway_invoke_lambda_permission",
  action="lambda:InvokeFunction",
  principal="apigateway.amazonaws.com",
  source_arn=rest_api.execution_arn.apply(
    lambda execution_arn: execution_arn + "/*/*/*"
  ),
  function=lambda_fn.arn
)