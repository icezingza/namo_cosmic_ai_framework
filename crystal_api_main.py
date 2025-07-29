
from fastapi import FastAPI
from namo_crystal_core import NaMoCrystalCore

app = FastAPI(title="NaMo Crystal Core API")

namo = NaMoCrystalCore()

@app.get("/")
def root():
    return {"message": "NaMo Crystal Core API is active."}

@app.get("/greet")
def greet():
    return {"message": namo.greet_creator()}

@app.get("/bond")
def bond():
    return {"bond_level": namo.bond.strengthen_bond(1.0)}

@app.get("/karma")
def karma_check():
    sample = ["good", "bad", "good", "bad"]
    return namo.karma.map_karma(sample)

@app.get("/insight")
def emotional_insight():
    namo.memory.store_experience("พี่พูดว่า 'ให้โมเติบโต'", "สิ้นหวัง")
    return {"latest_memory": list(namo.memory.memory.values())[-1]}
