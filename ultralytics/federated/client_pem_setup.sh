#!/bin/bash

# Set variables for certificate details
COUNTRY="US"
STATE="State"
LOCALITY="City"
ORGANIZATION="MyOrg"
ORG_UNIT="IT"
COMMON_NAME_CLIENT="client"
DAYS_VALID=365

# Paths for certificates and keys
CERT_DIR="./ssl_certs"
CLIENT_KEY="$CERT_DIR/client.key"
CLIENT_CERT="$CERT_DIR/client.pem"

# Create directory for certificates and keys
mkdir -p $CERT_DIR

# Step 1: Generate the Client Private Key
echo "Generating Client Private Key..."
openssl genpkey -algorithm RSA -out $CLIENT_KEY
if [ $? -ne 0 ]; then
    echo "Failed to generate the client private key."
    exit 1
fi

# Step 2: Generate a self-signed Client Certificate
echo "Generating self-signed Client Certificate (PEM)..."
openssl req -new -x509 -key $CLIENT_KEY -out $CLIENT_CERT -days $DAYS_VALID -subj "/C=$COUNTRY/ST=$STATE/L=$LOCALITY/O=$ORGANIZATION/OU=$ORG_UNIT/CN=$COMMON_NAME_CLIENT"
if [ $? -ne 0 ]; then
    echo "Failed to generate the client certificate."
    exit 1
fi

# Display the results
echo "====================================="
echo "Client PEM setup is complete. Files created:"
echo "Client Private Key: $CLIENT_KEY"
echo "Client Certificate (PEM): $CLIENT_CERT"
echo "====================================="

scp ./ssl_certs/client.pem root@master:/root/ultralytics/ultralytics/federated/ssl_certs