from aws_cdk import (
    # Duration,
    Stack,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
    # aws_sqs as sqs,
)
from constructs import Construct

class StepFunctionAccountListStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        list_accounts = sfn_tasks.CallAwsService(
            self,
            id="List Accounts - Max Results 3",
            comment="List Accounts limited to Max Results of 3, meaning NextToken will be returned",
            service="organizations",
            action="listAccounts",
            result_path="$.ListAccountResult",
            iam_resources=["*"],
        )
                
        list_more_accounts = sfn_tasks.CallAwsService(
            self,
            id="List Accounts - Using Next Token",
            comment="List Accounts limited to Max Results of 3, meaning NextToken will be returned",
            service="organizations",
            action="listAccounts",
            parameters={
                "NextToken": sfn.JsonPath.string_at(
                    "$.ListAccountResult.NextToken"
                )
            },
            result_path="$.ListAccountResult",
            iam_resources=["*"],
        )

        definition = list_accounts.next(
            sfn.Choice(self, "Is Next Token present?")
            .when(
                sfn.Condition.is_present("$.ListAccountResult.NextToken"),
                list_more_accounts
#                list_more_accounts.next("List Accounts - Using Next Token")    
            ).otherwise(sfn.Succeed(self, "Done"))
        )
        
        state_machine = sfn.StateMachine(
            self,
            id="MyNewMachine",
            state_machine_type=sfn.StateMachineType.STANDARD,
            definition=definition,
        )