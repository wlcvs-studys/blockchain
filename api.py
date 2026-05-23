from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import Blockchain

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods = ['GET'])
def mine():
  return "We'll mine a new Block"

@app.route('/transaction/new', methods = ['POST'])
def new_transaction():
  values = request.get_json()

  # Check that the required fields are in the POST'ed data 
  required = ['sender', 'recipient', 'amount']
  if not all(k in values for k in required):
    return 'Missing values', 400 
  
  # Create a new Transaction
  index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

  response = {'message': f'Transaction will be added to Block {index}'}

  return jsonify(response), 201

@app.route('/chain', methods = ['GET'])
def full_chain():
  response = {
    'chain': blockchain.chain,
    'length': len(blockchain.chain),
  }
  return jsonify(response), 200

if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 5000)