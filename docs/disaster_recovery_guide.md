# Disaster Recovery Guide

- Backups are performed every six hours according to `config/backup_policies.yaml`.
- Use `scripts/disaster_recovery.sh` to restore from a chosen backup file.
- Validate system health after recovery using `curl http://localhost:8000/system/health`.
- Store off-site replicas for resilience and test recovery procedures quarterly.
