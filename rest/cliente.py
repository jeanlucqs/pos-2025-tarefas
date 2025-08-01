import sys
from users import JSONPlaceholderClient

class InteractiveClient:
    
    def __init__(self):
        self.client = JSONPlaceholderClient()
    
    def show_menu(self):
        print("\n" + "="*50)
        print("    CLIENTE JSONPLACEHOLDER - MENU PRINCIPAL")
        print("="*50)
        print("1. Listar todos os usuários")
        print("2. Buscar usuário por ID")
        print("3. Criar novo usuário")
        print("4. Atualizar usuário")
        print("5. Deletar usuário")
        print("6. Sair")
        print("="*50)
    
    def list_all_users(self):
        print("\n--- LISTANDO TODOS OS USUÁRIOS ---")
        users = self.client.get_all_users()
        
        if not users:
            print("Nenhum usuário encontrado ou erro na requisição.")
            return
        
        print(f"Total de usuários: {len(users)}")
        print("\nResumo dos usuários:")
        print("-" * 60)
        print(f"{'ID':<4} {'Nome':<20} {'Username':<15} {'Email':<20}")
        print("-" * 60)
        
        for user in users:
            print(f"{user.get('id', 'N/A'):<4} "
                  f"{user.get('name', 'N/A')[:19]:<20} "
                  f"{user.get('username', 'N/A')[:14]:<15} "
                  f"{user.get('email', 'N/A')[:19]:<20}")
        
        while True:
            choice = input("\nDeseja ver detalhes de algum usuário? (s/n): ").lower()
            if choice == 'n':
                break
            elif choice == 's':
                try:
                    user_id = int(input("Digite o ID do usuário: "))
                    user = next((u for u in users if u['id'] == user_id), None)
                    if user:
                        self.client.display_user_info(user)
                    else:
                        print("Usuário não encontrado na lista.")
                except ValueError:
                    print("ID inválido. Digite um número.")
                break
            else:
                print("Opção inválida. Digite 's' ou 'n'.")
    
    def search_user_by_id(self):
        print("\n--- BUSCAR USUÁRIO POR ID ---")
        try:
            user_id = int(input("Digite o ID do usuário: "))
            user = self.client.get_user_by_id(user_id)
            
            if user:
                self.client.display_user_info(user)
            else:
                print(f"Usuário com ID {user_id} não encontrado.")
        except ValueError:
            print("ID inválido. Digite um número.")
    
    def create_new_user(self):
        print("\n--- CRIAR NOVO USUÁRIO ---")
        print("Digite as informações do novo usuário:")
        
        try:
            user_data = {}
            
            user_data['name'] = input("Nome completo: ").strip()
            user_data['username'] = input("Username: ").strip()
            user_data['email'] = input("Email: ").strip()
            user_data['phone'] = input("Telefone: ").strip()
            user_data['website'] = input("Website (opcional): ").strip()
            
            print("\n--- Endereço ---")
            address = {}
            address['street'] = input("Rua: ").strip()
            address['suite'] = input("Complemento (opcional): ").strip()
            address['city'] = input("Cidade: ").strip()
            address['zipcode'] = input("CEP: ").strip()
            
            geo = {}
            lat = input("Latitude (opcional): ").strip()
            lng = input("Longitude (opcional): ").strip()
            if lat and lng:
                geo['lat'] = lat
                geo['lng'] = lng
                address['geo'] = geo
            
            user_data['address'] = address
            
            print("\n--- Empresa ---")
            company = {}
            company_name = input("Nome da empresa (opcional): ").strip()
            if company_name:
                company['name'] = company_name
                company['catchPhrase'] = input("Slogan da empresa (opcional): ").strip()
                company['bs'] = input("Área de atuação (opcional): ").strip()
                user_data['company'] = company
            
            if not user_data['name'] or not user_data['email']:
                print("Nome e email são obrigatórios!")
                return
            
            # Criar usuário
            created_user = self.client.create_user(user_data)
            if created_user:
                print("\n✅ Usuário criado com sucesso!")
                self.client.display_user_info(created_user)
            else:
                print("❌ Erro ao criar usuário.")
                
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
    
    def update_user(self):
        print("\n--- ATUALIZAR USUÁRIO ---")
        try:
            user_id = int(input("Digite o ID do usuário a ser atualizado: "))
            
            # Buscar usuário atual
            current_user = self.client.get_user_by_id(user_id)
            if not current_user:
                print(f"Usuário com ID {user_id} não encontrado.")
                return
            
            print("\nUsuário atual:")
            self.client.display_user_info(current_user)
            
            print("\nDigite os novos dados (deixe em branco para manter o valor atual):")
            
            updated_data = {'id': user_id}
            
            new_name = input(f"Nome [{current_user.get('name', '')}]: ").strip()
            if new_name:
                updated_data['name'] = new_name
            else:
                updated_data['name'] = current_user.get('name', '')
            
            new_username = input(f"Username [{current_user.get('username', '')}]: ").strip()
            if new_username:
                updated_data['username'] = new_username
            else:
                updated_data['username'] = current_user.get('username', '')
            
            new_email = input(f"Email [{current_user.get('email', '')}]: ").strip()
            if new_email:
                updated_data['email'] = new_email
            else:
                updated_data['email'] = current_user.get('email', '')
            
            new_phone = input(f"Telefone [{current_user.get('phone', '')}]: ").strip()
            if new_phone:
                updated_data['phone'] = new_phone
            else:
                updated_data['phone'] = current_user.get('phone', '')
            
            new_website = input(f"Website [{current_user.get('website', '')}]: ").strip()
            if new_website:
                updated_data['website'] = new_website
            else:
                updated_data['website'] = current_user.get('website', '')
            
            updated_user = self.client.update_user(user_id, updated_data)
            if updated_user:
                print("\n✅ Usuário atualizado com sucesso!")
                self.client.display_user_info(updated_user)
            else:
                print("❌ Erro ao atualizar usuário.")
                
        except ValueError:
            print("ID inválido. Digite um número.")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
    
    def delete_user(self):
        print("\n--- DELETAR USUÁRIO ---")
        try:
            user_id = int(input("Digite o ID do usuário a ser deletado: "))
            
            # Buscar usuário para confirmação
            user = self.client.get_user_by_id(user_id)
            if not user:
                print(f"Usuário com ID {user_id} não encontrado.")
                return
            
            print("\nUsuário a ser deletado:")
            self.client.display_user_info(user)
            
            # Confirmação
            confirm = input("\nTem certeza que deseja deletar este usuário? (s/N): ").lower()
            if confirm == 's':
                success = self.client.delete_user(user_id)
                if success:
                    print("✅ Usuário deletado com sucesso!")
                else:
                    print("❌ Erro ao deletar usuário.")
            else:
                print("Operação cancelada.")
                
        except ValueError:
            print("ID inválido. Digite um número.")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
    
    def run(self):
        print("Bem-vindo ao Cliente JSONPlaceholder!")
        print("Este cliente permite gerenciar usuários através da API JSONPlaceholder.")
        
        while True:
            try:
                self.show_menu()
                choice = input("\nEscolha uma opção (1-6): ").strip()
                
                if choice == '1':
                    self.list_all_users()
                elif choice == '2':
                    self.search_user_by_id()
                elif choice == '3':
                    self.create_new_user()
                elif choice == '4':
                    self.update_user()
                elif choice == '5':
                    self.delete_user()
                elif choice == '6':
                    print("\nObrigado por usar o Cliente JSONPlaceholder!")
                    sys.exit(0)
                else:
                    print("Opção inválida. Escolha uma opção de 1 a 6.")
                
                # Pausa para o usuário ver o resultado
                input("\nPressione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\nPrograma interrompido pelo usuário.")
                sys.exit(0)
            except Exception as e:
                print(f"Erro inesperado: {e}")
                input("Pressione Enter para continuar...")


def main():
    client = InteractiveClient()
    client.run()


if __name__ == "__main__":
    main()