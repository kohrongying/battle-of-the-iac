resource "aws_api_gateway_rest_api" "this" {
  name        = "apigw-${var.service.name}"
  description = "API Gateway for ${var.service.name}"
  endpoint_configuration {
    types = ["REGIONAL"]
  }
  policy = data.aws_iam_policy_document.resource_policies.json
}

data "aws_iam_policy_document" "resource_policies" {
  statement {
    sid = ""

    actions = [
      "execute-api:Invoke",
    ]

    principals {
      identifiers = ["*"]
      type = "*"
    }

    resources = [
      "*",
    ]
  }
}

resource "aws_api_gateway_resource" "this" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  parent_id   = aws_api_gateway_rest_api.this.root_resource_id
  path_part   = "psi"
}

resource "aws_api_gateway_method" "any" {
  rest_api_id                   = aws_api_gateway_rest_api.this.id
  resource_id                   = aws_api_gateway_resource.this.id
  http_method                   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = aws_api_gateway_rest_api.this.id
  resource_id             = aws_api_gateway_resource.this.id
  http_method             = aws_api_gateway_method.any.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${module.lambda.this_lambda_function_invoke_arn}:$${stageVariables.lambdaAlias}"
}