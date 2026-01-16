import asyncio
import os

from fastmcp import Client
from openai import OpenAI
import dotenv

caminho_servidor = 'http://localhost:8000/sse'
cliente = Client(caminho_servidor)


async def testar_servidor(cliente, local):
    dotenv.load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    async with cliente:
        argumentos = {"local": local}
        tempo_atual = await cliente.call_tool("buscar_tempo_atual", arguments=argumentos)
        previsao_tempo = await cliente.call_tool("buscar_previsao_tempo", arguments=argumentos)

        mensagem_sistema = f"""
        Voce é um bot que faz buscas de previsão do tempo e sintetiza a resposta  
        O usuário buscou pela previsão no seguinte local: {local}. 
        Para esta busca, voce recebeu a seguinte previsão: {previsao_tempo}
        Alem disso o tempo atual é {tempo_atual} 
        Com base neste conteudo formate uma resposta amigavel ao usuário
        """
        cliente_openai = OpenAI(api_key=api_key)

        response = cliente_openai.responses.create(
            model='gpt-4o-mini',
            instructions=mensagem_sistema,
            input="Qual a previsão do tempo no local indicado?"
        )
        print(response.output_text)

if __name__ == "__main__":
    asyncio.run(testar_servidor(
        cliente=cliente,
        local='Ouro Fino')
    )