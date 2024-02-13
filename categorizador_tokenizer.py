from openai import OpenAI
from dotenv import load_dotenv
from itertools import islice
import os
import tiktoken

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo="gpt-3.5-turbo"

codificador = tiktoken.encoding_for_model(modelo)

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            # Lê as primeiras 10 linhas do arquivo
            dados = islice(arquivo, 20)
            # Converte as linhas em uma string
            dados = "".join(dados)
            return dados
    except IOError as e:
        print(f"Erro: {e}")

prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

prompt_usuario = carrega("dados\lista_de_compras_100_clientes.csv")


arquivo_csv = "./dados/lista_de_compras_100_clientes.csv"
dados_usuario = carrega(arquivo_csv)
lista_tokens = codificador.encode(dados_usuario)
numero_tokens = len(lista_tokens)
#se o tamanho for maior do que o esperado e maior do que o suportado pelo modelo
modelo = "gpt-3.5-turbo" if numero_tokens < 4097 else "GPT-4"



print(f"Quantidade de Tokens: {numero_tokens}")
print(f"Modelo escolhido: {modelo}")


lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": prompt_usuario
        }
    ]


resposta = client.chat.completions.create(
    messages = lista_mensagens,
    model=modelo
)

print(resposta.choices[0].message.content)
