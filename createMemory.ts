import db from './initFirestore';

export async function createMemory(data: any): Promise<string> {
  const memoryRef = db.collection('memories').doc();

  const memoryData = {
    ...data,
    id: memoryRef.id,
    timestamp: new Date(),
    importance: 50,
    recall_count: 0,
    last_recalled: null,
  };

  await memoryRef.set(memoryData);
  return memoryRef.id;
}