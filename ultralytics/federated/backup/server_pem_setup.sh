#!/bin/bash

# Set variables for certificate details
COUNTRY="US"
STATE="State"
LOCALITY="City"
ORGANIZATION="MyOrg"
ORG_UNIT="IT"
COMMON_NAME_SERVER="server"
DAYS_VALID=365

# Paths for certificates and keys (all in the tls_certs directory)
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

# Step 1: Generate the Root CA (Certificate Authority)
echo "Generating Root CA..."
openssl genpkey -algorithm RSA -out $CA_KEY
openssl req -x509 -new -nodes -key $CA_KEY -sha256 -days $DAYS_VALID -out $CA_CERT -subj "/C=$COUNTRY/ST=$STATE/L=$LOCALITY/O=$ORGANIZATION/OU=$ORG_UNIT/CN=RootCA"

# Step 2: Generate the Server Private Key
echo "Generating Server Key..."
openssl genpkey -algorithm RSA -out $SERVER_KEY

# Step 3: Generate the Server CSR with configuration for SAN
echo "Generating Server CSR with SAN..."
openssl req -new -key $SERVER_KEY -out $SERVER_CSR -config $CONFIG_FILE

# Step 4: Generate the Server Certificate with SAN (Subject Alternative Name)
echo "Signing Server Certificate with CA, including SAN..."
openssl x509 -req -in $SERVER_CSR -CA $CA_CERT -CAkey $CA_KEY -CAcreateserial \
  -out $SERVER_CERT -days $DAYS_VALID -sha256 -extfile $CONFIG_FILE -extensions req_ext

# Step 5: Verify the Server Certificate
echo "Verifying the Server Certificate..."
openssl verify -CAfile $CA_CERT $SERVER_CERT

# Step 6: Combine Server Certificate and Key into PEM format for easier management
echo "Combining Server Certificate and Key into a single PEM file..."
cat $SERVER_CERT $SERVER_KEY > $SERVER_PEM

# Display the results
echo "====================================="
echo "Server TLS setup is complete. Files created:"
echo "Root CA: $CA_CERT"
echo "Server Key: $SERVER_KEY"
echo "Server CSR: $SERVER_CSR"
echo "Server Certificate: $SERVER_CERT"
echo "Server PEM: $SERVER_PEM"
echo "====================================="
