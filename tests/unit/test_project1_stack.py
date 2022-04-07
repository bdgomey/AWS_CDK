import aws_cdk as core
import aws_cdk.assertions as assertions
from project1.project1_stack import Project1Stack


def test_sqs_queue_created():
    app = core.App()
    stack = Project1Stack(app, "project1")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = Project1Stack(app, "project1")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)
