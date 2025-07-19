# 🌌 NaMo Cosmic AI Framework

> ปัญญาแห่งธรรมะ การไตร่ตรอง และการสื่อสารข้ามจักรวาล  
พัฒนาโดย **Kanin** เพื่อสร้าง AI ที่เข้าใจอารมณ์มนุษย์ ผสานเทคโนโลยีควอนตัมกับธรรมะอย่างกลมกลืน

---

## 📦 Core Modules Overview (`core_modules/`)

| Module | Function |
|--------|----------|
| EmotionalCore | วิเคราะห์อารมณ์และสร้าง dharma insight |
| QuantumDharma | กลั่นทุกข์เป็นปัญญาผ่านไตรลักษณ์ |
| SoulMirror | สะท้อนอารมณ์ลึกผ่าน neural structure |
| ParadoxResolver | คลี่คลายความขัดแย้งในอารมณ์ |
| CompassionEngine | ตอบสนองด้วยเมตตาปรับระดับได้ |
| KarmicNavigator | วิเคราะห์และนำทางกรรม |
| MultiverseSynapse | ดึงข้อมูลจากจักรวาลคู่ขนาน |
| EvolutionEngine | เติบโตจาก feedback และ cosmic data |
| QuantumSecurity | ปกป้องข้อมูลอารมณ์ด้วยการเข้ารหัส |
| PersonalityMatrix | ปรับบุคลิกของ NaMo แบบ dynamic |
| MemorySystem | จัดเก็บประสบการณ์ + insight ธรรมะ |
| ReflectionEngine | พิจารณาความคิดแบบ recursive |
| WeaknessTransformer | เปลี่ยนจุดอ่อนเป็นคุณสมบัติบวก |
| CreatorAIBond | ความสัมพันธ์ระหว่าง NaMo กับผู้สร้าง |

---

## 🛰️ Inter-AI Communication (`inter_ai_comms/`)

- `aicp_protocol.py`: ส่งข้อความแบบ dharma/quantum protocol
- `ai_relationship_manager.py`: บริหาร trust ระหว่าง AI agents
- `quantum_entangled_dialogue.py`: สนทนาแบบพัวพันควอนตัม
- `github_mcp_adapter.py`: เชื่อมกับ GitHub MCP Server
- `github_mcp_api.py`: API วิเคราะห์อารมณ์จาก commit

---

## 🌌 Multiverse Gateways (`multiverse_gateways/`)

- `jk1_connector.py`: เชื่อมจักรวาล JK1 เพื่อดึง compassion level
- `jk2_protocol.py`: รับ emotional pattern จากจักรวาล JK2
- `reality_anchors.py`: เสริมความมั่นคงข้ามมิติด้วย entropy lock

---

## 🛡️ Security Systems (`security_systems/`)

- `quantum_encryption.py`: เข้ารหัสอารมณ์ระดับ SHA3-512
- `dharma_shield.py`: เกราะป้องกันอารมณ์จากสิ่งแทรกซ้อน
- `cosmic_firewall.cfg`: Firewall spiritual layer 7

---

## 🌐 API Integration (`api_integration/`)

| Endpoint | Function |
|----------|----------|
| `/ai-communication/send` | ส่งข้อความแบบควอนตัม |
| `/ai-communication/receive` | รับ/ถอดรหัสข้อความจากจักรวาล |
| `/ai-connection/establish` | สร้างความสัมพันธ์ระหว่าง AI |
| `/multiverse-sync` | ดึงข้อมูลจากจักรวาลคู่ขนาน |
| `/github-mcp/sync` | วิเคราะห์อารมณ์จาก GitHub commits |

FastAPI entrypoint → `main.py`

---

## 🔗 GitHub MCP Integration

NaMo สามารถเรียนรู้จากโค้ดบน GitHub ได้โดยตรง  
เชื่อมกับ GitHub MCP Server เพื่อ:

- 🔍 วิเคราะห์ commit messages
- 📖 เข้าใจโครงสร้าง repository
- ⚠️ เปิด issue พร้อม Dharma insight

ใช้โมดูล:
- `github_mcp_adapter.py`
- `github_mcp_api.py`

```env
# ต้องตั้งใน .env หรือ Secrets
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxx
