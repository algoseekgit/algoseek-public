# Edgar Filings Examples

This is a collection of examples of how to use the Algoseek's Edgar Filing Dataset.

## Table of Contents

- [Edgar Filings Examples](#edgar-filings-examples)
  - [Table of Contents](#table-of-contents)
  - [Available notebooks](#available-notebooks)
    - [Financial Filings](#financial-filings)
    - [Shares Outstanding](#shares-outstanding)
  - [Prerequisites](#prerequisites)
    - [Database credentials](#database-credentials)
    - [Software Requirements](#software-requirements)
  - [Usage](#usage)
  - [alternative usage](#alternative-usage)

## Available notebooks

The following notebooks are available in this repository:

### Financial Filings

This notebook shows how to get the financial filings of a company as reported in the 10-K and 10-Q filings.

### Shares Outstanding

This notebook shows how to get the shares outstanding of a company as reported in the 10-K and 10-Q filings.

## Prerequisites

### Database credentials

For the examples to work, you will need to have credentials to access our database service, if you don't have them please feel free to contact your account executive and we'l provide it to you.

For easy of use there is a `.env_example` file in the root of the project that you can use to set the environment variables, please rename it to `.env` and fill in the values.

- `CLICKHOUSE_HOST`: The host of the Clickhouse server
- `CLICKHOUSE_PORT`: The port of the Clickhouse server
- `CLICKHOUSE_USER`: The user to authenticate
- `CLICKHOUSE_PASSWORD`: The password to authenticate
- `CLICKHOUSE_DATABASE`: The database to use

### Software Requirements

The provided examples are written in Python and use Jupyter notebooks for execution. A `Makefile` is included to automate the installation of dependencies and run the examples. This will work seamlessly on a Linux or MacOS environment. If you are using a different operating system, you can manually run the commands specified in the `Makefile`.

To run the examples, ensure that you have Python 3.10 installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

Additionally, the `Make` utility is required to execute the commands in the `Makefile`. It is typically available by default on Linux systems. If you don't have it, you can install it on a Linux system using `sudo apt install make`. For MacOS, you can install the Xcode command line tools with `xcode-select --install`.

## Usage

In order to run the examples, you will need to install the dependencies, you can do so by running the following command:

```bash
make install
```

After that you can run the examples by running the following command:

```bash
make run
```

This will open a Jupyter notebook in your browser, you can then navigate to the `edgar-filings-examples/notebooks` folder and open the examples.

## alternative usage

If you don't want to install a Jupyter notebook, you can run the examples directly using the database manager of your choice, for example you can use `dbeaver` to connect to the database and run the queries in the examples.

You can find the queries in the `edgar-filings-examples/sql` folder, you can open them with a text editor and copy the queries to the database manager.
