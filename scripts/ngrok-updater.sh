#!/bin/sh
set -e

WORKDIR=/workdir
API_HOST=${NGROK_HOST:-ngrok}
API_PORT=${NGROK_PORT:-4040}
API_URL="http://${API_HOST}:${API_PORT}/api/tunnels"
interval=${SLEEP_INTERVAL:-2}

echo "Waiting for ngrok API at $API_URL"
while true; do
  resp=$(curl -s "$API_URL" || true)
  pub=$(echo "$resp" | jq -r '.tunnels[0].public_url // empty')
  if [ -n "$pub" ]; then
    echo "Found ngrok URL: $pub"
    break
  fi
  sleep "$interval"
done

# update .env atomically
tmp="${WORKDIR}/.env.tmp.$$"
if [ -f "${WORKDIR}/.env" ]; then
  grep -v '^CSRF_TRUSTED_ORIGINS=' "${WORKDIR}/.env" > "$tmp" || true
else
  : > "$tmp"
fi

echo "CSRF_TRUSTED_ORIGINS=$pub" >> "$tmp"
mv "$tmp" "${WORKDIR}/.env"

echo ".env updated with: CSRF_TRUSTED_ORIGINS=$pub"

# restart web container discovered by compose label
web_name=$(docker ps --filter "label=com.docker.compose.service=web" --format '{{.Names}}' | head -n1)
if [ -n "$web_name" ]; then
  echo "Restarting web container $web_name"
  docker restart "$web_name"
else
  echo "Web container not found; please restart web manually"
fi
