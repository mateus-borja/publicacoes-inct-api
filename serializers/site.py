def DecodeArtigo(artigo) -> dict:
    return {
        "id": str(artigo["_id"]),
        "title": artigo["titulo"],
        "author": artigo["autores"],
        "content": artigo["ano"],
        "date": artigo["link"],
        "tags": artigo["post_img"]
    }

def DecodeArtigos(artigos) -> list:
    return [DecodeArtigo(artigo) for artigo in artigos]