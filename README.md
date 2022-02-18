<h1>ERC20 Staking</h1>
<h2>General</h2>
<p>This contract allows users to stake their ERC20 tokens to Aave and&nbsp;offer their benefits to the DAO contract.&nbsp;</p>
<h2>Lender.sol</h2>
<p>The contract is used so the user can stake/withdraw ERC20 tokens to AAVE.</p>
<p>Any amount deposited by the user is the amount he'll be able to withdraw.</p>
<p>All staking benefits are kept by the DAO to be distributed to shelters (see main project).</p>
<h2 dir="auto">Dependencies</h2>
<p dir="auto">This contract mostly depends on the <strong>IERC20.sol</strong>&nbsp;interface and <strong>Ownable.sol</strong> contract from OpenZeppelin.</p>
<p dir="auto">It also relies on&nbsp;<strong>ILendingPoolAddressesProvider.sol</strong> and<strong>&nbsp;ILendingPool.sol</strong> from Aave V2.&nbsp;</p>
<h2 dir="auto"><a id="user-content-env-file" class="anchor" href="https://github.com/DeFiGangster/Solidity-erc20-token#env-file"></a>.env file</h2>
<p dir="auto">Make sure you have a&nbsp;<strong>.env</strong>&nbsp;file in your working directory containing:</p>
<ul dir="auto">
<li>export PRIVATE_KEY="<em>YOUR_KEY</em>"</li>
<li>export WEB3_INFURA_PROJECT_ID="<em>YOUR_INFURA_ID</em>"</li>
<li>export ETHERSCAN_TOKEN="<em>YOUR_ETHERSCAN_TOKEN</em>"</li>
</ul>
<p dir="auto"><em>NB</em>: the&nbsp;ETHERSCAN_TOKEN is only needed if you want your contract to be verified upon deployment.&nbsp;</p>
<h2 dir="auto"><a id="user-content-deployment" class="anchor" href="https://github.com/DeFiGangster/Solidity-erc20-token#deployment"></a>Deployment</h2>
<p dir="auto">The contract has been deployed successfully on Kovan test network at the following address: 0x81F73B077Ed4B38239B2dbd0724F408B5E806beA</p>
<h2 dir="auto">REACT Front-end</h2>
<p dir="auto">This contract can be used by using the front-end of this repo <em>(to be added ...)</em>.&nbsp;</p>
<h2>How to use?</h2>
<p dir="auto">This contract has been created by using Python and Brownie. So you should consider using both these tools to reproduce the exact result.</p>
