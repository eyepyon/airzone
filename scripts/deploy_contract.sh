#!/bin/bash

# Airzone NFT Contract Deployment Script
# This script deploys the Sui Move smart contract to the specified network
#
# Requirements: 3.2 - NFT minting via Move smart contract

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Airzone NFT Contract Deployment"
echo "=========================================="
echo ""

# Check if Sui CLI is installed
if ! command -v sui &> /dev/null; then
    echo -e "${RED}Error: Sui CLI is not installed${NC}"
    echo "Please install Sui CLI first:"
    echo "  cargo install --locked --git https://github.com/MystenLabs/sui.git --branch testnet sui"
    exit 1
fi

echo -e "${GREEN}✓ Sui CLI found${NC}"
echo ""

# Get network from argument or default to testnet
NETWORK=${1:-testnet}

echo "Target Network: $NETWORK"
echo ""

# Validate network
if [ "$NETWORK" != "testnet" ] && [ "$NETWORK" != "devnet" ] && [ "$NETWORK" != "mainnet" ]; then
    echo -e "${RED}Error: Invalid network. Must be 'testnet', 'devnet', or 'mainnet'${NC}"
    exit 1
fi

# Check if wallet is configured
if ! sui client active-address &> /dev/null; then
    echo -e "${RED}Error: No active Sui wallet found${NC}"
    echo "Please configure your Sui wallet first:"
    echo "  sui client"
    exit 1
fi

ACTIVE_ADDRESS=$(sui client active-address)
echo -e "${GREEN}✓ Active wallet: $ACTIVE_ADDRESS${NC}"
echo ""

# Check wallet balance
echo "Checking wallet balance..."
BALANCE=$(sui client gas --json | jq -r '[.[] | .balance] | add')

if [ -z "$BALANCE" ] || [ "$BALANCE" == "null" ]; then
    echo -e "${RED}Error: Could not retrieve wallet balance${NC}"
    exit 1
fi

echo "Wallet balance: $BALANCE MIST"

# Convert MIST to SUI (1 SUI = 1,000,000,000 MIST)
SUI_BALANCE=$(echo "scale=2; $BALANCE / 1000000000" | bc)
echo "               $SUI_BALANCE SUI"
echo ""

# Check if balance is sufficient (need at least 0.1 SUI for deployment)
MIN_BALANCE=100000000  # 0.1 SUI in MIST
if [ "$BALANCE" -lt "$MIN_BALANCE" ]; then
    echo -e "${YELLOW}Warning: Low balance. You may need more SUI for deployment.${NC}"
    echo "Minimum recommended: 0.1 SUI"
    echo ""
    
    if [ "$NETWORK" == "testnet" ] || [ "$NETWORK" == "devnet" ]; then
        echo "You can get test tokens from the faucet:"
        echo "  curl --location --request POST 'https://faucet.$NETWORK.sui.io/gas' \\"
        echo "    --header 'Content-Type: application/json' \\"
        echo "    --data-raw '{\"FixedAmountRequest\":{\"recipient\":\"$ACTIVE_ADDRESS\"}}'"
        echo ""
    fi
    
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Navigate to contracts directory
cd "$(dirname "$0")/../contracts"

echo "Building contract..."
echo ""

# Build the contract
if ! sui move build; then
    echo -e "${RED}Error: Contract build failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Contract built successfully${NC}"
echo ""

# Deploy the contract
echo "Deploying contract to $NETWORK..."
echo ""

# Set gas budget (100 SUI = 100,000,000,000 MIST)
GAS_BUDGET=100000000  # 0.1 SUI

echo "Gas budget: $GAS_BUDGET MIST (0.1 SUI)"
echo ""

# Deploy and capture output
DEPLOY_OUTPUT=$(sui client publish --gas-budget $GAS_BUDGET --json 2>&1)

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Deployment failed${NC}"
    echo "$DEPLOY_OUTPUT"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Contract deployed successfully!${NC}"
echo ""

# Parse deployment output
PACKAGE_ID=$(echo "$DEPLOY_OUTPUT" | jq -r '.objectChanges[] | select(.type == "published") | .packageId')
TRANSACTION_DIGEST=$(echo "$DEPLOY_OUTPUT" | jq -r '.digest')

if [ -z "$PACKAGE_ID" ] || [ "$PACKAGE_ID" == "null" ]; then
    echo -e "${YELLOW}Warning: Could not parse package ID from deployment output${NC}"
    echo "Please extract it manually from the output above"
    echo ""
    echo "$DEPLOY_OUTPUT" | jq '.'
    exit 1
fi

echo "=========================================="
echo "Deployment Summary"
echo "=========================================="
echo ""
echo "Network:            $NETWORK"
echo "Package ID:         $PACKAGE_ID"
echo "Transaction Digest: $TRANSACTION_DIGEST"
echo "Deployer Address:   $ACTIVE_ADDRESS"
echo ""

# Update .env file
ENV_FILE="../backend/.env"

if [ -f "$ENV_FILE" ]; then
    echo "Updating $ENV_FILE..."
    
    # Check if SUI_PACKAGE_ID exists in .env
    if grep -q "^SUI_PACKAGE_ID=" "$ENV_FILE"; then
        # Update existing value
        sed -i.bak "s/^SUI_PACKAGE_ID=.*/SUI_PACKAGE_ID=$PACKAGE_ID/" "$ENV_FILE"
        echo -e "${GREEN}✓ Updated SUI_PACKAGE_ID in $ENV_FILE${NC}"
    else
        # Append new value
        echo "" >> "$ENV_FILE"
        echo "# Sui Smart Contract" >> "$ENV_FILE"
        echo "SUI_PACKAGE_ID=$PACKAGE_ID" >> "$ENV_FILE"
        echo -e "${GREEN}✓ Added SUI_PACKAGE_ID to $ENV_FILE${NC}"
    fi
    
    # Update network if needed
    if grep -q "^SUI_NETWORK=" "$ENV_FILE"; then
        sed -i.bak "s/^SUI_NETWORK=.*/SUI_NETWORK=$NETWORK/" "$ENV_FILE"
    fi
    
    echo ""
else
    echo -e "${YELLOW}Warning: $ENV_FILE not found${NC}"
    echo "Please manually add the following to your .env file:"
    echo ""
    echo "SUI_PACKAGE_ID=$PACKAGE_ID"
    echo "SUI_NETWORK=$NETWORK"
    echo ""
fi

echo "=========================================="
echo "Next Steps"
echo "=========================================="
echo ""
echo "1. Verify the package ID is set in backend/.env:"
echo "   SUI_PACKAGE_ID=$PACKAGE_ID"
echo ""
echo "2. Ensure sponsor wallet is configured:"
echo "   SUI_SPONSOR_PRIVATE_KEY=<your-sponsor-private-key>"
echo ""
echo "3. Test NFT minting:"
echo "   python backend/verify_sui_client.py"
echo ""
echo "4. View contract on Sui Explorer:"
if [ "$NETWORK" == "mainnet" ]; then
    echo "   https://suiexplorer.com/object/$PACKAGE_ID"
else
    echo "   https://suiexplorer.com/object/$PACKAGE_ID?network=$NETWORK"
fi
echo ""

echo -e "${GREEN}Deployment complete!${NC}"
