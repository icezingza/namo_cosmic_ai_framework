# Scaling Guide

1. Monitor resource utilisation with Prometheus metrics exposed on port `8001`.
2. Use the `ScalabilityEngine` to evaluate scaling decisions based on CPU, memory, and business KPIs.
3. Configure Kubernetes HPA using the manifests under `deployment/kubernetes/`.
4. For Docker deployments, adjust replica counts in `docker-compose.prod.yml`.
5. Review `config/scaling_policies.yaml` for threshold tuning and cooldown strategies.
