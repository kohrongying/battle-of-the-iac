resource "aws_api_gateway_stage" "stage" {
  count = length(var.stages)
  stage_name    = var.stages[count.index]
  rest_api_id   = aws_api_gateway_rest_api.this.id
  deployment_id = aws_api_gateway_deployment.deployment[count.index].id

  variables = {
    lambdaAlias = var.stages[count.index]
  }

  lifecycle {
    ignore_changes = [deployment_id]
  }
}

resource "aws_api_gateway_deployment" "deployment" {
  count = length(var.stages)
  rest_api_id   = aws_api_gateway_rest_api.this.id
  stage_name    = var.stages[count.index]
  depends_on = [aws_api_gateway_integration.integration]
}
