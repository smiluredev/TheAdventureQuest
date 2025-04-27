import requests
import time
import sys

# Pedir a chave da API para o jogador
api_key = input("Digite sua chave de API do OpenRouter: ").strip()

# Função para perguntar ao OpenRouter
def perguntar_ao_openrouter(mensagem):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Você é um mestre de RPG que cria aventuras baseadas nas escolhas do jogador."},
            {"role": "user", "content": mensagem}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        resposta_json = response.json()
        return resposta_json["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Erro ao se comunicar com o OpenRouter: {e}")
        return None

# Função para carregar a aventura salva
def carregar_aventura():
    try:
        with open("aventura_salva.txt", "r", encoding="utf-8") as arquivo:
            historia = arquivo.read()
        print("\nAventura carregada com sucesso!\n")
        return historia
    except FileNotFoundError:
        print("\nNenhuma aventura salva encontrada. Iniciando uma nova...\n")
        return "Você é um mestre de RPG. Crie o começo de uma aventura medieval para o jogador."

# Função para salvar a aventura
def salvar_aventura(historia):
    with open("aventura_salva.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(historia)
    print("\nJogo salvo com sucesso!\n")

# Função para iniciar a aventura
def iniciar_aventura(historia_inicial):
    historia = historia_inicial

    while True:
        resposta = perguntar_ao_openrouter(historia)

        if not resposta:
            print("Erro na resposta. Encerrando o jogo.")
            break

        print("\n" + resposta)

        escolha = input("\nO que irá fazer agora? ")

        # Atualizar história
        historia += f"\n{resposta}\nJogador escolheu: {escolha}\nContinue a história:"

        if escolha.lower() == "salvar":
            salvar_aventura(historia)
            continue

        if escolha.lower() == "sair":
            print("\nSaindo da aventura...\n")
            break

        if any(palavra in resposta.lower() for palavra in ["fim", "morreu", "completou", "venceu"]):
            print("\n--- FIM DA HISTÓRIA ---\n")
            break

        time.sleep(5)

# Função principal com menu
def menu_principal():
    while True:
        print("\n=== The Adventure Quest ===")
        print("1) Novo Jogo")
        print("2) Carregar Aventura")
        print("3) Sair")

        escolha = input("\nEscolha uma opção (1-3): ")

        if escolha == "1":
            historia_inicial = "Você é um mestre de RPG. Crie o começo de uma aventura medieval para o jogador."
            iniciar_aventura(historia_inicial)
        elif escolha == "2":
            historia_carregada = carregar_aventura()
            iniciar_aventura(historia_carregada)
        elif escolha == "3":
            print("\nObrigado por jogar!")
            sys.exit()
        else:
            print("\nOpção inválida. Tente novamente.")

# Iniciar o programa
menu_principal()
