from scripts.helpful_scripts import (
    get_account,
    deploy_proxy_box,
    upgrade,
    encode_function_data,
)
from brownie import BoxV2, Contract, Box, BoxV2, TransparentUpgradeableProxy, ProxyAdmin


def test_proxy_upgrades():
    account = get_account()

    boxv1 = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        boxv1.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)

    proxy_box.store(1, {"from": account})

    box_v2 = BoxV2.deploy({"from": account})

    upgrade_transaction = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.incremint({"from": account})
    assert proxy_box.retrieve() == 2
