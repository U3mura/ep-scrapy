import scrapy

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

        habilidades_links = response.css('table.vitals-table tbody tr:nth-child(6) td a::attr(href)').getall()

        for habilidade_link in habilidades_links:
            habilidade_url_completa = f'https://pokemondb.net{habilidade_link}'
            yield response.follow(habilidade_url_completa, self.parse_habilidade)
        
        yield {
            "nome": nome,
            "id": id,
            "tamanho": tamanho,
            "peso": peso,
            "url_pokemon": url_pokemon,
            "tipos": tipos,
            "evolucoes": evolucoes,
        }

    def parse_habilidade(self, response):
        habilidade_nome = response.css('h1::text').get()
        
        habilidade_descricao = ' '.join(response.css('#main > div.grid-row > div:nth-child(1) > p *::text').getall())
        
        habilidade_descricao = ' '.join(habilidade_descricao.split())
        
        habilidade_url = response.url

        yield {
            "nome_habilidade": habilidade_nome,
            "descricao": habilidade_descricao.strip(),
            "url_habilidade": habilidade_url
        }