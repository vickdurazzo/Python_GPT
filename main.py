from openai import OpenAI
from dotenv import load_dotenv #usado para lermos as chaves de acessos da openai
import os

load_dotenv()
#Buscando a chave de acesso no .env
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

resposta = cliente.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content":"Listar apenas os nomes dos produtos, sem considerar descrição."
        },
        {
            "role": "user",
            "content":"Liste 3 produtos sustentáveis"
        }
    ],
    model="gpt-3.5-turbo",
)

print(resposta)