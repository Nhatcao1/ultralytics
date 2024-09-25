#!/bin/bash

# Paths for certificates and keys
CERT_DIR="./tls_certs"
CA_KEY="$CERT_DIR/ca.key"
CA_CERT="$CERT_DIR/ca.crt"
CLIENT_CSR="$CERT_DIR/client.csr"
CLIENT_CERT="$CERT_DIR/client.crt"
DAYS_VALID=365

# Step 4: Sign the Client CSR
echo "Signing Client CSR with CA..."
openssl x509 -req -in $CLIENT_CSR -CA $CA_CERT -CAkey $CA_KEY -CAcreateserial -out $CLIENT_CERT -days $DAYS_VALID -sha256

# Display the result
echo "====================================="
echo "Client certificate signed. Files created:"
echo "Client Certificate: $CLIENT_CERT"
echo "====================================="

# scp ./tls_certs/client.crt worker1:/root/ultralytics/ultralytics/federated/tls_certs
