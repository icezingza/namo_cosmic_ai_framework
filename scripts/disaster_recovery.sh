#!/bin/bash
set -e

echo "🔄 Starting Disaster Recovery Process..."

BACKUP_DIR="/backups"
RESTORE_DATE="${1:-$(date +%Y%m%d)}"
BACKUP_FILE="$BACKUP_DIR/backup-$RESTORE_DATE.sql"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "❌ Backup file not found: $BACKUP_FILE"
  exit 1
fi

echo "📦 Restoring from backup: $BACKUP_FILE"

echo "🛑 Stopping services..."
docker-compose -f docker-compose.prod.yml down

echo "💾 Restoring database..."
docker-compose -f docker-compose.prod.yml run --rm db \
  psql -h db -U user -d infinity_ai < "$BACKUP_FILE"

echo "🚀 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

echo "✅ Verifying restoration..."
sleep 10
if ! curl -f http://localhost:8000/system/health; then
  echo "❌ Restoration verification failed"
  exit 1
fi

echo "🎉 Disaster recovery completed successfully!"
