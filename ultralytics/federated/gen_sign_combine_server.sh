#!/bin/bash

# Set certificate details
COUNTRY="US"
STATE="State"
LOCALITY="City"
ORGANIZATION="MyOrg"
ORG_UNIT="IT"
COMMON_NAME_SERVER="server"
DAYS_VALID=365

# Paths for certificates and keys
CERT_DIR="./tls_certs"
CA_KEY="$CERT_DIR/ca.key"
CA_CERT="$CERT_DIR/ca.crt"
SERVER_KEY="$CERT_DIR/server.key"
SERVER_CSR="$CERT_DIR/server.csr"
SERVER_CERT="$CERT_DIR/server.crt"
SERVER_PEM="$CERT_DIR/server.pem"
CONFIG_FILE="./openssl_server.cnf"  # Ensure this path is correct

# Create directory for certificates and keys
mkdir -p $CERT_DIR

# Step 1: Generate the Server Private Key
echo "Generating Server Key..."
openssl genpkey -algorithm RSA -out $SERVER_KEY

# Step 2: Generate the Server CSR with SAN
echo "Generating Server CSR with SAN..."
openssl req -new -key $SERVER_KEY -out $SERVER_CSR -config $CONFIG_FILE

# Step 3: Sign the Server CSR with CA, including SAN
echo "Signing Server CSR with CA, including SAN..."
openssl x509 -req -in $SERVER_CSR -CA $CA_CERT -CAkey $CA_KEY -CAcreateserial \
  -out $SERVER_CERT -days $DAYS_VALID -sha256 -extfile $CONFIG_FILE -extensions req_ext

# Step 4: Combine Server Certificate and Key into PEM format
echo "Combining Server Certificate and Key into PEM format..."
cat $SERVER_CERT $SERVER_KEY > $SERVER_PEM

# Display the results
echo "====================================="
echo "Server setup is complete. Files created:"
echo "Server Key: $SERVER_KEY"
echo "Server CSR: $SERVER_CSR"
echo "Server Certificate: $SERVER_CERT"
echo "Server PEM: $SERVER_PEM"
echo "====================================="

# scp ./tls_certs/server.pem worker1:/root/ultralytics/ultralytics/federated/tls_certs/
