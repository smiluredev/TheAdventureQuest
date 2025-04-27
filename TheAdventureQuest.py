import openai
import time

# Pedir a chave da API para o jogador
api_key = input("Digite sua chave de API do OpenRouter: ").strip()

# Conectar no OpenRouter usando a chave do jogador
client = openai.OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Função para perguntar ao ChatGPT
def perguntar_ao_chatgpt(mensagem):
    resposta = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",  # modelo via OpenRouter
        messages=[
            {"role": "system", "content": "Você é um mestre de RPG que cria aventuras baseadas nas escolhas do jogador."},
            {"role": "user", "content": mensagem}
        ]
    )
    return resposta.choices[0].message.content

# Começar o jogo
print("Bem-vindo ao The Adventure Quest!")
mensagem = "Começar Aventura."

# Carregar história salva (se existir)
try:
    with open("aventura_salva.txt", "r", encoding="utf-8") as arquivo:
        historia = arquivo.read()
    print("Aventura carregada!\n")
except FileNotFoundError:
    historia = "Você é um mestre de RPG. Crie o começo de uma aventura medieval para o jogador."

# Loop principal do jogo
while True:
    resposta = perguntar_ao_chatgpt(historia)
    print("\n" + resposta)
    
    escolha = input("\nO que irá fazer agora? ")
    historia += f"\n{resposta}\nVocê Escolheu: {escolha}\nContinue a história:"
    
    if escolha.lower() == "salvar":
        with open("aventura_salva.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(historia)
        print("Jogo salvo! Continue jogando ou digite outra ação.")
        continue

    if any(palavra in resposta.lower() for palavra in ["fim", "morreu", "completou", "venceu"]):
        print("\n--- FIM DA HISTÓRIA ---\n")
        break

    time.sleep(5)  # pausa para não sobrecarregar

