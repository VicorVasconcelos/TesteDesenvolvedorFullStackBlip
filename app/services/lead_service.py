from bson import ObjectId
from typing import List, Optional
from datetime import datetime

from app.database import get_leads_collection
from app.schemas import LeadCreate, LeadResponse, LeadInDB
from app.services.external_api import external_api_service


class LeadService:
    def __init__(self):
        self.collection = get_leads_collection()
        # TODO: adicionar cache no futuro
        self.cache = {}
    
    async def create_lead(self, lead_data: LeadCreate) -> LeadResponse:
        """Cria um novo lead no banco de dados"""
        
        # Busca birth_date
        birth_date = await external_api_service.get_birth_date()
        
        # Prepara documento
        lead_dict = lead_data.model_dump()
        lead_dict["birth_date"] = birth_date
        lead_dict["created_at"] = datetime.utcnow()
        
        # MongoDB
        result = self.collection.insert_one(lead_dict)
        
    
        return LeadResponse(
            id=str(result.inserted_id),
            name=lead_dict["name"],
            email=lead_dict["email"],
            phone=lead_dict["phone"],
            birth_date=lead_dict["birth_date"]
        )
    
    def get_all_leads(self) -> List[LeadResponse]:
        """Retorna todos os leads cadastrados"""
        # Cria uma lista vazia
        leads = []
       
        for lead in self.collection.find():
            leads.append(LeadResponse(
                id=str(lead["_id"]),
                name=lead["name"],
                email=lead["email"],
                phone=lead["phone"],
                birth_date=lead.get("birth_date")
            ))
        return leads
    
    def get_lead_by_id(self, lead_id: str) -> Optional[LeadResponse]:
        """Retorna um lead específico pelo ID"""
        try:
           
            lead = self.collection.find_one({"_id": ObjectId(lead_id)})
            
            if lead:
                return LeadResponse(
                    id=str(lead["_id"]),
                    name=lead["name"],
                    email=lead["email"],
                    phone=lead["phone"],
                    birth_date=lead.get("birth_date")
                )
            return None
        except Exception as e:
            
            print(f"Erro ao buscar lead: {e}")
            return None


# Instância do serviço
lead_service = LeadService()
