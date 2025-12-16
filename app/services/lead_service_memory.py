from typing import List, Optional, Dict
from datetime import datetime
from bson import ObjectId

from app.schemas import LeadCreate, LeadResponse
from app.services.external_api import external_api_service



leads_storage: Dict[str, dict] = {}


class LeadServiceInMemory:
    """
    Versão em memória do serviço de leads.
    Funciona sem MongoDB para testes.
    """
    
    async def create_lead(self, lead_data: LeadCreate) -> LeadResponse:
        """Cria um novo lead no storage em memória"""
        
        # Busca birth_date
        birth_date = await external_api_service.get_birth_date()
        
        # Gera ID
        lead_id = str(ObjectId())
        
        # Prepara documento
        lead_dict = {
            "_id": lead_id,
            "name": lead_data.name,
            "email": lead_data.email,
            "phone": lead_data.phone,
            "birth_date": birth_date,
            "created_at": datetime.utcnow()
        }
        
        # Salva em memória
        leads_storage[lead_id] = lead_dict
        
        return LeadResponse(
            id=lead_id,
            name=lead_dict["name"],
            email=lead_dict["email"],
            phone=lead_dict["phone"],
            birth_date=lead_dict["birth_date"]
        )
    
    def get_all_leads(self) -> List[LeadResponse]:
        """Retorna todos os leads do storage"""
        leads = []
        
        
        for lead in leads_storage.values():
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
        
        # Busca no storage
        lead = leads_storage.get(lead_id)
        
        if lead:
            return LeadResponse(
                id=str(lead["_id"]),
                name=lead["name"],
                email=lead["email"],
                phone=lead["phone"],
                birth_date=lead.get("birth_date")
            )
        return None


# Instância
lead_service_memory = LeadServiceInMemory()
