import boto3
import sys

REGION = "ap-south-1"
STACK_NAME = "shalaconnect"
TEMPLATE_FILE = "aws/cloudformation.yml"

PARAMS = [
    {"ParameterKey": "GitHubOwner",         "ParameterValue": "YashSabale01"},
    {"ParameterKey": "GitHubRepo",          "ParameterValue": "ShalaConnect"},
    {"ParameterKey": "GitHubBranch",        "ParameterValue": "main"},
    {"ParameterKey": "GitHubConnectionArn", "ParameterValue": "arn:aws:codeconnections:ap-south-1:351245513808:connection/6e8095b3-a99f-4177-9d48-b2733d499293"},
    {"ParameterKey": "DBPassword",          "ParameterValue": "MyRdsPass123!"},
    {"ParameterKey": "JwtSecret",           "ParameterValue": "shalaconnect_prod_jwt_secret_32_chars_minimum!!"},
    {"ParameterKey": "AdminEmail",          "ParameterValue": "admin@shalaconnect.in"},
    {"ParameterKey": "AdminPassword",       "ParameterValue": "Admin@123"},
]

def main():
    with open(TEMPLATE_FILE, encoding="utf-8") as f:
        template_body = f.read()

    cfn = boto3.client("cloudformation", region_name=REGION)

    # Check stack status
    stack_status = None
    try:
        resp = cfn.describe_stacks(StackName=STACK_NAME)
        stack_status = resp["Stacks"][0]["StackStatus"]
        print(f"Stack exists with status: {stack_status}")
    except cfn.exceptions.ClientError:
        print(f"Stack does not exist — creating fresh...")

    # If in a bad/transitional state, wait for delete then recreate
    if stack_status in ("ROLLBACK_COMPLETE", "ROLLBACK_IN_PROGRESS", "DELETE_IN_PROGRESS"):
        if stack_status != "DELETE_IN_PROGRESS":
            print("Deleting failed stack before recreating...")
            cfn.delete_stack(StackName=STACK_NAME)
        else:
            print("Stack is already deleting, waiting...")
        waiter = cfn.get_waiter("stack_delete_complete")
        waiter.wait(StackName=STACK_NAME, WaiterConfig={"Delay": 10, "MaxAttempts": 60})
        print("Deleted. Creating fresh stack...")
        stack_status = None

    try:
        if stack_status and stack_status not in ["ROLLBACK_COMPLETE"]:
            response = cfn.update_stack(
                StackName=STACK_NAME,
                TemplateBody=template_body,
                Parameters=PARAMS,
                Capabilities=["CAPABILITY_NAMED_IAM"],
            )
            waiter = cfn.get_waiter("stack_update_complete")
            print(f"Updating stack: {response['StackId']}")
        else:
            response = cfn.create_stack(
                StackName=STACK_NAME,
                TemplateBody=template_body,
                Parameters=PARAMS,
                Capabilities=["CAPABILITY_NAMED_IAM"],
                OnFailure="ROLLBACK",
            )
            waiter = cfn.get_waiter("stack_create_complete")
            print(f"Creating stack: {response['StackId']}")

        print("Waiting... (RDS takes ~10-15 min)")
        waiter.wait(StackName=STACK_NAME, WaiterConfig={"Delay": 30, "MaxAttempts": 60})
        print("SUCCESS!")

    except cfn.exceptions.ClientError as e:
        if "No updates are to be performed" in str(e):
            print("Already up to date.")
        else:
            print(f"ERROR: {e}")
            events = cfn.describe_stack_events(StackName=STACK_NAME)["StackEvents"]
            print("\nFailed events:")
            for ev in events[:15]:
                status = ev.get("ResourceStatus", "")
                if "FAILED" in status or "ROLLBACK" in status:
                    print(f"  {ev.get('LogicalResourceId')}: {ev.get('ResourceStatusReason')}")
            sys.exit(1)

    # Print outputs
    stack = cfn.describe_stacks(StackName=STACK_NAME)["Stacks"][0]
    print("\nStack Outputs:")
    for o in stack.get("Outputs", []):
        print(f"  {o['OutputKey']}: {o['OutputValue']}")

if __name__ == "__main__":
    main()
