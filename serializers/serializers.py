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

def DecodeConteudo(conteudo) -> dict:
    return {
        "tipo": conteudo["tipo"],
        "url": conteudo.get("url"),
        "questoes": conteudo.get("questoes"),
    }

def DecodeModulo(modulo) -> dict:
    return {
        "id": str(modulo["id"]),
        "titulo": modulo["titulo"],
        "ordem": modulo["ordem"],
        "conteudos": [DecodeConteudo(c) for c in modulo.get("conteudos", [])],
    }

def DecodeCurso(curso) -> dict:
    modulos_ordenados = sorted(curso.get("modulos", []), key=lambda m: m.get("ordem", 0))
    return {
        "id": str(curso["_id"]),
        "titulo": curso["titulo"],
        "descricao": curso["descricao"],
        "imagem": curso["imagem"],
        "tags": curso.get("tags", []),
        "publicado": curso.get("publicado", False),
        "modulos": [DecodeModulo(m) for m in modulos_ordenados],
        "created_at": curso.get("created_at", ""),
        "created_by": curso.get("created_by", ""),
        "created_by_name": curso.get("created_by_name", ""),
    }

def DecodeCursos(cursos) -> list:
    return [DecodeCurso(curso) for curso in cursos]