import scrapy

# Exercício:
# Buscar:
# Nome, ID, Tamanho e Peso
# Alguns dados estão dentro da página do Pokemon
# Página do Pokémon deve usar o parser "parser_pokemon"

# Dica: Principais CSS Selectors:
# https://www.w3schools.com/cssref/css_selectors.php

class PokeSpider(scrapy.Spider):
    name = 'pokespider'
    start_urls = ['https://pokemondb.net/pokedex/all']

    def parse(self, response):
        linha = response.css('table#pokedex > tbody > tr:first-child')
        link = linha.css("td:nth-child(2) > a::attr(href)")
        yield response.follow(link.get(), self.parser_pokemon)

    def parser_pokemon(self, response):
        nome = response.css('h1::text').get()
        id = response.css('table.vitals-table > tbody > tr:nth-child(1) > td > strong::text').get()
        tamanho = response.css('table.vitals-table > tbody > tr:nth-child(4) > td::text').get()
        peso = response.css('table.vitals-table > tbody > tr:nth-child(5) > td::text').get()
        url_pokemon = response.url
        tipos = response.css('table.vitals-table tbody tr:nth-child(2) td a::text').getall()[:2]
        evolucoes = []
        evolucoes_possiveis = response.css('#main div.infocard-list-evo div span.infocard-lg-data.text-muted')
        
        for evolucao in evolucoes_possiveis:
            nome_evolucao = evolucao.css('a::text').get()
            id_evolucao = evolucao.css('small:nth-child(1)::text').get()
            url_evolucao = evolucao.css('a::attr(href)').get()
            url_evolucao_completinha = f'https://pokemondb.net{url_evolucao}'
          
            evolucoes.append({
                "nome_evolucao": nome_evolucao,
                "id_evolucao": id_evolucao,
                "url_evolucao": url_evolucao_completinha
            })
          
        yield {
            "nome": nome,
            "id": id,
            "tamanho": tamanho,
            "peso": peso,
            "url_pokemon": url_pokemon,
            "tipos": tipos,
            "evolucoes": evolucoes,
        }




#yield {"nome": nome.get()}


# class PokeSpider(scrapy.Spider):
#   name = 'pokespider'
#   start_urls = ['https://pokemondb.net/pokedex/all']

#   def parse(self, response):
#     ### tabela de seletores de CSS
#     tabela_pokedex = "table#pokedex > tbody > tr"

#     linhas = response.css(tabela_pokedex)

#     # Processa uma linha apenas
#     linha = linhas[0]
#     coluna_href = linha.css("td:nth-child(2) > a::attr(href)")
#     yield response.follow(coluna_href.get(), self.parser_pokemon)

#     # Processa todas as linhas
#     for linha in linhas:
#       # coluna_nome = linha.css("td:nth-child(2) > a::text")
#       # coluna_id = linha.css("td:nth-child(1) > span.infocard-cell-data::text")
#       #yield {'id': coluna_id.get(),'nome': coluna_nome.get()}

#       coluna_href = linha.css("td:nth-child(2) > a::attr(href)")
#       yield response.follow(coluna_href.get(), self.parser_pokemon)

#   def parser_pokemon(self, response):
#     id_selector = "table.vitals-table > tbody > tr:nth-child(1) > td > strong::text"
    
#     id = response.css(id_selector)
#     yield {'id': id.get()}
    