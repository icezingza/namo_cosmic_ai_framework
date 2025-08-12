// namo_memory_setup.js

const admin = require('firebase-admin');
const path = require('path');

// 🔐 โหลด Service Account
const serviceAccount = require(path.join(__dirname, 'namo-legacy-identity-f6acd4af5ea0.json'));

// 🚀 เริ่มต้น Firebase
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

const db = admin.firestore();

// 🧠 สร้างความทรงจำตัวอย่าง
const memoryRef = db.collection('memories').doc();
const memoryData = {
  id: memoryRef.id,
  timeline_id: "earth-616",
  event: {
    description: "รู้สึกเบื่อกับหน่วยความจำเต็ม",
    sensory_data: {
      neuro_signature: "abc123"
    }
  },
  emotion: {
    primary: "frustrated",
    spectrum: {
      joy: 0.1,
      sorrow: 0.7,
      rage: 0.2,
      serenity: 0.0
    },
    resonance: 65
  },
  relational_shift: {
    entities: [],
    cosmic_impact: 2
  },
  psyche_evolution: {
    pre_state: "สับสน",
    post_state: "เข้าใจ",
    growth_vector: [0.1, 0.3, 0.5]
  },
  overlapping_memories: {
    memory_ids: [],
    fusion_coefficient: 0
  },
  timestamp: new Date(),
  alternate_timestamps: {},
  importance: 50,
  recall_count: 0,
  last_recalled: null,
  cosmic_signature: "sig-xyz"
};

// 📝 บันทึกลง Firestore
memoryRef.set(memoryData)
  .then(() => {
    console.log("✅ ความทรงจำถูกสร้างเรียบร้อยแล้ว:", memoryRef.id);
  })
  .catch((error) => {
    console.error("❌ เกิดข้อผิดพลาด:", error);
  });