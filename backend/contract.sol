// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalImageHashStore {
    mapping(address => string) private hashes;

    event HashStored(address indexed sender, string ipfsHash);

    function storeHash(string calldata ipfsHash) external {
        hashes[msg.sender] = ipfsHash;
        emit HashStored(msg.sender, ipfsHash);
    }

    function getHash(address user) external view returns (string memory) {
        return hashes[user];
    }
}
