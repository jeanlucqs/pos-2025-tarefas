import json

CAMINHO_JSON = "parsers/imobiliaria.json"

# Carrega os dados do arquivo
with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
    dados = json.load(f)

imoveis = dados.get("imobiliaria", [])

def mostrar_menu():
    print("\n📋 Lista de Imóveis:\n")
    for i, imovel in enumerate(imoveis, start=1):
        print(f"{i}. {imovel['descricao']}")

def mostrar_detalhes(imovel):
    print("\n📄 Detalhes do Imóvel Selecionado:\n")
    print("Descrição:", imovel["descricao"])

    prop = imovel["proprietario"]
    print("Proprietário(a):", prop["nome"])
    print("Email:", prop.get("email", "(nenhum informado)"))

    telefones = prop.get("telefones", [])
    if telefones:
        print("Telefones:", ", ".join(telefones))
    else:
        print("Telefones: (nenhum informado)")

    end = imovel["endereco"]
    print("\n--- Endereço ---")
    print("Rua:", end.get("rua", ""))
    print("Bairro:", end.get("bairro", ""))
    print("Cidade:", end.get("cidade", ""))
    print("Número:", end.get("numero", "S/N"))

    carac = imovel["caracteristicas"]
    print("\n--- Características ---")
    print(f"Tamanho: {carac['tamanho']} m²")
    print("Número de Quartos:", carac["numQuartos"])
    print("Número de Banheiros:", carac["numBanheiros"])

    print("\nValor:", imovel["valor"])

while True:
    mostrar_menu()

    try:
        escolha = int(input("\nDigite o número do imóvel para ver mais detalhes: "))
        if not (1 <= escolha <= len(imoveis)):
            print("⚠️ Escolha inválida. Tente novamente.")
            continue
    except ValueError:
        print("⚠️ Entrada inválida. Digite um número.")
        continue

    mostrar_detalhes(imoveis[escolha - 1])

    continuar = input("\nDeseja consultar outro imóvel? (s/n): ").strip().lower()
    if continuar != 's':
        print("\n✅ Sessão encerrada. Obrigado por usar o sistema!")
        break
