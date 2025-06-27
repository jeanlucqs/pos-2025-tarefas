import xml.etree.ElementTree as ET
import json

# Entrada e saída
arquivo_xml = "parsers/imobiliaria.xml"
arquivo_json = "parsers/imobiliaria.json"

# Lê o XML
tree = ET.parse(arquivo_xml)
root = tree.getroot()

# Namespace usado no XML
ns = {"ns": "http://imobiliaria.org"}

# Lista que armazenará os imóveis convertidos
imoveis = []

for imovel in root.findall("ns:imovel", ns):
    descricao = imovel.find("ns:descricao", ns).text.strip()

    prop_tag = imovel.find("ns:proprietario", ns)
    nome = prop_tag.find("ns:nome", ns).text.strip()
    email = prop_tag.findtext("ns:email", default=None, namespaces=ns)
    telefones = [tel.text.strip() for tel in prop_tag.findall("ns:telefone", ns)]

    proprietario = {
        "nome": nome,
        "email": email,
        "telefones": telefones
    }

    endereco_tag = imovel.find("ns:endereco", ns)
    endereco = {
        tag.tag.replace("{http://imobiliaria.org}", ""): tag.text.strip()
        for tag in endereco_tag
    }

    carac_tag = imovel.find("ns:caracteristicas", ns)
    caracteristicas = {
        "tamanho": float(carac_tag.find("ns:tamanho", ns).text),
        "numQuartos": int(carac_tag.find("ns:numQuartos", ns).text),
        "numBanheiros": int(carac_tag.find("ns:numBanheiros", ns).text)
    }

    valor = imovel.find("ns:valor", ns).text.strip()

    imoveis.append({
        "descricao": descricao,
        "proprietario": proprietario,
        "endereco": endereco,
        "caracteristicas": caracteristicas,
        "valor": valor
    })

with open(arquivo_json, "w", encoding="utf-8") as f:
    json.dump({"imobiliaria": imoveis}, f, indent=2, ensure_ascii=False)

print(f"Arquivo '{arquivo_json}' gerado com sucesso!")
