import requests
import re
import json
from bs4 import BeautifulSoup
from unidecode import unidecode
import random

conversions = json.load(open('conversions.json'))

receita = 'arroz+branco'
lista_ingredientes = []

url = f'https://receitinhas.com.br/?s={receita}'

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4'
]

user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}

print(f"Usando User-Agent: {user_agent}")

r = requests.get(url, headers=headers)

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
    print('Requisição para a lista de receitas falhou com status:', r.status_code)

if 'href_do_item' in locals():
    requestReceita = requests.get(href_do_item, headers=headers)

    if requestReceita.status_code == 200:
        soup = BeautifulSoup(requestReceita.text, 'html.parser')

        ingredientes = soup.find('ul', class_='recipe-content__steps')
        print("Conteúdo: ", ingredientes)

        if ingredientes:
            for ingrediente in ingredientes.find_all('li'):
                texto_limpo = unidecode(ingrediente.text.replace('Check', '').replace('½', '0.5').replace('⅛', '0.12').replace('¼', '0.25').replace('¾', '0.75')).replace('\r', '').strip()
                texto_sem_parenteses = re.sub(r'\(([^)]*)\)', r'\1', texto_limpo)

                numero = texto_sem_parenteses.split(" ")
                valor_numerico = re.findall(r'\d*\.?\d+', numero[0])

                if valor_numerico:
                    quantidade = float(valor_numerico[0])

                    if numero[1] == 'xicara' or numero[1] == 'xicaras':
                        quantidade *= float(conversions['xicara']['ml'])
                    elif numero[1] == 'colher' or numero[1] == 'colheres':
                        if len(numero) > 2 and numero[2] == 'sopa':
                            quantidade *= float(conversions['colher sopa']['ml'])
                        elif len(numero) > 2 and numero[2] == 'cha':
                            quantidade *= float(conversions['colher cha']['ml'])
                    lista_ingredientes.append({"ingrediente": texto_sem_parenteses, "quantidade": quantidade})
                else:
                    lista_ingredientes.append({"ingrediente": texto_sem_parenteses, "quantidade": "a gosto"})
                    print(f"Não foi possível extrair o valor numérico de: {texto_sem_parenteses}")
        else:
            print('Lista de ingredientes não encontrada. Verifique a estrutura do HTML.')
    else:
        print('Requisição para a receita falhou com status:', requestReceita.status_code)
        print('Conteúdo da resposta:', requestReceita.text)  

body = {
    "url_do_item": href_do_item,
    "ingredientes": lista_ingredientes
}

body_json = json.dumps(body, indent=4)

print("Body JSON:")
print(body_json)
