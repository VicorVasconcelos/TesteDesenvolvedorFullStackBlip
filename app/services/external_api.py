import httpx
import os
from typing import Optional
import time


class ExternalAPIService:
    def __init__(self):
        self.api_url = os.getenv("EXTERNAL_API_URL", "https://dummyjson.com/users/1")
        
        self.timeout = 3.0
    
    async def get_birth_date(self) -> Optional[str]:
        """
        Busca a data de nascimento da API externa.
        Retorna None em caso de falha.
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.api_url)
                response.raise_for_status()
                data = response.json()
                
               
                birth_date = data["birthDate"]
                return birth_date
                
        except httpx.TimeoutException:
            print("Timeout ao buscar data de nascimento")
            return None
        except httpx.HTTPError as e:
            print(f"Erro HTTP ao buscar data de nascimento: {e}")
            return None
        except Exception as e:
            
            print(f"Erro desconhecido: {e}")
            return None


# Instância global
external_api_service = ExternalAPIService()
