#!/bin/sh

# Generate self-signed SSL cert if real cert doesn't exist.
# This allows nginx to always start on 8443, even without Let's Encrypt certs.
CERT_DIR="/etc/nginx/ssl/live/YOUR_DOMAIN"
CERT="$CERT_DIR/fullchain.pem"

if [ ! -f "$CERT" ]; then
    mkdir -p "$CERT_DIR"
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$CERT_DIR/privkey.pem" \
        -out "$CERT_DIR/fullchain.pem" \
        -subj "/CN=localhost" 2>/dev/null
fi
