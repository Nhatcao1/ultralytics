#!/bin/bash

# Set certificate details
COUNTRY="US"
STATE="State"
LOCALITY="City"
ORGANIZATION="MyOrg"
ORG_UNIT="IT"
COMMON_NAME_CLIENT="client"

# Paths for client keys and CSR
CERT_DIR="./tls_certs"
CLIENT_KEY="$CERT_DIR/client.key"
CLIENT_CSR="$CERT_DIR/client.csr"

# Create directory for certificates
mkdir -p $CERT_DIR

# Step 2: Generate Client Private Key
echo "Generating Client Key..."
openssl genpkey -algorithm RSA -out $CLIENT_KEY

# Step 3: Generate the Client CSR
echo "Generating Client CSR..."
openssl req -new -key $CLIENT_KEY -out $CLIENT_CSR -subj "/C=$COUNTRY/ST=$STATE/L=$LOCALITY/O=$ORGANIZATION/OU=$ORG_UNIT/CN=$COMMON_NAME_CLIENT"

# Display the result
echo "====================================="
echo "Client CSR setup is complete. Files created:"
echo "Client Key: $CLIENT_KEY"
echo "Client CSR: $CLIENT_CSR"
echo "====================================="

#scp ./tls_certs/client.csr master:/root/ultralytics/ultralytics/federated/tls_certs/

