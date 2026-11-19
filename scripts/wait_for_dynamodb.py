"""Wait until DynamoDB Local answers ListTables.

Selects the local AWS profile. Run this on your laptop, with DynamoDB Local up.
"""

import argparse
import sys
import time

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from voting.db import LOCAL_DYNAMODB_URL


def wait_for_dynamodb(timeout_seconds: int) -> None:
    client = boto3.client(
        "dynamodb",
        endpoint_url=LOCAL_DYNAMODB_URL,
        config=Config(
            connect_timeout=1,
            read_timeout=1,
            retries={"max_attempts": 1},
        ),
    )
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            client.list_tables()
            return
        except (BotoCoreError, ClientError, OSError):
            time.sleep(1)
    raise TimeoutError(
        f"DynamoDB Local did not become ready within {timeout_seconds}s "
        f"(endpoint {LOCAL_DYNAMODB_URL!r})."
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Wait until DynamoDB Local responds to ListTables."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Seconds to wait before failing (default: 60).",
    )
    args = parser.parse_args()

    try:
        wait_for_dynamodb(args.timeout)
    except TimeoutError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

    print("DynamoDB is ready.")


if __name__ == "__main__":
    boto3.setup_default_session(profile_name="local")
    main()
