import requests
import re
import json
from bs4 import BeautifulSoup
from unidecode import unidecode
conversions=json.load(open('conversions.json'))

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
        texto_limpo = unidecode(ingrediente.text.replace('Check', '').replace('½', '0.5').replace('⅛', '0.12').replace('¼', '0.25').replace('¾', '0.75'))
        texto_sem_parenteses = re.sub(r'\(([^)]*)\)', r'\1', texto_limpo)
        numero = texto_sem_parenteses.split(" ")
        print(numero[0])
        if(numero[1]=='xicara' or numero[1]=='xicaras'):
            quantidade = float(numero[0])*float(conversions['xicara']['ml'])
        elif(numero[1]=='colher' or numero[1]=='colheres'):
            if(numero[2]=='sopa'):
                quantidade = float(numero[0])*float(conversions['colher sopa']['ml'])
            elif(numero[2]=='cha'):
                quantidade = float(numero[0])*float(conversions['colher cha']['ml'])
        else:
            quantidade = float(numero[0])
        lista_ingredientes.append({"ingrediente": texto_sem_parenteses, "quantidade": quantidade })  # Adicionando cada ingrediente como um dicionário separado
else:
    print('Requisição falhou')


# Montando o corpo com as informações tratadas
body = {
    "url_do_item": href_do_item,
    "ingredientes": lista_ingredientes
}

# Convertendo o dicionário em JSON com formatação legível
body_json = json.dumps(body, indent=4)




print("Body JSON:")
print(body_json)
