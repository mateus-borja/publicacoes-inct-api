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