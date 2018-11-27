'''
This is an example how to interact with the following contract:

pragma solidity ^0.4.2;

contract Election {
    string public candidateName;

    function Election () public {
        candidateName = "Candidate 1";
    }

    function setCandidate (string _name) public {
        candidateName = _name;
    }
}


That should be deployed in some Web3 provider
'''
import pudb; pu.db
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

# Connect to local Ganache
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
assert w3.isConnected()

# Contract ABI
contract_abi = '''
[
	{
		"constant": true,
		"inputs": [],
		"name": "candidateName",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_name",
				"type": "string"
			}
		],
		"name": "setCandidate",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	}
]
'''

# Contract Address
contract_address = w3.toChecksumAddress('0xf400aa6c9f9658cebdb8d370f9782e23412f9e34')

# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]

# Create the contract instance with the contract address
election = w3.eth.contract(address=contract_address, abi=contract_abi)

# Display the default candidate from the contract
print('Default contract candidate: {}'.format(
    election.functions.candidateName().call()
))

print('Setting the candidate to Menem...')
tx_hash = election.functions.setCandidate('Menem').transact()

# Wait for transaction to be mined...
w3.eth.waitForTransactionReceipt(tx_hash)

# Display the new setCandidateing value
print('Updated contract to: {}'.format(
    election.functions.candidateName().call()
))

# When issuing a lot of reads, try this more concise reader:
reader = ConciseContract(election)
assert reader.candidateName() == "Menem"
