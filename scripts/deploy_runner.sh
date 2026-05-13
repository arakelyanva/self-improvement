#!/usr/bin/env bash
set -euo pipefail

# Required Parameters passed from the action lifecycle
HETZNER_CLOUD_TOKEN="${1}"
CF_TUNNEL_TOKEN="${2}"
RUNNER_REGISTRATION_TOKEN="${3}"
REPO_URL="${4}"

cat << EOF > cloud-config.yaml
#cloud-config
runcmd:
  # Firewall setup
  - ufw default deny incoming
  - ufw allow out to any
  - ufw --force enable

  # CF tunnel setup
  - mkdir -p /etc/cloudflared
  - curl -L --output /tmp/cloudflared.deb github.com
  - dpkg -i /tmp/cloudflared.deb
  - cloudflared service install "${CF_TUNNEL_TOKEN}"

  # GHA self-hosted setup
  - mkdir /actions-runner && cd /actions-runner
  - curl -o actions-runner-linux-x64-2.334.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.334.0/actions-runner-linux-x64-2.334.0.tar.gz
  - tar xzf ./actions-runner-linux-x64-2.334.0.tar.gz
  - useradd -m -s /bin/bash ubuntu
  - chown -R ubuntu:ubuntu /actions-runner
  - sudo -u ubuntu ./config.sh --url "${REPO_URL}" --token "${RUNNER_REGISTRATION_TOKEN}" --name "hetzner-isolated-node" --labels "hetzner-vps" --ephemeral --unattended
  - sudo -u ubuntu ./run.sh
EOF

PAYLOAD=$(jq -n \
  --arg name "ephemeral-test-node" \
  --arg server_type "cx23" \
  --arg image "ubuntu-24.04" \
  --rawfile user_data cloud-config.yaml \
  '{name: $name, server_type: $server_type, image: $image, user_data: $user_data}')

echo "Provisioning cost-optimized Hetzner VPS instance..."
curl -X POST \
  -H "Authorization: Bearer ${HETZNER_CLOUD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  "https://api.hetzner.cloud/v1/servers"

