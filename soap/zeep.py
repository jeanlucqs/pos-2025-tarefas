import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
import json

class SOAPClient:  
    def __init__(self, wsdl_url=None):
        self.wsdl_url = wsdl_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': ''
        })
    
    def create_soap_envelope(self, body_content):
        envelope = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" 
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
               xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soap:Body>
        {body_content}
    </soap:Body>
</soap:Envelope>"""
        return envelope
    
    def send_soap_request(self, url, soap_envelope, soap_action=""):
        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': soap_action
        }
        
        try:
            response = requests.post(url, data=soap_envelope, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição SOAP: {e}")
            return None
    
    def parse_soap_response(self, response):
        if not response:
            return None
        
        try:
            root = ET.fromstring(response.text)
            return root
        except ET.ParseError as e:
            print(f"Erro ao parsear resposta SOAP: {e}")
            return None
    
    def prettify_xml(self, xml_string):
        try:
            parsed = minidom.parseString(xml_string)
            return parsed.toprettyxml(indent="  ")
        except Exception as e:
            print(f"Erro ao formatar XML: {e}")
            return xml_string


class CalculatorSOAPClient(SOAPClient):
    
    def __init__(self):
        # URL de exemplo - substitua por um serviço real
        super().__init__("http://www.dneonline.com/calculator.asmx?WSDL")
        self.service_url = "http://www.dneonline.com/calculator.asmx"
    
    def add_numbers(self, num1, num2):
        body_content = f""
        
        soap_envelope = self.create_soap_envelope(body_content)
        soap_action = "http://tempuri.org/Add"
        
        print(f"Enviando requisição SOAP para somar {num1} + {num2}")
        print("Envelope SOAP:")
        print(self.prettify_xml(soap_envelope))
        
        response = self.send_soap_request(self.service_url, soap_envelope, soap_action)
        
        if response and response.status_code == 200:
            print(f"Resposta recebida (Status: {response.status_code})")
            print("Resposta SOAP:")
            print(self.prettify_xml(response.text))
            
            # Parse da resposta
            root = self.parse_soap_response(response)
            if root:
                # Extrair resultado
                namespaces = {
                    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
                    'temp': 'http://tempuri.org/'
                }
                
                result_elem = root.find('.//temp:AddResult', namespaces)
                if result_elem is not None:
                    result = int(result_elem.text)
                    return {
                        'success': True,
                        'result': result,
                        'operation': f"{num1} + {num2} = {result}"
                    }
        
        return {'success': False, 'error': 'Falha na operação SOAP'}
    
    def subtract_numbers(self, num1, num2):
        body_content = f"""
        <Subtract xmlns="http://tempuri.org/">
            <intA>{num1}</intA>
            <intB>{num2}</intB>
        </Subtract>
        """
        
        soap_envelope = self.create_soap_envelope(body_content)
        soap_action = "http://tempuri.org/Subtract"
        
        print(f"Enviando requisição SOAP para subtrair {num1} - {num2}")
        
        response = self.send_soap_request(self.service_url, soap_envelope, soap_action)
        
        if response and response.status_code == 200:
            root = self.parse_soap_response(response)
            if root:
                namespaces = {
                    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
                    'temp': 'http://tempuri.org/'
                }
                
                result_elem = root.find('.//temp:SubtractResult', namespaces)
                if result_elem is not None:
                    result = int(result_elem.text)
                    return {
                        'success': True,
                        'result': result,
                        'operation': f"{num1} - {num2} = {result}"
                    }
        
        return {'success': False, 'error': 'Falha na operação SOAP'}


class GenericSOAPClient(SOAPClient):
    def __init__(self, service_url):
        super().__init__()
        self.service_url = service_url
    
    def call_soap_method(self, method_name, parameters, namespace="http://tempuri.org/", soap_action=""):
        params_xml = ""
        for key, value in parameters.items():
            params_xml += f"<{key}>{value}</{key}>\n"
        
        body_content = f"""
        <{method_name} xmlns="{namespace}">
            {params_xml}
        </{method_name}>
        """
        
        soap_envelope = self.create_soap_envelope(body_content)
        
        print(f"Chamando método SOAP: {method_name}")
        print("Envelope SOAP:")
        print(self.prettify_xml(soap_envelope))
        
        response = self.send_soap_request(self.service_url, soap_envelope, soap_action)
        
        if response:
            print(f"Resposta recebida (Status: {response.status_code})")
            print("Resposta SOAP:")
            print(self.prettify_xml(response.text))
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'response': response.text,
                    'status_code': response.status_code
                }
        
        return {
            'success': False,
            'error': 'Falha na requisição SOAP',
            'status_code': response.status_code if response else None
        }


def demonstrate_soap_clients():
    print("=== DEMONSTRAÇÃO DE CLIENTES SOAP ===")
    
    print("\n1. TESTANDO CLIENTE SOAP DE CALCULADORA")
    print("-" * 50)
    
    calc_client = CalculatorSOAPClient()
    
    print("\n--- Teste de Soma ---")
    result = calc_client.add_numbers(15, 25)
    if result['success']:
        print(f"✅ Resultado: {result['operation']}")
    else:
        print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
    
    print("\n--- Teste de Subtração ---")
    result = calc_client.subtract_numbers(50, 20)
    if result['success']:
        print(f"✅ Resultado: {result['operation']}")
    else:
        print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
    
    print("\n\n2. TESTANDO CLIENTE SOAP GENÉRICO")
    print("-" * 50)
    
    generic_client = GenericSOAPClient("http://www.webservicex.net/ConvertTemperature.asmx")
    
    parameters = {
        'Temperature': '32',
        'FromUnit': 'degreeFahrenheit',
        'ToUnit': 'degreeCelsius'
    }
    
    print("\n--- Exemplo de conversão de temperatura ---")
    result = generic_client.call_soap_method(
        method_name="ConvertTemp",
        parameters=parameters,
        namespace="http://www.webservicex.net/",
        soap_action="http://www.webservicex.net/ConvertTemp"
    )
    
    if result['success']:
        print("✅ Requisição SOAP enviada com sucesso")
    else:
        print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")


def create_manual_soap_example():
    print("\n\n3. EXEMPLO MANUAL DE SOAP")
    print("-" * 50)
    
    soap_client = SOAPClient()
    
    cep_body = """
    <ConsultaCEP xmlns="http://cep.republicavirtual.com.br/">
        <cep>01310-100</cep>
    </ConsultaCEP>
    """
    
    envelope = soap_client.create_soap_envelope(cep_body)
    
    print("Exemplo de envelope SOAP para consulta de CEP:")
    print(soap_client.prettify_xml(envelope))
    
    # Exemplo de parsing de resposta SOAP
    sample_response = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ConsultaCEPResponse xmlns="http://cep.republicavirtual.com.br/">
            <ConsultaCEPResult>
                <resultado>1</resultado>
                <resultado_txt>sucesso - cep completo</resultado_txt>
                <uf>SP</uf>
                <cidade>São Paulo</cidade>
                <bairro>Bela Vista</bairro>
                <tipo_logradouro>Avenida</tipo_logradouro>
                <logradouro>Paulista</logradouro>
            </ConsultaCEPResult>
        </ConsultaCEPResponse>
    </soap:Body>
</soap:Envelope>"""
    
    print("\nExemplo de resposta SOAP:")
    print(soap_client.prettify_xml(sample_response))
    
    root = ET.fromstring(sample_response)
    namespaces = {
        'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
        'cep': 'http://cep.republicavirtual.com.br/'
    }
    
    resultado = root.find('.//cep:resultado', namespaces)
    uf = root.find('.//cep:uf', namespaces)
    cidade = root.find('.//cep:cidade', namespaces)
    logradouro = root.find('.//cep:logradouro', namespaces)
    
    if resultado is not None:
        print(f"\n--- Dados extraídos da resposta SOAP ---")
        print(f"Resultado: {resultado.text}")
        print(f"UF: {uf.text if uf is not None else 'N/A'}")
        print(f"Cidade: {cidade.text if cidade is not None else 'N/A'}")
        print(f"Logradouro: {logradouro.text if logradouro is not None else 'N/A'}")


def soap_error_handling_example():
    print("\n\n4. EXEMPLO DE TRATAMENTO DE ERROS SOAP")
    print("-" * 50)
    
    soap_client = SOAPClient()
    
    fault_response = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <soap:Fault>
            <faultcode>Client</faultcode>
            <faultstring>Invalid parameter value</faultstring>
            <detail>
                <error>O valor do parâmetro 'cep' é inválido</error>
            </detail>
        </soap:Fault>
    </soap:Body>
</soap:Envelope>"""
    
    print("Exemplo de SOAP Fault (erro):")
    print(soap_client.prettify_xml(fault_response))
    
    root = ET.fromstring(fault_response)
    namespaces = {'soap': 'http://schemas.xmlsoap.org/soap/envelope/'}
    
    fault = root.find('.//soap:Fault', namespaces)
    if fault is not None:
        faultcode = fault.find('faultcode')
        faultstring = fault.find('faultstring')
        detail = fault.find('detail/error')
        
        print(f"\n--- Erro SOAP detectado ---")
        print(f"Código: {faultcode.text if faultcode is not None else 'N/A'}")
        print(f"Mensagem: {faultstring.text if faultstring is not None else 'N/A'}")
        print(f"Detalhe: {detail.text if detail is not None else 'N/A'}")


def main():
    print("CLIENTE SOAP - Demonstração completa")
    print("Este script demonstra como trabalhar com serviços SOAP usando Python")
    
    try:
        demonstrate_soap_clients()
        create_manual_soap_example()
        soap_error_handling_example()
        
        print("\n" + "="*60)
        print("RESUMO DOS CONCEITOS SOAP DEMONSTRADOS:")
        print("="*60)
        print("1. Criação de envelopes SOAP")
        print("2. Envio de requisições SOAP com requests")
        print("3. Parsing de respostas SOAP com ElementTree")
        print("4. Tratamento de SOAP Faults (erros)")
        print("5. Clientes especializados vs genéricos")
        print("6. Formatação e exibição de XML")
        print("="*60)
        
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        print("Nota: Alguns serviços SOAP podem não estar disponíveis para teste.")


if __name__ == "__main__":
    main()