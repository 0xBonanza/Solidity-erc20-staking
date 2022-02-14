from brownie import (
    network,
    config,
    accounts,
    Contract,
    interface
)
from web3 import Web3


LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "mainnet-fork", "ganache"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def approve_erc20(amount, contract_address, erc20_address, account):
    print("Approving ERC20...")
    erc20 = interface.IERC20(erc20_address)
    tx_hash = erc20.approve(contract_address, amount, {"from": account})
    tx_hash.wait(1)
    print(f"{Web3.fromWei(amount, 'ether')} ERC20 approved!")
    return True


def get_weth(address, account=None):
    """
    Mints WETH by depositing ETH.
    """
    account = (
        account if account else accounts.add(config["wallets"]["from_key"])
    )  # add your keystore ID as an argument to this call
    erc20 = interface.IWeth(address)
    tx = erc20.deposit({"from": account, "value": 1 * 1e18})
    tx.wait(1)
    print(f"{account} received 1 WETH")
    return tx


def get_account_detail(pool_address, account_address):
    (total_collateral_eth,
     total_debt_eth,
     available_borrow_eth,
     current_liquidation_threshold,
     ltv,
     health_factor) = interface.ILendingPool(pool_address).getUserAccountData(account_address)
    # Contract
    print(f"{account_address} has deposited {Web3.fromWei(total_collateral_eth, 'ether')} worth of ETH")
    return total_collateral_eth, available_borrow_eth
