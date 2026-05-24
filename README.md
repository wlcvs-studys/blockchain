# Blockchain Implementation

A simple but educational blockchain implementation in Python built following the [Learn Blockchains by Building One](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46) tutorial by [Daniel van Flymen](https://github.com/dvf).

This project demonstrates the fundamental concepts of blockchain technology, including:
- Block creation and hashing
- Proof of Work algorithm
- Chain validation
- Transaction management
- Node synchronization via HTTP API

## Project Structure

```
blockchain/
├── blockchain.py       # Core blockchain class with mining, validation, and consensus logic
├── api.py              # Flask REST API server
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Multi-Node Setup](#multi-node-setup)
- [API Endpoints](#api-endpoints)
- [How It Works](#how-it-works)

## Features

- **Block Mining**: Implements Proof of Work algorithm to validate new blocks
- **Transaction Management**: Create and manage cryptocurrency transactions
- **Chain Validation**: Verify the integrity of the entire blockchain
- **REST API**: Full HTTP API for interacting with the blockchain
- **Node Consensus**: Resolve conflicts between nodes by adopting the longest valid chain
- **Peer-to-Peer Network**: Support for multiple nodes to communicate and synchronize

## Installation

### Prerequisites

- Python 3.6 or higher
- pip or pipenv (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/wlcvs-studys/blockchain.git
cd blockchain
```

### Step 2: Install Dependencies

**Option A: Using pip with Virtual Environment (Recommended)**

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

Now install dependencies:

```bash
pip install -r requirements.txt
```

To deactivate the virtual environment later, simply run:

```bash
deactivate
```

**Option B: Using pipenv (Alternative)**

```bash
pip install pipenv
pipenv install
```

## Running the Application

### Single Node

Start a blockchain node on the default port (5000):

```bash
python api.py
```

The server will be available at `http://localhost:5000`

To run on a custom port, you can modify the port configuration in `api.py` or use environment variables with your own setup.

## Testing

### Manual Testing with cURL

#### 1. Get the current blockchain

```bash
curl http://localhost:5000/chain
```

#### 2. Create a new transaction

```bash
curl -X POST http://localhost:5000/transactions/new \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "alice",
    "recipient": "bob",
    "amount": 5
  }'
```

#### 3. Mine a new block

```bash
curl -X GET http://localhost:5000/mine
```

#### 4. Register a new node

```bash
curl -X POST http://localhost:5000/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "nodes": ["http://localhost:5001"]
  }'
```

#### 5. Resolve conflicts (consensus algorithm)

```bash
curl -X GET http://localhost:5000/nodes/resolve
```

## Multi-Node Setup

This section demonstrates how to set up a network of multiple blockchain nodes that communicate and synchronize with each other.

### Setup Overview

We'll create two nodes:
- **Node 1**: Port 5000 (primary node)
- **Node 2**: Port 5001 (secondary node)

### Step 1: Terminal Setup

Open two terminal windows in the project directory. To run the nodes on different ports, you'll need to modify `api.py` to support the desired ports or use your own port configuration approach.

**Terminal 1 (Node 1 - Port 5000):**
```bash
python api.py
```

**Terminal 2 (Node 2 - Port 5001):**

Modify `api.py` to run on port 5001 (or set up your environment accordingly), then run:
```bash
python api.py
```

You should see Flask running on both ports:
```
* Running on http://127.0.0.1:5000
```

and

```
* Running on http://127.0.0.1:5001
```

### Step 2: Register Nodes

Register Node 2 on Node 1. In a new terminal (or using another tool like Postman):

```bash
curl -X POST http://localhost:5000/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "nodes": ["http://localhost:5001"]
  }'
```

Expected response:
```json
{
  "message": "New nodes have been added",
  "total_nodes": ["127.0.0.1:5001"]
}
```

Register Node 1 on Node 2:

```bash
curl -X POST http://localhost:5001/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "nodes": ["http://localhost:5000"]
  }'
```

Expected response:
```json
{
  "message": "New nodes have been added",
  "total_nodes": ["127.0.0.1:5000"]
}
```

### Step 3: Create Transactions on Node 1

Create some transactions on Node 1:

```bash
curl -X POST http://localhost:5000/transactions/new \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "alice",
    "recipient": "bob",
    "amount": 10
  }'
```

Expected response:
```json
{
  "message": "Transaction will be added to Block 2"
}
```

Create another transaction:

```bash
curl -X POST http://localhost:5000/transactions/new \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "bob",
    "recipient": "charlie",
    "amount": 5
  }'
```

### Step 4: Mine a Block on Node 1

Mine a new block on Node 1 to include the pending transactions:

```bash
curl -X GET http://localhost:5000/mine
```

Response example:
```json
{
  "message": "New Block Forged",
  "index": 2,
  "transactions": [
    {
      "sender": "alice",
      "recipient": "bob",
      "amount": 10
    },
    {
      "sender": "bob",
      "recipient": "charlie",
      "amount": 5
    }
  ],
  "proof": 119678,
  "previous_hash": "c91e4a2f..."
}
```

### Step 5: Synchronize Nodes

Run the consensus algorithm on Node 2 to sync with Node 1:

```bash
curl -X GET http://localhost:5001/nodes/resolve
```

If Node 2's chain is shorter, it will be updated. Response if the chain was replaced:
```json
{
  "message": "Our chain was replaced",
  "new_chain": [
    {
      "index": 1,
      "timestamp": 1234567890,
      "transactions": [],
      "proof": 100,
      "previous_hash": 1
    },
    {
      "index": 2,
      "timestamp": 1234567900,
      "transactions": [
        {
          "sender": "alice",
          "recipient": "bob",
          "amount": 10
        },
        {
          "sender": "bob",
          "recipient": "charlie",
          "amount": 5
        }
      ],
      "proof": 119678,
      "previous_hash": "c91e4a2f..."
    }
  ]
}
```

### Step 6: Verify Synchronization

Check the blockchain on both nodes to confirm they are synchronized:

**Node 1:**
```bash
curl http://localhost:5000/chain | python -m json.tool
```

**Node 2:**
```bash
curl http://localhost:5001/chain | python -m json.tool
```

Both should have the same chain length and blocks.

### Step 7: Test with More Transactions

Create a transaction on Node 2:

```bash
curl -X POST http://localhost:5001/transactions/new \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "charlie",
    "recipient": "alice",
    "amount": 3
  }'
```

Mine on Node 2:

```bash
curl -X GET http://localhost:5001/mine
```

Sync Node 1 with Node 2:

```bash
curl -X GET http://localhost:5000/nodes/resolve
```

## API Endpoints

### GET `/chain`

Returns the entire blockchain.

```bash
curl http://localhost:5000/chain
```

### GET `/mine`

Creates a new block by mining. The Proof of Work algorithm runs, and all pending transactions are added to the new block.

```bash
curl http://localhost:5000/mine
```

### POST `/transactions/new`

Creates a new transaction to be added to the next mined block.

```bash
curl -X POST http://localhost:5000/transactions/new \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "alice",
    "recipient": "bob",
    "amount": 5
  }'
```

### POST `/nodes/register`

Registers a new node in the list of nodes.

```bash
curl -X POST http://localhost:5000/nodes/register \
  -H "Content-Type: application/json" \
  -d '{
    "nodes": ["http://localhost:5001", "http://localhost:5002"]
  }'
```

### GET `/nodes/resolve`

Implements the consensus algorithm. Resolves conflicts by replacing the chain with the longest valid chain across all nodes.

```bash
curl http://localhost:5000/nodes/resolve
```

## How It Works

### Code Organization

The project is organized into two main components:

#### `blockchain.py` - Core Blockchain Logic

This file contains the `Blockchain` class which implements all the core blockchain functionality:

- **`__init__()`** - Initializes the blockchain with an empty chain and creates the genesis block
- **`new_block(proof, previous_hash)`** - Creates and adds a new block to the chain
- **`new_transaction(sender, recipient, amount)`** - Adds a transaction to the pending transaction pool
- **`proof_of_work(last_proof)`** - Implements the Proof of Work algorithm to find a valid proof for a new block
- **`valid_proof(last_proof, proof)`** - Validates if a proof satisfies the Proof of Work requirements (leading 4 zeros)
- **`hash(block)`** - Creates a SHA-256 hash of a block
- **`valid_chain(chain)`** - Validates an entire blockchain by checking all block hashes and proofs
- **`register_node(address)`** - Registers a new peer node in the network
- **`resolve_conflicts()`** - Implements the Consensus Algorithm to sync with the longest valid chain in the network
- **`last_block`** - Property that returns the last block in the chain

#### `api.py` - REST API Server

This file contains the Flask application that exposes the blockchain functionality via HTTP endpoints:

- **`/mine` (GET)** - Mines a new block, adds mining reward transaction, and forges the block
- **`/transactions/new` (POST)** - Creates a new transaction to be added to the next mined block
- **`/chain` (GET)** - Returns the complete blockchain
- **`/nodes/register` (POST)** - Registers new peer nodes
- **`/nodes/resolve` (GET)** - Runs the consensus algorithm to sync with the longest valid chain

### Blockchain Concepts

#### Block Structure

Each block contains:
- `index` - The block's position in the chain (1, 2, 3, ...)
- `timestamp` - When the block was created (Unix timestamp)
- `transactions` - List of transactions in the block
- `proof` - The Proof of Work number
- `previous_hash` - The hash of the previous block

#### Proof of Work

The Proof of Work algorithm finds a number that, when hashed with the previous proof, produces a hash with a specific number of leading zeros (in this case, 4 zeros):

```
hash(previous_proof + new_proof) = "0000xxxxx..."
```

This ensures blocks are computationally expensive to create and prevents spam. The more leading zeros required, the harder it is to find a valid proof.

#### Genesis Block

The first block in the blockchain (block 0) is created with:
- `previous_hash` = 1
- `proof` = 100
- `index` = 1

#### Consensus Algorithm

When a node has multiple peer nodes registered, it can use the consensus algorithm to resolve conflicts:

1. **Request chains** from all registered peer nodes
2. **Validate** each received chain using `valid_chain()`
3. **Find** the longest valid chain
4. **Replace** the local chain if a longer valid chain was found

This ensures all nodes eventually converge on the same blockchain version (the longest one), preventing forking and maintaining network consensus.

#### Transaction Flow

1. A transaction is created via the `/transactions/new` endpoint
2. The transaction is added to `current_transactions` (pending pool)
3. When a block is mined via `/mine`:
   - A mining reward transaction is created (sender "0" = mining reward)
   - All pending transactions are included in the new block
   - The block is added to the chain
   - `current_transactions` is cleared
4. The next block will only include transactions created after the previous block was mined