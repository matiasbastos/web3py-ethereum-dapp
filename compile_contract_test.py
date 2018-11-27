import pudb; pu.db
from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract

# Solidity source code
contract_source_code = '''
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
'''

compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:Election']


# Connect to local Ganache
w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
assert w3.isConnected()

# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]

# Instantiate and deploy contract
Election = w3.eth.contract(abi=contract_interface['abi'],
			   bytecode=contract_interface['bin'])

# Submit the transaction that deploys the contract
tx_hash = Election.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Create the contract instance with the newly-deployed address
election = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)

# Display the default candidate from the contract
print('Default contract candidate: {}'.format(
    election.functions.setCandidate().call()
))

print('Setting the candidate to Menem...')
tx_hash = election.functions.setCandidate('Menem').transact()

# Wait for transaction to be mined...
w3.eth.waitForTransactionReceipt(tx_hash)

# Display the new setCandidateing value
print('Updated contract setCandidateing: {}'.format(
    election.functions.setCandidate().call()
))

# When issuing a lot of reads, try this more concise reader:
reader = ConciseContract(election)
assert reader.setCandidate() == "Menem"
