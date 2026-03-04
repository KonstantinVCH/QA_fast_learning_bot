#!/bin/bash
# QA Fast Learning Bot v2.1 — deploy script
# Usage: ./deploy.sh
# Requires: SERVER, SSH_KEY, QA_BOT_TOKEN, OPENROUTER_API_KEY env vars
set -e

SERVER="${SERVER:-serverhshp.com}"
BOT_DIR="/opt/qa_bot"
SERVICE_NAME="qa_bot"

echo "=== QA Bot v2.1 Deploy ==="
echo "Target: $SERVER"

# Upload code (only qa_bot package + requirements + run script)
echo "Uploading files..."
ssh root@"$SERVER" "mkdir -p $BOT_DIR"
rsync -av --delete \
    --include="qa_bot/" \
    --include="qa_bot/**" \
    --include="requirements.txt" \
    --exclude="*" \
    . root@"$SERVER":"$BOT_DIR"/

# Install dependencies
echo "Installing dependencies..."
ssh root@"$SERVER" "cd $BOT_DIR && pip install -r requirements.txt --quiet"

# Create .env if not exists
ssh root@"$SERVER" "
  if [ ! -f $BOT_DIR/.env ]; then
    echo 'QA_BOT_TOKEN=FILL_ME' > $BOT_DIR/.env
    echo 'OPENROUTER_API_KEY=FILL_ME' >> $BOT_DIR/.env
    echo 'LOG_LEVEL=INFO' >> $BOT_DIR/.env
    echo '⚠️ Created .env — fill in the tokens!'
  fi
"

# Create systemd service
ssh root@"$SERVER" "cat > /etc/systemd/system/${SERVICE_NAME}.service << 'EOF'
[Unit]
Description=QA Fast Learning Bot v2.1
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$BOT_DIR
EnvironmentFile=$BOT_DIR/.env
ExecStart=/usr/bin/python3 -m qa_bot.bot
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF"

# Enable and start
ssh root@"$SERVER" "
  systemctl daemon-reload
  systemctl enable $SERVICE_NAME
  systemctl restart $SERVICE_NAME
  sleep 2
  systemctl status $SERVICE_NAME --no-pager
"

echo "=== Deploy complete! ==="
