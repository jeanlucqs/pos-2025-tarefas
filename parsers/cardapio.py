from xml.dom.minidom import parse

dom = parse("parsers/cardapio.xml")
pratos = dom.getElementsByTagName("prato")

print("Lista de Pratos:\n")
for i, prato in enumerate(pratos, start=1):
    nome = prato.getElementsByTagName("nome")[0].firstChild.nodeValue.strip()
    print(f"{i}. {nome}")

escolha = int(input("\nDigite o número do prato para ver os detalhes: "))
prato = pratos[escolha - 1]

nome = prato.getElementsByTagName("nome")[0].firstChild.nodeValue.strip()
descricao = prato.getElementsByTagName("descricao")[0].firstChild.nodeValue.strip()
ingredientes = [
    ing.firstChild.nodeValue.strip()
    for ing in prato.getElementsByTagName("ingredientes")[0].getElementsByTagName("ingrediente")
]

preco = prato.getElementsByTagName("preco")[0].firstChild.nodeValue.strip()
calorias = prato.getElementsByTagName("calorias")[0].firstChild.nodeValue.strip()
tempo_preparo = prato.getElementsByTagName("tempo_preparo")[0].firstChild.nodeValue.strip()

print("\n--- Detalhes do Prato ---")
print("Nome:", nome)
print("Descrição:", descricao)
print("Ingredientes:", ", ".join(ingredientes))
print("Preço:", preco)
print("Calorias:", calorias)
print("Tempo de Preparo:", tempo_preparo)
