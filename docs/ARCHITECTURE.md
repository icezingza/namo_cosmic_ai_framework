# Architecture (Draft)
- Layers:
  - core_modules/ — ตรรกะหลัก (stateless ให้มากที่สุด)
  - api_integration/ — การเชื่อมต่อภายนอก (GitHub MCP, LLMs, Multiverse)
  - deployment/ — Dockerfile, cloudbuild, Procfile
- Dataflow (คร่าว ๆ):
  Inputs → api_integration → core_modules → outputs

> เติม diagram จาก assets/ และคำอธิบายแต่ละโมดูลจริง
