from openai import OpenAI
from dotenv import load_dotenv #usado para lermos as chaves de acessos da openai
import os

load_dotenv()
#Buscando a chave de acesso no .env
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-3.5-turbo"

def categoriza_produto(nome_produto, lista_categorias_possiveis):
    #criando um template, melhorando a engenharia do prompt
    prompt_sistema = f"""
    Você é um categorizador de produtos.
            Você deve assumir as categorias presentes na lista abaixo.

            # Lista de Categorias Válidas
            {lista_categorias_possiveis.split(",")}	

            # Formato da Saída
            Produto: Nome do Produto
            Categoria: apresente a categoria do produto

            # Exemplo de Saída
            Produto: Escova elétrica com recarga solar
            Categoria: Eletrônicos Verdes
    """
    resposta = cliente.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content":prompt_sistema
            },
            {
                "role": "user",
                "content":nome_produto
            }
        ],
        model=modelo,
        temperature = 0, #melhorar a aleatoriedade
        max_tokens=200, #limite de palavras
        n = 1  #quantidade de respostas possiveis
    )
    return resposta.choices[0].message.content

categorias_validas = input("Informe as categorias validas (Separado por virgulas): ")

while True:
    nome_produto = input("Nome do Produto: ")
    texto_reposta = categoriza_produto(nome_produto, categorias_validas)
    print(texto_reposta)


#print(resposta.choices[0].message.content) #imprimi a primeira resposta
"""
loop para pegar cada resposta possivel que a openai retornou
for contador in range(0,3):
    print(resposta.choices[contador].message.content)
"""