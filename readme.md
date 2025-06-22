# iSi test assigment

iSi test assigment

## Installation

```shell
# Clone the repository:
$ git clone https://github.com/Denis-Source/isi-assgiment.git
```

```shell
# Navigate to the project folder
$ cd isi-assgiment
```

## Quick Start

> Environment variables (in `.env`) should be provided first (see [`.env.example`](.env.example))

```shell
# Run docker compose
docker-compose -f docker-compose.yaml up --build
```

> Project should run at http://127.0.0.1:8000/
> The project will contain test data to start with

## Test Data

Test data will load automatically of first docker compose
It will create the following users with password `SeccureP4assw0rd`:
 - admin (superuser)
 - user-2
 - user-3

## Development Tools

```shell
# Install development tools (globally)
pip install -r deployment/requirements/tools.txt
```

```shell
# Apply pre-commit hooks
$ git config core.hooksPath .git-hooks
```
