#!/bin/bash

# Set certificate details
COUNTRY="US"
STATE="State"
LOCALITY="City"
ORGANIZATION="MyOrg"
ORG_UNIT="IT"
COMMON_NAME="RootCA"
DAYS_VALID=365

# Paths for CA certificates and keys
CERT_DIR="./tls_certs"
CA_KEY="$CERT_DIR/ca.key"
CA_CERT="$CERT_DIR/ca.crt"

# Create directory for certificates
mkdir -p $CERT_DIR

# Step 1: Generate the Root CA
echo "Generating Root CA..."
openssl genpkey -algorithm RSA -out $CA_KEY
openssl req -x509 -new -nodes -key $CA_KEY -sha256 -days $DAYS_VALID -out $CA_CERT -subj "/C=$COUNTRY/ST=$STATE/L=$LOCALITY/O=$ORGANIZATION/OU=$ORG_UNIT/CN=$COMMON_NAME"

# Display the result
echo "====================================="
echo "CA setup is complete. Files created:"
echo "Root CA Key: $CA_KEY"
echo "Root CA Certificate: $CA_CERT"
echo "====================================="

#scp ./tls_certs/client.crt worker1:/root/ultralytics/ultralytics/federated/tls_certs/
