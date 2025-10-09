#!/bin/bash
set -e

echo "🚀 Deploying Infinity AI Framework to Production..."

source .env.production

if [ -z "$DB_PASSWORD" ] || [ -z "$REDIS_PASSWORD" ]; then
  echo "❌ Missing required environment variables"
  exit 1
fi

echo "📦 Building Docker images..."
docker-compose -f docker-compose.prod.yml build

echo "🔄 Running database migrations..."
docker-compose -f docker-compose.prod.yml run --rm infinity-ai \
  python -m alembic upgrade head

echo "🚀 Deploying services..."
docker-compose -f docker-compose.prod.yml up -d

echo "⏳ Waiting for services to be healthy..."
sleep 30

echo "🏥 Running health checks..."
if ! curl -f http://localhost:8000/system/health; then
  echo "❌ Health check failed"
  docker-compose -f docker-compose.prod.yml logs infinity-ai
  exit 1
fi

echo "✅ Deployment completed successfully!"
echo "📊 Dashboard available at: http://localhost:3000"
echo "🔧 API Documentation at: http://localhost:8000/docs"
