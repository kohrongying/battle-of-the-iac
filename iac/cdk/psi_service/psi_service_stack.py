from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_lambda as lambda_)


class PSIServiceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        SERVICE_NAME = "sg-psi-bot"

        handler = lambda_.Function(self, f'{SERVICE_NAME}-lambda',
                    runtime=lambda_.Runtime.PYTHON_3_8,
                    code=lambda_.Code.from_asset("resources"),
                    handler="lambda_function.lambda_handler"
        )

#         api = apigateway.LambdaRestApi(self, f"{SERVICE_NAME}-api", {
#           handler: handler
#         })

#         lambda_integration = apigateway.LambdaIntegration(handler,
#                 request_templates={"application/json": '{ "statusCode": "200" }'})
#
#         api.root.add_method("ANY", lambda_integration)