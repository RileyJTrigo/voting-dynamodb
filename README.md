# Polls

Flask serves the HTTP API and the browser UI. Polls are stored in DynamoDB. On your laptop the database is DynamoDB Local. On EC2 the database is Amazon DynamoDB. See the **specs** repository for the product specifications (use cases, API, data model, and related materials).


## Documentation

| Doc | Contents |
|-----|----------|
| [Development setup](docs/development.md) | Virtualenv, install, unit tests, lint, local AWS profile, DynamoDB Local, run the app, acceptance tests |
| [Deploy manually](docs/deploy-manual.md) | Polls table, security group, instance profile, user data, systemd, debugging |
| [Deploy with CloudFormation](docs/deploy-cloudformation.md) | CLI: one stack for the table and the instance |
| [Design](docs/design.md) | Layers, data types, UI notes, package layout |


## Quick start

- Create a virtual environment and install dependencies
- Add the `local` profile to `~/.aws/credentials` and `~/.aws/config`
- Start DynamoDB Local and create the `Polls` table
- Run `python -m voting.app` and open [http://127.0.0.1:5000/](http://127.0.0.1:5000/)


See [Development setup](docs/development.md) for full steps.
