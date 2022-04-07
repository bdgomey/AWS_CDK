#!/usr/bin/env python3

import aws_cdk as cdk

from project1.project1_stack import S3
from project1.project1_stack import EC2Stack

app = cdk.App()
S3(app, "project1")
EC2Stack(app, "ec2")
app.synth()
