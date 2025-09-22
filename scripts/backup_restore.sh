#!/bin/bash
set -e

BACKUP_DIR=${1:-./deployment/backups}
RESTORE_TARGET=${2:-latest}

if [ ! -d "$BACKUP_DIR" ]; then
  echo "❌ Backup directory not found: $BACKUP_DIR"
  exit 1
fi

if [ "$RESTORE_TARGET" = "latest" ]; then
  BACKUP_FILE=$(ls -t "$BACKUP_DIR" | head -n 1)
else
  BACKUP_FILE=$RESTORE_TARGET
fi

if [ -z "$BACKUP_FILE" ]; then
  echo "❌ No backup files available"
  exit 1
fi

echo "📦 Restoring from backup: $BACKUP_FILE"
docker-compose -f docker-compose.prod.yml down
cat "$BACKUP_DIR/$BACKUP_FILE" | docker-compose -f docker-compose.prod.yml run --rm db \
  psql -h db -U user -d infinity_ai

docker-compose -f docker-compose.prod.yml up -d
