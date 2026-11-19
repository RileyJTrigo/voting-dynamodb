"""Create the Polls table in DynamoDB Local.

Fails if the table already exists. To reset, run delete_table.py first.
Selects the local AWS profile. Run this on your laptop, with DynamoDB Local up.
"""

import sys

import boto3
from botocore.exceptions import ClientError

from voting.db import LOCAL_DYNAMODB_URL, POLLS_TABLE_NAME


def _table_exists(dynamodb, table_name: str) -> bool:
    try:
        dynamodb.meta.client.describe_table(TableName=table_name)
        return True
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ResourceNotFoundException":
            return False
        raise


def main() -> None:
    dynamodb = boto3.resource("dynamodb", endpoint_url=LOCAL_DYNAMODB_URL)

    if _table_exists(dynamodb, POLLS_TABLE_NAME):
        print(
            f"Table {POLLS_TABLE_NAME!r} already exists. "
            "Delete it first if you want to recreate: "
            "python scripts/delete_table.py",
            file=sys.stderr,
        )
        sys.exit(1)

    table = dynamodb.create_table(
        TableName=POLLS_TABLE_NAME,
        KeySchema=[{"AttributeName": "pollId", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "pollId", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()


if __name__ == "__main__":
    boto3.setup_default_session(profile_name="local")
    main()
