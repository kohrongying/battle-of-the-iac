module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "1.43.0"

  function_name = "${var.service.name}-webhook-lambda"
  description   = "My awesome lambda function"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"

  publish = true
  source_path = "lambda_function.py"
  allowed_triggers = {
    APIGatewayAny = {
      service    = "apigateway"
      source_arn = "${aws_api_gateway_rest_api.this.execution_arn}/*/*/*"
    }
  }
}

module "alias_dev" {
  source = "terraform-aws-modules/lambda/aws//modules/alias"

  refresh_alias = false

  name = "dev"

  function_name    = module.lambda.this_lambda_function_name
  function_version = module.lambda.this_lambda_function_version

  allowed_triggers = {
    DevAPIGatewayAny = {
      service    = "apigateway"
      source_arn = "${aws_api_gateway_rest_api.this.execution_arn}/*/*/*"
    }
  }
}

module "alias_prod" {
  source = "terraform-aws-modules/lambda/aws//modules/alias"

  refresh_alias = false

  name = "prod"

  function_name    = module.lambda.this_lambda_function_name
  function_version = module.lambda.this_lambda_function_version

  allowed_triggers = {
    ProdAPIGatewayAny = {
      service    = "apigateway"
      source_arn = "${aws_api_gateway_rest_api.this.execution_arn}/*/*/*"
    }
  }
}

