import asyncio
import os

from fastmcp import Client
from openai import OpenAI
import dotenv

caminho_servidor = 'http://localhost:8000/sse'
cliente = Client(caminho_servidor)


async def testar_servidor(cliente, busca):
    dotenv.load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    async with cliente:
        argumentos = {"busca": busca}
        resultado = await cliente.call_tool("buscar_wikipedia", arguments=argumentos)
        print(resultado)

        mensagem_sistema = f"""
        Voce é um bot que faz busca na wikipedia, o usuario buscou pelo 
        seguinte tema: {busca}. 
        Para esta busca, voce recebeu a seguinte responsta: {resultado} 
        Com base neste conteudo formate uma resposta amigavel ao usuário
        """
        cliente_openai = OpenAI(api_key=api_key)

        response = cliente_openai.responses.create(
            model='gpt-4o-mini',
            instructions=mensagem_sistema,
            input="Pode me falar mais sobre este assunto?"
        )
        print(response.output_text)

if __name__ == "__main__":
    asyncio.run(testar_servidor(
        cliente=cliente,
        busca='Isaac Asimov')
    )