"""Delete the Polls table in DynamoDB Local.

Prompts for confirmation unless -y is passed.
Selects the local AWS profile. Run this on your laptop, with DynamoDB Local up.
"""

import argparse
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


def _confirm_delete(table_name: str) -> bool:
    answer = input(
        f"Delete table {table_name!r}? This cannot be undone. [y/N] "
    ).strip().lower()
    return answer in ("y", "yes")


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete the Polls DynamoDB table.")
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Delete without prompting.",
    )
    args = parser.parse_args()

    dynamodb = boto3.resource("dynamodb", endpoint_url=LOCAL_DYNAMODB_URL)

    if not _table_exists(dynamodb, POLLS_TABLE_NAME):
        print(f"Table {POLLS_TABLE_NAME!r} does not exist.", file=sys.stderr)
        sys.exit(1)

    if not args.yes and not _confirm_delete(POLLS_TABLE_NAME):
        print("Delete cancelled.")
        sys.exit(1)

    table = dynamodb.Table(POLLS_TABLE_NAME)
    table.delete()
    table.wait_until_not_exists()
    print(f"Deleted table {POLLS_TABLE_NAME!r}.")


if __name__ == "__main__":
    boto3.setup_default_session(profile_name="local")
    main()
