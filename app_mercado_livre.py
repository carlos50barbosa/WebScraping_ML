import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL base do Mercado Livre para produtos
base_url = 'https://lista.mercadolivre.com.br/geladeira'

# Número máximo de páginas a percorrer
max_pages = 35

# Cria uma estrutura para armazenar os dados
dic_produtos = {'Marca': [], 'Preço': []}

# Loop para percorrer as páginas
for page in range(1, max_pages + 1):
    # URL da página atual
    url = f'{base_url}_Desde_{(page - 1) * 50 + 1}'

    # Faz a requisição HTTP
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Converte o conteúdo HTML em um objeto BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontra todos os itens da lista de produtos
        produtos = soup.find_all(
            'li', class_='ui-search-layout__item shops__layout-item ui-search-layout__stack')
                
        #Lista
        # list_produtos = ['marca', 'preco']

        # Itera sobre os produto encontrados e extrai informações
        for produto in produtos:
            # Extrai o nome do produto
            name = produto.find(
                'h2', class_='ui-search-item__title').text.strip()

            # Extrai o preço do produto
            price = produto.find(
                'span', class_='andes-money-amount__fraction').text.strip()

            # Imprime as informações do produto
            print(f'Nome: {name} Preço: R$ {price}')

            dic_produtos['Marca'].append(name)
            dic_produtos['Preço'].append(price)
            
            # Cria um dicionário para armazenar informações
            # dic_produtos = {'Nome': name, 'Preço': price}

            # Adiciona informações na lista
            # list_produtos.append(dic_produtos)

    else:
        print(f'Erro ao acessar a página {page} do Mercado Livre')

df = pd.DataFrame(dic_produtos)

# Local e nome do arquivo
df.to_csv('Mercado_Livre.csv', encoding='UTF-8', sep=';')
# print(list_produtos)