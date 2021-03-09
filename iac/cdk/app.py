#!/usr/bin/env python3

from aws_cdk import core

# from cdk.cdk_stack import CdkStack
from psi_service.psi_service_stack import PSIServiceStack

# app = cdk.App()
# CdkStack(app, "cdk")

app = core.App()
PSIServiceStack(app,
  "psi-service-cdk-1",
  env={'region': 'ap-southeast-1'}
)

app.synth()
