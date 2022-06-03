import signal
import click
from brownie import (
    ProxyAdmin,
    StrategyExample,
    TransparentUpgradeableProxy,
    accounts,
    network,
    Contract
)
import eth_utils

def main():
    print("\nDeploying minimized Vault")

    # proxy admin account
    admin = accounts.load(
        click.prompt(
            "admin account",
            type=click.Choice(accounts.load())
        )
    )
    print(f"admin account: {admin.address}\n")

    # contract owner account
    owner = accounts.load(
        click.prompt(
            "owner account",
            type=click.Choice(accounts.load())
        )
    )
    print(f"contract owner account: {owner.address}\n")

    print(f"\nDeploying on {network.show_active()}:\n")

    # admin contract
    proxy_admin = ProxyAdmin.deploy(
        {'from': admin}
    )
    strategy = StrategyExample.deploy(
        {'from': owner}
    )
    proxy = TransparentUpgradeableProxy.deploy(
        strategy.address,
        proxy_admin.address,
        eth_utils.to_bytes(hexstr="0x"),
        {'from': admin},
    )
    # For xample, Curve 2pool
    # platformAddress is the pool's address
    # rewardTokenAddress is CRV
    # asset = [asset0, asset1], or just [asset0]
    # pToken = [pool LP token, pool LP token], or just [pool LP token]
    # Note: for Curve 2pool, platformAddress = LP token address
    platformAddress = input("Enter your platform address: ")
    vault_addr = input("Enter your vault address: ")
    rewardTokenAddress = input("Enter your reward token address: ")
    # add more asset/collateral if needed
    asset = input("Enter your asset/collateral address: ")
    pToken = input("Enter your LP token address: ")
    strategy_proxy = Contract.from_abi("Vault", proxy.address, StrategyExample.abi)
    txn = strategy.initialize(platformAddress, vault_addr, rewardTokenAddress, [asset], [pToken], {'from': owner})
    txn = strategy_proxy.initialize(platformAddress, vault_addr, rewardTokenAddress, [asset], [pToken], {'from': owner})
