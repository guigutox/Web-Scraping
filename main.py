import requests
from bs4 import BeautifulSoup

receita = 'arroz+branco'

url = f'https://receitinhas.com.br/?s={receita}'

r = requests.get(url)

if(r.status_code == 200):
    soup = BeautifulSoup(r.text, 'html.parser')
    link_item = soup.find('a', class_='loop__item__link')

    if link_item:
        # Obtém o valor do atributo href
        href_do_item = link_item.get('href')
        if href_do_item:
            print(f'URL do item: {href_do_item}')
        else:
            print('Atributo href não encontrado no elemento <a>')
else:
    print('Elemento <a> não encontrado com a classe "loop__item__link"')


requestReceita = requests.get(href_do_item)

if(requestReceita.status_code == 200):
    soup = BeautifulSoup(requestReceita.text, 'html.parser')
    ingredientes = soup.find('ul', class_='recipe-content__steps')
    for ingrediente in ingredientes:
        texto_limpo = ingrediente.text.replace('Check', '')
        print(texto_limpo)

else:
    print('Requisição falhou')
