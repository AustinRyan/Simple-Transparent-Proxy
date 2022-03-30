from scripts.helpful_scripts import encode_function_data, get_account, deploy_proxy_box
from brownie import (
    Box,
    Contract,
    TransparentUpgradeableProxy,
    ProxyAdmin,
)


def test_proxy_delegates_calls():
    account = get_account()
    proxy_box = deploy_proxy_box(account)
    assert proxy_box.retrieve() == 0
    proxy_box.store(1, {"from": account})
    assert proxy_box.retrieve() == 1
