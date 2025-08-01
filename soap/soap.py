from zeep import Client, Settings
from zeep.transports import Transport
from zeep.exceptions import Fault, TransportError, ValidationError
from requests import Session
from requests.auth import HTTPBasicAuth
import logging
import sys

logging.basicConfig(level=logging.INFO)


class ZeepSOAPClient:    
    def __init__(self, wsdl_url, username=None, password=None, timeout=30):
        self.wsdl_url = wsdl_url
        
        session = Session()
        if username and password:
            session.auth = HTTPBasicAuth(username, password)
        
        transport = Transport(session=session, timeout=timeout)
    
        settings = Settings(strict=False, xml_huge_tree=True)
        
        try:
            # Criar cliente Zeep
            self.client = Client(wsdl_url, transport=transport, settings=settings)
            print(f"✅ Cliente SOAP criado com sucesso para: {wsdl_url}")
            
        except Exception as e:
            print(f"❌ Erro ao criar cliente SOAP: {e}")
            self.client = None
    
    def list_services(self):
        if not self.client:
            return None
        
        print("\n=== SERVIÇOS DISPONÍVEIS ===")
        for service_name, service in self.client.wsdl.services.items():
            print(f"\nServiço: {service_name}")
            print(f"  Endpoint: {service.ports[list(service.ports.keys())[0]].address}")
            
            for operation_name, operation in service.ports[list(service.ports.keys())[0]].binding._operations.items():
                print(f"  Operação: {operation_name}")
                
                # Mostrar parâmetros de entrada
                if hasattr(operation.input, 'signature'):
                    print(f"    Entrada: {operation.input.signature}")
                
                # Mostrar parâmetros de saída
                if hasattr(operation.output, 'signature'):
                    print(f"    Saída: {operation.output.signature}")
    
    def call_service(self, service_name, operation_name, **kwargs):
        if not self.client:
            return {'success': False, 'error': 'Cliente não inicializado'}
        
        try:
            service = getattr(self.client.service, operation_name)
            
            print(f"Chamando {operation_name} com parâmetros: {kwargs}")
            
            result = service(**kwargs)
            
            print(f"✅ Operação {operation_name} executada com sucesso")
            
            return {
                'success': True,
                'result': result,
                'operation': operation_name,
                'parameters': kwargs
            }
            
        except Fault as fault:
            error_msg = f"SOAP Fault: {fault}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'type': 'soap_fault'
            }
            
        except ValidationError as ve:
            error_msg = f"Erro de validação: {ve}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'type': 'validation_error'
            }
            
        except TransportError as te:
            error_msg = f"Erro de transporte: {te}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'type': 'transport_error'
            }
            
        except Exception as e:
            error_msg = f"Erro inesperado: {e}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'type': 'unknown_error'
            }


class CalculatorZeepClient(ZeepSOAPClient):    
    def __init__(self):
        wsdl_url = "http://www.dneonline.com/calculator.asmx?WSDL"
        super().__init__(wsdl_url)
    
    def add(self, num1, num2):
        """Soma dois números"""
        return self.call_service("Calculator", "Add", intA=num1, intB=num2)
    
    def subtract(self, num1, num2):
        """Subtrai dois números"""
        return self.call_service("Calculator", "Subtract", intA=num1, intB=num2)
    
    def multiply(self, num1, num2):
        """Multiplica dois números"""
        return self.call_service("Calculator", "Multiply", intA=num1, intB=num2)
    
    def divide(self, num1, num2):
        """Divide dois números"""
        return self.call_service("Calculator", "Divide", intA=num1, intB=num2)


class NumberConversionZeepClient(ZeepSOAPClient):   
    def __init__(self):
        wsdl_url = "https://www.dataaccess.com/webservicesserver/numberconversion.wso?WSDL"
        super().__init__(wsdl_url)
    
    def number_to_words(self, number):
        """Converte número para palavras"""
        return self.call_service("NumberConversion", "NumberToWords", ubiNum=number)
    
    def number_to_dollars(self, number):
        """Converte número para formato de dólares"""
        return self.call_service("NumberConversion", "NumberToDollars", dNum=number)


class WeatherZeepClient(ZeepSOAPClient):    
    def __init__(self):
        wsdl_url = "http://www.webservicex.net/globalweather.asmx?WSDL"
        super().__init__(wsdl_url)
    
    def get_cities_by_country(self, country_name):
        """Obtém cidades por país"""
        return self.call_service("GlobalWeather", "GetCitiesByCountry", CountryName=country_name)
    
    def get_weather(self, city_name, country_name):
        """Obtém clima de uma cidade"""
        return self.call_service("GlobalWeather", "GetWeather", 
                               CityName=city_name, CountryName=country_name)


def test_calculator_client():
    print("\n" + "="*60)
    print("TESTANDO CLIENTE DE CALCULADORA COM ZEEP")
    print("="*60)
    
    calc = CalculatorZeepClient()
    
    if not calc.client:
        print("❌ Não foi possível conectar ao serviço de calculadora")
        return
    
    calc.list_services()
    
    operations = [
        ("Soma", lambda: calc.add(15, 25)),
        ("Subtração", lambda: calc.subtract(50, 20)),
        ("Multiplicação", lambda: calc.multiply(7, 8)),
        ("Divisão", lambda: calc.divide(100, 4))
    ]
    
    for op_name, op_func in operations:
        print(f"\n--- {op_name} ---")
        try:
            result = op_func()
            if result['success']:
                print(f"✅ Resultado: {result['result']}")
            else:
                print(f"❌ Erro: {result['error']}")
        except Exception as e:
            print(f"❌ Erro na operação {op_name}: {e}")


def test_number_conversion_client():
    print("\n" + "="*60)
    print("TESTANDO CLIENTE DE CONVERSÃO DE NÚMEROS COM ZEEP")
    print("="*60)
    
    converter = NumberConversionZeepClient()
    
    if not converter.client:
        print("❌ Não foi possível conectar ao serviço de conversão")
        return
    
    converter.list_services()
    
    test_numbers = [123, 1000, 25]
    
    for number in test_numbers:
        print(f"\n--- Convertendo número: {number} ---")
        
        words_result = converter.number_to_words(number)
        if words_result['success']:
            print(f"Em palavras: {words_result['result']}")
        else:
            print(f"❌ Erro ao converter para palavras: {words_result['error']}")
        
        dollars_result = converter.number_to_dollars(number)
        if dollars_result['success']:
            print(f"Em dólares: {dollars_result['result']}")
        else:
            print(f"❌ Erro ao converter para dólares: {dollars_result['error']}")


def test_weather_client():
    print("\n" + "="*60)
    print("TESTANDO CLIENTE DE CLIMA COM ZEEP")
    print("="*60)
    
    weather = WeatherZeepClient()
    
    if not weather.client:
        print("❌ Não foi possível conectar ao serviço de clima")
        return
    
    weather.list_services()
    
    country = "Brazil"
    print(f"\n--- Buscando cidades no {country} ---")
    cities_result = weather.get_cities_by_country(country)
    
    if cities_result['success']:
        print("✅ Cidades encontradas (primeiras 5):")
        cities_data = str(cities_result['result'])[:500] + "..."
        print(cities_data)
    else:
        print(f"❌ Erro ao buscar cidades: {cities_result['error']}")
    
    city = "São Paulo"
    print(f"\n--- Buscando clima para {city}, {country} ---")
    weather_result = weather.get_weather(city, country)
    
    if weather_result['success']:
        print(f"✅ Clima obtido: {str(weather_result['result'])[:200]}...")
    else:
        print(f"❌ Erro ao buscar clima: {weather_result['error']}")


def demonstrate_zeep_features():
    print("\n" + "="*60)
    print("DEMONSTRANDO RECURSOS ESPECÍFICOS DO ZEEP")
    print("="*60)
    
    print("\n1. VANTAGENS DO ZEEP:")
    print("   ✅ Parse automático do WSDL")
    print("   ✅ Validação automática de tipos")
    print("   ✅ Geração automática de classes Python")
    print("   ✅ Suporte a namespaces complexos")
    print("   ✅ Tratamento robusto de erros SOAP")
    print("   ✅ Suporte a autenticação HTTP")
    print("   ✅ Cache de WSDL")
    
    print("\n2. COMPARAÇÃO COM SOAP MANUAL:")
    print("   Manual: Criar envelope XML manualmente")
    print("   Zeep:   client.service.operation_name(param1=value1)")
    print()
    print("   Manual: Parsear resposta XML manualmente")
    print("   Zeep:   Retorna objetos Python diretamente")
    print()
    print("   Manual: Validação manual de tipos")
    print("   Zeep:   Validação automática baseada no WSDL")
    
    print("\n3. EXEMPLO DE USO SIMPLIFICADO:")
    print("""
    from zeep import Client
    client = Client('http://example.com/service?wsdl')
    result = client.service.my_operation(param1='value1')
    
    # Sem Zeep (complexo):
    # - Criar envelope SOAP XML
    # - Configurar headers HTTP
    # - Enviar requisição POST
    # - Parsear resposta XML
    # - Extrair dados manualmente
    """)


def main():
    print("CLIENTE SOAP COM ZEEP - Demonstração completa")
    print("Este script demonstra como usar a biblioteca Zeep para consumir serviços SOAP")
    
    try:
        # Testar diferentes clientes
        test_calculator_client()
        test_number_conversion_client()
        test_weather_client()
        demonstrate_zeep_features()
        
        print("\n" + "="*60)
        print("RESUMO DA DEMONSTRAÇÃO ZEEP:")
        print("="*60)
        print("1. Cliente de calculadora (operações matemáticas)")
        print("2. Cliente de conversão de números")
        print("3. Cliente de serviços de clima")
        print("4. Recursos e vantagens do Zeep")
        print("\nNota: Alguns serviços podem não estar disponíveis temporariamente.")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro durante a execução: {e}")
        print("Verifique sua conexão com a internet e a disponibilidade dos serviços.")


if __name__ == "__main__":
    main()