from scripts.helpful_scripts import encode_function_data, get_account, upgrade
from brownie import (
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)


def main():
    account = get_account()
    print(f"Deploying to: {network.show_active()}")
    box = Box.deploy({"from": account})
    print(box.retrieve())

    # sets proxy admin
    proxy_admin = ProxyAdmin.deploy({"from": account})

    # create initializer, right now its empty but needed for TUP parameter
    initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()

    # create the proxy
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )

    print(f"Proxy deployed to {proxy} you can now upgrade to v2")

    # assign the proxy to the box contract
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    print(proxy_box.retrieve())

    # upgrade
    box_v2 = BoxV2.deploy({"from": account})

    upgrade_transaction = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )

    print("Proxy has been upgraded!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.incremint({"from": account})
    print(proxy_box.retrieve())
