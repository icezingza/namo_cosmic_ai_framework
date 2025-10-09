#!/bin/bash
set -e

echo "⚙️ Running performance benchmark"
pytest tests/performance_tests.py --benchmark-disable
