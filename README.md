# Project Structure

## Directories
- [*doc*](doc): Documentations
- [*instance*](instance): Database location and other files 
- [*main*](main):  Contains all the main scripts
  - [*static*](main/static): JS, CSS and other resources
  - [*templates*](main/templates): HTML webpages
- [*tests*](tests): Contain all the tests for our project
- [*util*](util): Helpful tools
- [*playground*](playground): Standalone testing before full implementation.
- [*Solar Chain*](SolarChain/projects/SolarChain): Algokit Project containing the [Smart Contract](SolarChain/projects/SolarChain/smart_contracts/unit_transfer/unit_contract.py)

# Setup

### Pre-requisites

- [Python 3.12](https://www.python.org/downloads/) or later
- [Docker](https://www.docker.com/) (only required for LocalNet)
- Make sure all packages are installed.
  - Run `pip install -r requirements.txt` to install all required packages.
- For compiling contract after modification run: `algokit compile py <INPUT> --output-arc32 --no-output-teal`. *No need to run this if contract is not modified.*

### Initial Setup

#### 1. Clone the Repository
Start by cloning this repository to your local machine.

#### 2. Install Pre-requisites
Ensure the following pre-requisites are installed and properly configured:

- **Docker**: Required for running a local Algorand network. [Install Docker](https://www.docker.com/).
- **AlgoKit CLI**: Essential for project setup and operations. Install the latest version from [AlgoKit CLI Installation Guide](https://github.com/algorandfoundation/algokit-cli#install). Verify installation with `algokit --version`, expecting `2.0.0` or later.
- **Start LocalNet**: Use `algokit localnet start` to initiate a local Algorand network.

> For test net just run [this file](playground/asset_smart_contract_tests.py) and make sure the variable `LOCAL_NET` is set to false and accounts are properly setup in the [accounts file](playground/account_constants.py).

> Pycharm was the IDE used.

# Running the program.
Run [`main.py`](main.py) and navigate to the [website](http://127.0.0.1:5000/).

For standalone smart contract testing navigate to [Standalone file](playground/asset_smart_contract_tests.py)
> NOTE: If using localnet you will have to create new localnet accounts and asset for testing on localnet. If doing so then mention the new accounts' mnemonic in [this file](playground/account_constants.py) in the `ACCOUNTS_LOCAL` list and update the `ASSET_ID_LOCAL_NET` variable to the new asset's ID. See [this file](playground/asset_creation.py) to create a new asset for localnet.
>
> For using test net make sure that in the file the variable `LOCAL_NET` is set to false. This will make it automatically use the testnet accounts mentioned in the [accounts file](playground/account_constants.py).

# Common Issues
## Docker Errors
Logged in but got `unauthorized: incorrect username or password error.`

Right-Click on the system tray icon, does it show you logged in as username@domain.com? If so, Sign out, the issue is that you must login to Docker using your hub username, which is different than your email address, even though in some cases, both are interchangeable.
You can do this by signing out from the system tray icon, or by logging in at a command prompt, using the syntax `docker login --username your_username_here.`
If you’re not sure of your username, you can login to the [Docker Hub](https://hub.docker.com/), and your username will be displayed on the far right hand side of the menu bar, next to “Dashboard”, “Explore” and such.

# Tools

This project makes use of Algorand Python to build Algorand smart contracts.

The following tools are in use:

- [AlgoKit](https://github.com/algorandfoundation/algokit-cli) - One-stop shop tool for developers building on the Algorand network; [docs](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/algokit.md), [intro tutorial](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/tutorials/intro.md)
- [Algorand Python](https://github.com/algorandfoundation/puya) - A semantically and syntactically compatible, typed Python language that works with standard Python tooling and allows you to express smart contracts (apps) and smart signatures (logic signatures) for deployment on the Algorand Virtual Machine (AVM); [docs](https://github.com/algorandfoundation/puya), [examples](https://github.com/algorandfoundation/puya/tree/main/examples)
- [AlgoKit Utils](https://github.com/algorandfoundation/algokit-utils-py) - A set of core Algorand utilities that make it easier to build solutions on Algorand.
- [pytest](https://docs.pytest.org/): Automated testing.
- [Docker](https://www.docker.com/): For localnet testing
- [Flask](https://flask.palletsprojects.com/en/stable/): For backend
