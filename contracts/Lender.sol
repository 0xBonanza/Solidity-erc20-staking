// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import '@aave/contracts/interfaces/ILendingPoolAddressesProvider.sol';
import '@aave/contracts/interfaces/ILendingPool.sol';


contract ContributorLender is Ownable {

    address public admin;
    address[] public contributors;
    address[] public poolTokens;
    mapping(address => bool) public tokenIsAccepted;
    mapping(address => mapping(address => uint256)) public contributions;
    address public poolAddress;
    ILendingPool public lendingPool;
    ILendingPoolAddressesProvider public poolProvider;

    constructor() public {
        admin = msg.sender;
    }

    // set pool provider
    function setPoolProvider(address _poolProvider) public onlyOwner {
        poolProvider = ILendingPoolAddressesProvider(_poolProvider);
    }

    // get lending pool
    function getLendingPool() public returns (ILendingPool) {
        poolAddress = poolProvider.getLendingPool();
        return ILendingPool(poolAddress);
    }

    // add a token that can be staked
    function setPoolTokens(address _token) public onlyOwner {
        tokenIsAccepted[_token] = true;
        poolTokens.push(_token);
    }

    // UNUSED: user can deposits funds
    function contribute(address _token, uint256 _amount) public {
        require(_amount > 0, "You need to spend something.");
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        contributors.push(msg.sender);
        contributions[_token][msg.sender] += _amount;
    }

    // let user deposit fund to Aave but aTokens goes to Treasury until withdrawal
    function poolDeposit(address _token, uint256 _amount) public {
        require(_amount > 0, "You need to spend something.");
        // make sure that the token is activated by the admin
        if (tokenIsAccepted[_token]) {
            IERC20(_token).transferFrom(msg.sender, address(this), _amount);
            contributors.push(msg.sender);
            contributions[_token][msg.sender] += _amount;
            lendingPool = getLendingPool();
            IERC20(_token).approve(address(lendingPool), _amount);
            lendingPool.deposit(_token, _amount, address(this), 0);
        }
    }

    // refund user MAX based on what he has contributed
    function poolRefund(address _token, uint256 _amount) public {
        require(_amount > 0, "You need to withdraw something.");
        require(contributions[_token][msg.sender] >= _amount, "You cannot withdraw more than what you contributed!");
        lendingPool.withdraw(_token, _amount, msg.sender);
        contributions[_token][msg.sender] -= _amount;
    }

    // DAO distributes to someone
    function distribute(address _token, address _beneficiary, uint256 _amount) public onlyOwner {
        IERC20(_token).transfer(_beneficiary, _amount);
    }

}
