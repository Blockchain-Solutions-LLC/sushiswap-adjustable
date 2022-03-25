pragma solidity =0.6.12;

import './uniswapv2/UniswapV2Pair.sol';
import './uniswapv2/UniswapV2Factory.sol';

contract Temp {
     bytes32 public constant INIT_CODE_PAIR_HASH = keccak256(abi.encodePacked(type(UniswapV2Pair).creationCode));
     bytes32 public constant INIT_CODE_PAIR_HASH2 = keccak256(abi.encodePacked(type(UniswapV2Factory).creationCode));
}
