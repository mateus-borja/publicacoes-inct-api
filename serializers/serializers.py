def DecodeArtigo(artigo) -> dict:
    return {
        "id": str(artigo["_id"]),
        "title": artigo["titulo"],
        "author": artigo["autores"], 
        "year": artigo["ano"],
        "link": artigo["link"],
        "tags": artigo.get("tags", []),
        "date": artigo.get("date", ""),
        "created_by": artigo.get("created_by", ""),
        "created_by_name": artigo.get("created_by_name", "")
    }

def DecodeArtigos(artigos) -> list:
    return [DecodeArtigo(artigo) for artigo in artigos]

def DecodeUser(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "nome": user["nome"],
        "role": user["role"]
    }

def DecodeUsers(users) -> list:
    return [DecodeUser(user) for user in users]

def DecodeNoticia(noticia) -> dict:
    return {
        "id": str(noticia["_id"]),
        "titulo": noticia["titulo"],
        "resumo": noticia["resumo"],
        "conteudo": noticia["conteudo"],
        "imagem": noticia["imagem"],
        "data": str(noticia["data"]),
        "laboratorio": noticia["laboratorio"],
        "tags": noticia.get("tags", []),
        "link": noticia["link"],
        "publicado": noticia["publicado"],
        "created_by": noticia.get("created_by", ""),
        "created_by_name": noticia.get("created_by_name", "")
    }

def DecodeNoticias(noticias) -> list:
    return [DecodeNoticia(noticia) for noticia in noticias]

def DecodeEvento(evento) -> dict:
    return {
        "id": str(evento["_id"]),
        "titulo": evento["titulo"],
        "resumo": evento["resumo"],
        "conteudo": evento["conteudo"],
        "imagem": evento["imagem"],
        "dataInicio": str(evento["dataInicio"]),
        "dataFim": str(evento["dataFim"]),
        "local": evento["local"],
        "laboratorio": evento["laboratorio"],
        "tags": evento.get("tags", []),
        "created_by": evento.get("created_by", ""),
        "created_by_name": evento.get("created_by_name", "")
    }

def DecodeEventos(eventos) -> list:
    return [DecodeEvento(evento) for evento in eventos]