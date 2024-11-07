import requests
import pandas as pd
import os
from datetime import datetime, timedelta

# Substitua 'CHAVE_API' pela sua chave de API da NASA
api_key = 'CHAVE_API'


def obter_dados_api(url):
    # Fazendo a solicitação GET para a API
    response = requests.get(url)
    # Verificando se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Convertendo a resposta para formato JSON
        data = response.json()
        # Retornando os dados
        return data
    else:
        print("Erro ao acessar a API, analise as conexões URL ou Token")

# Função para gerar as datas de outubro de 2024
def gerar_datas_outubro_2024():
    data_inicial = datetime(2024, 10, 1)
    data_final = datetime(2024, 10, 31)
    datas = []
    # Gerar as datas entre a data inicial e final
    while data_inicial <= data_final:
        datas.append(data_inicial.strftime('%Y-%m-%d'))
        data_inicial += timedelta(days=1)
    return datas

# Gerar as datas de outubro de 2024
datas_para_busca = gerar_datas_outubro_2024()

# Inicializando uma lista para armazenar os dados do rover
photo_data = []

# Para cada data coletar os dados do rover
for data in datas_para_busca:
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/Perseverance/photos?earth_date={data}&api_key={api_key}"
    print(f"Buscando dados para a data: {data}")
    dados = obter_dados_api(url)
    
    if dados and 'photos' in dados:
        for photo in dados['photos']:
            photo_data.append({
                'photo_id': photo['id'],
                'sol': photo['sol'],
                'camera_id': photo['camera']['id'],
                'camera_name': photo['camera']['name'],
                'camera_full_name': photo['camera']['full_name'],
                'img_src': photo['img_src'],
                'earth_date': photo['earth_date'],
                'rover_id': photo['rover']['id'],
                'rover_name': photo['rover']['name'],
                'rover_landing_date': photo['rover']['landing_date'],
                'rover_launch_date': photo['rover']['launch_date'],
                'rover_status': photo['rover']['status'],
            })

# Criando o DataFrame a partir da lista de dicionários
df = pd.DataFrame(photo_data)
# Exibindo o DataFrame
print(df)

# Caminho do diretório "DataFrames" dentro do projeto atual
diretorio = os.path.join(os.getcwd(), 'DataFrames')
# Criar o diretório "DataFrames" se ele não existir
os.makedirs(diretorio, exist_ok=True)
# Salvar o DataFrame em formato CSV dentro da pasta "DataFrames"
df.to_csv(os.path.join(diretorio, 'Perseverance.csv'), index=False)


# Criar o diretório principal com o nome do rover
if photo_data:
    rover_name = photo_data[0]['rover_name']
    directory = rover_name
    print(f"criando o diretorio {directory}")
    os.makedirs(directory, exist_ok=True)

    # Baixar cada uma das fotos e salvar no diretório organizado por data
    for photo in photo_data:
        data_pasta = photo['earth_date']
        data_directory = os.path.join(directory, data_pasta)
        os.makedirs(data_directory, exist_ok=True)
        print(f"criando o diretorio {data_directory}")

        img_url = photo['img_src']
        img_name = os.path.join(data_directory, f"{photo['photo_id']}.jpg")
        response = requests.get(img_url)
        if response.status_code == 200:
            with open(img_name, 'wb') as img_file:
                img_file.write(response.content)
                print(f"coletei a imagem {img_name}")
        else:
            print(f"Erro ao baixar a imagem {photo['photo_id']} da data {data_pasta}")
