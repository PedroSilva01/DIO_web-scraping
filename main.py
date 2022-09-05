import requests
from bs4 import BeautifulSoup
import json


#REALIZANDO WEB SCRAPING NO SITE DA ROCKETSEAT
res = requests.get("https://blog.rocketseat.com.br/?")
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, 'html.parser') #pega o que veio de res e ta dando um parser nele
#para que todo o conteudo do res seja transformado em objeto html
# print(res) #vai mostrar o estado do request que foi realizado no site 
# print(res.text) # vai pegar todo o html da pagina, formatado no utf-8, mas alguns caracteres podem ficar bagunçados
# print(soup)

#       INICIANDO A FAZER O SCRAPING    
#o beautifulsoup vai pegar cada item com a classe post e transformar em um array

posts = soup.find_all(class_="post") #transformou cada item com a class post em uma array
# print(posts[0])

#E AGR COLOCAREMOS TODOS OS ARTIGOS DENTRO DE UM DICIONARIO DO PYTHON, PARA DEPOSI TRANFORMAR EM UM ARQUIVO JSON OU CSV PARA TRATAR E COLOCAR NO BANCO DE DADOS

all_posts = []
for post in posts:
    # print(post.find('h2').text) # vai buscar o texto que tem dentro da tag h2, que no caso é os titulos de cada artigo do blog
    info = post.find(class_='m-article-card__info')
    title = info.h2.text #tratando as tags do html como objeto
    # print(title.capitalize())
    categoria_name = info.a.text
    # print(categoria_name.capitalize())


    add_time_info = info.find(class_='m-article-card__timestamp')
    time_info_list = info.find_all('span') #como no arquivo só tem 3 json fica mais facil. além de que colocou os 3 em uma lista indexavel
    date = time_info_list[0].text
    read_time = time_info_list[2].text


    author = post.find(class_='m-article-card__author')
    name_author = author['aria-label'] #ASSIM QUE PEGA O ATRIBUTO DE UMA TAG
    img = post.find(class_='m-article-card__picture')
    image = img.find(class_='m-article-card__picture-background')
    link_image = image['src']
    # print(link_image)
    all_posts.append({
        'title': title, 
        'category': categoria_name, 
        'author': name_author,
        'reading_time': read_time,
        'date': date,
        'img': link_image,
        })

# print(all_posts)

# AGORA TRANSFORMANDO ESSES DADOS PARA JSON
#empurrou todos os dados do all_posts para um json_file
with open('posts.json', 'w') as json_file: 
    json.dump(all_posts, json_file, indent=3, ensure_ascii=False) #o indent=3 serve para organizar melhor o arquivo json


#       AGORA PARA TRATAR ALGUNS ERROS DO JSON, COMO DIGITOS TROCADOS
#USA-SE O ENSURE_ASCI=False NO CODIGO DO JSON.DUMP

