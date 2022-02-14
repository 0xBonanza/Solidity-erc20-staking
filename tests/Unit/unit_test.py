
from scripts.helpful_scripts import get_account, get_weth, approve_erc20, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import ContributorLender, network, config, interface, exceptions
from web3 import Web3
import pytest


def test_can_deposit():
    # only or mainnet-fork
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Admin account
    account = get_account()
    lender_contract = ContributorLender.deploy({"from": account})

    # set lendingPool provider
    pool_provider_address = config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    tx_pool = lender_contract.setPoolProvider(pool_provider_address, {"from": account})
    tx_pool.wait(1)

    # get contributor 1 ready
    weth_token = config["networks"][network.show_active()]["weth_token"]
    contributor_1 = get_account(index=1)
    get_weth(address=weth_token, account=contributor_1)
    CONTRIBUTION = Web3.toWei(0.1, "ether")
    tx_approve = approve_erc20(CONTRIBUTION,
                               lender_contract.address,
                               weth_token,
                               contributor_1)
    tx_contrib = lender_contract.poolDeposit(weth_token,
                                             CONTRIBUTION,
                                             {"from": contributor_1})
    tx_contrib.wait(1)
    aWeth_token = config["networks"][network.show_active()]["aWeth_token"]
    eip20 = interface.EIP20Interface(aWeth_token)
    assert eip20.balanceOf(lender_contract.address) >= Web3.toWei(0.1, "ether")



#
# def test_can_create():
#     account = get_account()
#     lender_contract = ContributorLender.deploy({"from": account})
#     weth_token = config["networks"][network.show_active()]["weth_token"]
#     contributor_1 = get_account(index=1)
#     get_weth(address=weth_token, account=contributor_1)
#     tx_approve = approve_erc20(Web3.toWei(0.1, "ether"),
#                                lender_contract.address,
#                                weth_token,
#                                contributor_1)
#     CONTRIBUTED_AMOUNT = Web3.toWei(0.1, "ether")
#     tx_contrib = lender_contract.contribute(weth_token,
#                                             CONTRIBUTED_AMOUNT,
#                                             {"from": contributor_1})
#     tx_contrib.wait(1)
#     erc20 = interface.IERC20(weth_token)
#     assert erc20.balanceOf(lender_contract) == Web3.toWei(0.1, "ether")
#
#
# def test_can_contribute_and_distribute():
#     account = get_account()
#     lender_contract = ContributorLender.deploy({"from": account})
#     weth_token = config["networks"][network.show_active()]["weth_token"]
#     contributor_1 = get_account(index=1)
#     get_weth(address=weth_token, account=contributor_1)
#     tx_approve = approve_erc20(Web3.toWei(0.1, "ether"),
#                                lender_contract.address,
#                                weth_token,
#                                contributor_1)
#     tx_contrib = lender_contract.contribute(weth_token,
#                                             Web3.toWei(0.1, "ether"),
#                                             {"from": contributor_1})
#     tx_contrib.wait(1)
#     erc20 = interface.IERC20(weth_token)
#     contributor_2 = get_account(index=2)
#
#     # check that amount can be distributed to someone BY ADMIN
#     DISTRIBUTED_AMOUNT = Web3.toWei(0.05, "ether")
#     tx_distribute = lender_contract.distribute(weth_token,
#                                                contributor_2,
#                                                DISTRIBUTED_AMOUNT,
#                                                {"from": account})
#     tx_distribute.wait(1)
#     assert erc20.balanceOf(lender_contract) == Web3.toWei(0.05, "ether")
#     assert erc20.balanceOf(contributor_2) == DISTRIBUTED_AMOUNT
#
#     # check that amount cannot be distributed to someone BY ANYONE BUT ADMIN
#     DISTRIBUTED_AMOUNT = Web3.toWei(0.05, "ether")
#     with pytest.raises(exceptions.VirtualMachineError):
#         lender_contract.distribute(weth_token,
#                                    contributor_2,
#                                    DISTRIBUTED_AMOUNT,
#                                    {"from": contributor_2})
#
#
# def test_can_contribute_and_withdraw():
#     account = get_account()
#     lender_contract = ContributorLender.deploy({"from": account})
#     weth_token = config["networks"][network.show_active()]["weth_token"]
#     contributor_1 = get_account(index=1)
#     get_weth(address=weth_token, account=contributor_1)
#     tx_approve = approve_erc20(Web3.toWei(0.1, "ether"),
#                                lender_contract.address,
#                                weth_token,
#                                contributor_1)
#     CONTRIBUTED_AMOUNT = Web3.toWei(0.1, "ether")
#     tx_contrib = lender_contract.contribute(weth_token,
#                                             CONTRIBUTED_AMOUNT,
#                                             {"from": contributor_1})
#
#     tx_contrib.wait(1)
#     erc20 = interface.IERC20(weth_token)
#     current_user_balance = erc20.balanceOf(contributor_1)
#     WITHDRAWN_AMOUNT = Web3.toWei(0.05, "ether")
#     tx_distribute = lender_contract.withdraw(weth_token,
#                                              WITHDRAWN_AMOUNT,
#                                              {"from": contributor_1})
#     tx_distribute.wait(1)
#     assert erc20.balanceOf(lender_contract) == CONTRIBUTED_AMOUNT - WITHDRAWN_AMOUNT
#     assert erc20.balanceOf(contributor_1) == current_user_balance + WITHDRAWN_AMOUNT
