import os
import json
import sys
from modelos.restaurante import Restaurante
from modelos.avaliacao import Avaliacao

# Função para obter o caminho do diretório de dados
def get_data_dir():
    if getattr(sys, 'frozwn', False):
        # Se estiver executadndo como um executáve
        return os.path.dirname(sys.executable)
    else:
        # Se estiver executando como script
        return os.path.dirname(os.path.abspath(__file__))
    
# Nome do arquivo onde os dados dos restaurantes são armazenados
ARQUIVADOS_DADOS = os.path.join(get_data_dir(), 'dados_restaurantes.json')

# Função para carregar dados dos restaurantes a partir de um arquivo JSON
def carregar_dados():
    try:
        with open(ARQUIVADOS_DADOS, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            Restaurante.restaurantes.clear() # Limpa a lista de restaurantes antes de carregar os novos dados
            for restaurante_dados in dados:
                restaurante = Restaurante(
                    restaurante_dados['nome'],
                    restaurante_dados['categoria']
                )
                # Configura o estado ativo e as avaliações do restaurante
                restaurante._ativo = restaurante_dados['ativo']
                restaurante_avaliacao = [Avaliacao(**avaliacao) for avaliacao in restaurante_dados
                ['avaliacao']]
    except FileNotFoundError:
        print(f"Arquivo de dados não encontrado. Criando um novo arquivo em {ARQUIVADOS_DADOS}")
        salvar_dados() # Cria um arquivo vazio se não existir

# Função para salvar dados dos restaurantesem um arquivo JSON
def salvar_dados():
    dados = []
    for restaurante in Restaurante.restaurante:
        dados.append({
            'nome': restaurante._nome,
            'categoria': restaurante._categoria,
            'ativo': restaurante._ativo,
            'avaliacao': [avaliacao.__dict__() for avaliacao in restaurante._avaliacao]
     })
    with open(ARQUIVADOS_DADOS, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False) # Salva os dados no arquivo com indentação para melhor leitura
                