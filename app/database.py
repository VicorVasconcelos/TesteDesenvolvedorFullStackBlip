from pymongo import MongoClient
from pymongo.collection import Collection
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do MongoDB
MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "leads_db")

client = None
db = None

def connect_db():
    """Conecta ao MongoDB"""
    global client, db
    client = MongoClient(MONGO_URL)
    db = client[DATABASE_NAME]
    print("Conectado ao MongoDB")

def get_leads_collection() -> Collection:
    """Retorna a coleção de leads"""
    if db is None:
        connect_db()
    return db["leads"]

def close_db():
    """Fecha a conexão com MongoDB"""
    if client:
        client.close()
