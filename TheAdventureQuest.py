import requests
import time

# Sua chave de API do OpenRouter
API_KEY = "Put Your OpenRouter Key here"

# Função para perguntar ao OpenRouter
def perguntar_ao_chatgpt(mensagem):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",  # Pode ser outro modelo também, tipo mistral/mistral-7b-instruct
        "messages": [
            {"role": "system", "content": "Você é um mestre de RPG que cria aventuras baseadas nas escolhas do jogador."},
            {"role": "user", "content": mensagem}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    return data['choices'][0]['message']['content']

# Começar o jogo
print("Bem-vindo ao The Adventure Quest!")
mensagem = "Começar Aventura."

# Dentro do loop do jogo:
historia = "Você é um mestre de RPG. Crie o começo de sua história."

try:
    with open("aventura_salva.txt", "r", encoding="utf-8") as arquivo:
        historia = arquivo.read()
    print("Aventura carregada!\n")
except FileNotFoundError:
    historia = "Você é um mestre de RPG. Crie o começo de sua história."

while True:
    resposta = perguntar_ao_chatgpt(historia)
    print("\n" + resposta)

    escolha = input("\nO que irá fazer agora?: ")
    historia += f"\n{resposta}\nVocê Escolheu: {escolha}\nContinue a história:"

    if escolha.lower() == "salvar":
        with open("aventura_salva.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(historia)
        print("Jogo salvo! Continue jogando ou digite outra ação.")
        continue

    if any(palavra in resposta.lower() for palavra in ["fim", "morreu", "completou", "venceu"]):
        print("\n--- FIM DA HISTÓRIA ---\n")
        break

    # Pausar 5 segundos para evitar overload
    time.sleep(15)