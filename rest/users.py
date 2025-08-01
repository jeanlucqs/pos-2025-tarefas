import requests
import json
from typing import Dict, List, Optional

class JSONPlaceholderClient:
    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.users_endpoint = f"{self.base_url}/users"
    
    def get_all_users(self) -> List[Dict]:
        try:
            response = requests.get(self.users_endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar usuários: {e}")
            return []
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        try:
            response = requests.get(f"{self.users_endpoint}/{user_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar usuário {user_id}: {e}")
            return None
    
    def create_user(self, user_data: Dict) -> Optional[Dict]:
        try:
            response = requests.post(
                self.users_endpoint,
                json=user_data,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao criar usuário: {e}")
            return None
    
    def update_user(self, user_id: int, user_data: Dict) -> Optional[Dict]:
        try:
            response = requests.put(
                f"{self.users_endpoint}/{user_id}",
                json=user_data,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao atualizar usuário {user_id}: {e}")
            return None
    
    def delete_user(self, user_id: int) -> bool:
        try:
            response = requests.delete(f"{self.users_endpoint}/{user_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao deletar usuário {user_id}: {e}")
            return False
    
    def display_user_info(self, user: Dict) -> None:
        print(f"\n--- Usuário ID: {user.get('id', 'N/A')} ---")
        print(f"Nome: {user.get('name', 'N/A')}")
        print(f"Username: {user.get('username', 'N/A')}")
        print(f"Email: {user.get('email', 'N/A')}")
        print(f"Telefone: {user.get('phone', 'N/A')}")
        print(f"Website: {user.get('website', 'N/A')}")
        
        address = user.get('address', {})
        if address:
            print(f"Endereço: {address.get('street', '')}, {address.get('suite', '')}")
            print(f"Cidade: {address.get('city', '')}")
            print(f"CEP: {address.get('zipcode', '')}")
        
        company = user.get('company', {})
        if company:
            print(f"Empresa: {company.get('name', '')}")
            print(f"Slogan: {company.get('catchPhrase', '')}")
        
        print("-" * 40)


def main():
    client = JSONPlaceholderClient()
    
    print("=== CLIENTE JSONPLACEHOLDER - GERENCIAMENTO DE USUÁRIOS ===")
    
    print("\n1. Listando todos os usuários:")
    users = client.get_all_users()
    print(f"Total de usuários encontrados: {len(users)}")
    
    for user in users[:3]:
        client.display_user_info(user)
    
    print("\n2. Buscando usuário específico (ID: 1):")
    user = client.get_user_by_id(1)
    if user:
        client.display_user_info(user)
    
    print("\n3. Criando novo usuário:")
    new_user_data = {
        "name": "João Silva",
        "username": "joaosilva",
        "email": "joao.silva@example.com",
        "phone": "(11) 99999-9999",
        "website": "joaosilva.com",
        "address": {
            "street": "Rua das Flores",
            "suite": "Apt. 101",
            "city": "São Paulo",
            "zipcode": "01234-567",
            "geo": {
                "lat": "-23.5505",
                "lng": "-46.6333"
            }
        },
        "company": {
            "name": "Tech Solutions",
            "catchPhrase": "Inovação em cada linha de código",
            "bs": "desenvolvimento de software"
        }
    }
    
    created_user = client.create_user(new_user_data)
    if created_user:
        print("Usuário criado com sucesso:")
        client.display_user_info(created_user)
    
    print("\n4. Atualizando usuário (ID: 1):")
    update_data = {
        "id": 1,
        "name": "Leanne Graham Updated",
        "username": "Bret_Updated",
        "email": "leanne.updated@example.com",
        "phone": "(11) 88888-8888"
    }
    
    updated_user = client.update_user(1, update_data)
    if updated_user:
        print("Usuário atualizado com sucesso:")
        client.display_user_info(updated_user)
    
    print("\n5. Deletando usuário (ID: 1):")
    success = client.delete_user(1)
    if success:
        print("Usuário deletado com sucesso!")
    else:
        print("Erro ao deletar usuário.")
    
    print("\n=== FIM DOS TESTES ===")


if __name__ == "__main__":
    main()