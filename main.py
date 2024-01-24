import requests
import re
import json
from bs4 import BeautifulSoup
from unidecode import unidecode

receita = 'arroz+branco'
lista_ingredientes = []

url = f'https://receitinhas.com.br/?s={receita}'

r = requests.get(url)

if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')
    link_item = soup.find('a', class_='loop__item__link')

    if link_item:
        href_do_item = link_item.get('href')
        if href_do_item:
            print(f'URL do item: {href_do_item}')
        else:
            print('Atributo href não encontrado no elemento <a>')
else:
    print('Elemento <a> não encontrado com a classe "loop__item__link"')

requestReceita = requests.get(href_do_item)

if requestReceita.status_code == 200:
    soup = BeautifulSoup(requestReceita.text, 'html.parser')
    ingredientes = soup.find('ul', class_='recipe-content__steps')
    for ingrediente in ingredientes.find_all('li'):  # Iterar sobre cada item da lista
        texto_limpo = unidecode(ingrediente.text.replace('Check', '').replace('½', '0,5'))
        texto_sem_parenteses = re.sub(r'\([^)]*\)', '', texto_limpo)
        lista_ingredientes.append(texto_sem_parenteses)
else:
    print('Requisição falhou')

for x in lista_ingredientes:
    print(x)

saida = json.dumps(lista_ingredientes)
print("Lista convertida: ", saida)
