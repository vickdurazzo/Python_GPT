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

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def analisador_sentimento(produto):
    prompt_sistema = f"""
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

        # Formato de Saída

        Nome do Produto:
        Resumo das Avaliações:
        Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Ponto fortes: lista com três bullets
        Pontos fracos: lista com três bullets
    """
    
    prompt_usuario = carrega(f"./dados/avaliacoes-{produto}.txt")
    print(f"Iniciou a análise de sentimentos do produto {produto}")



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

    texto_resposta = resposta.choices[0].message.content
    salva(f"./dados/analise-{produto}.txt", texto_resposta)

analisador_sentimento("Maquiagem mineral")
