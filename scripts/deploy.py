from scripts.helpful_scripts import get_account, get_weth, approve_erc20, get_account_detail
from brownie import ContributorLender, network, config, interface
from web3 import Web3


def deploy_contract():
    account = get_account()
    lender_contract = ContributorLender.deploy({"from": account},
                                               publish_source=config["networks"][network.show_active()]["verify"])
    print(f"Contract deployed at {lender_contract.address}")

    # get weth to admin if needed
    weth_token = config["networks"][network.show_active()]["weth_token"]
    erc20 = interface.IERC20(weth_token)
    if network.show_active() in ["mainnet-fork"]:
        get_weth(address=weth_token, account=account)
        print(f"User WETH balance is {Web3.fromWei(erc20.balanceOf(account), 'ether')}")

    # check balances of admin and contract
    print(f"Contract WETH balance is {Web3.fromWei(erc20.balanceOf(lender_contract), 'ether')}")
    print(f"User WETH balance is {Web3.fromWei(erc20.balanceOf(account), 'ether')}")

    # set lendingPool provider
    pool_provider_address = config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    print(f"Pool provider at {pool_provider_address}")
    tx_pool = lender_contract.setPoolProvider(pool_provider_address, {"from": account})
    tx_pool.wait(1)

    # make admin deposit to pool
    CONTRIBUTION = Web3.toWei(0.01, "ether")
    tx_approve = approve_erc20(CONTRIBUTION,
                               lender_contract.address,
                               weth_token,
                               account)
    tx_deposit = lender_contract.poolDeposit(weth_token, CONTRIBUTION, {"from": account})
    tx_deposit.wait(1)
    print(f"Contract WETH balance is {Web3.fromWei(erc20.balanceOf(lender_contract), 'ether')}")
    print(f"User WETH balance is {Web3.fromWei(erc20.balanceOf(account), 'ether')}")

    # show account result
    contract_collateral, _ = get_account_detail(lender_contract.poolAddress(), lender_contract.address)
    account_collateral, _ = get_account_detail(lender_contract.poolAddress(), account)

    # refund admin user on request
    tx_refund = lender_contract.poolRefund(weth_token, CONTRIBUTION, {"from": account})
    tx_refund.wait(1)
    print(f"Contract WETH balance is {Web3.fromWei(erc20.balanceOf(lender_contract), 'ether')}")
    print(f"User WETH balance is {Web3.fromWei(erc20.balanceOf(account), 'ether')}")

    # show account result
    contract_collateral, _ = get_account_detail(lender_contract.poolAddress(), lender_contract.address)
    account_collateral, _ = get_account_detail(lender_contract.poolAddress(), account)


def main():
    deploy_contract()
