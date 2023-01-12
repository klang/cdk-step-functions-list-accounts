import aws_cdk as core
import aws_cdk.assertions as assertions

from step_function_account_list.step_function_account_list_stack import StepFunctionAccountListStack

# example tests. To run these tests, uncomment this file along with the example
# resource in step_function_account_list/step_function_account_list_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = StepFunctionAccountListStack(app, "step-function-account-list")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
