from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from app.database import connect_db, close_db
from app.services.lead_service import lead_service
from app.schemas import LeadCreate, LeadResponse

app = FastAPI(
    title="Leads API", 
    version="1.0.0",
    description="API de Gerenciamento de Leads"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """Conecta ao banco na inicialização"""
    connect_db()
    print("API iniciada com MongoDB!")


@app.on_event("shutdown")
async def shutdown():
    """Fecha conexão com banco"""
    close_db()


@app.post("/leads", response_model=LeadResponse, status_code=201)
async def create_lead(lead: LeadCreate):
    """
    Cria um novo lead
    """
    try:
        return await lead_service.create_lead(lead)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/leads", response_model=List[LeadResponse])
def get_leads():
    """
    Lista todos os leads
    """
    return lead_service.get_all_leads()


@app.get("/leads/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: str):
    """
    Retorna um lead específico por ID
    """
    lead = lead_service.get_lead_by_id(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    return lead


@app.get("/")
def root():
    """Endpoint raiz"""
    return {"message": "API de Leads", "docs": "/docs"}
