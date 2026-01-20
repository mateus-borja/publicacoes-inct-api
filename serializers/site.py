def DecodePublicacao(publicacao) -> dict:
    return {
        "id": str(publicacao["_id"]),
        "title": publicacao["titulo"],
        "author": publicacao["autores"],
        "content": publicacao["ano"],
        "date": publicacao["link"],
        "tags": publicacao["post_img"]
    }

def DecodePublicacoes(publicacoes) -> list:
    return [DecodePublicacao(publicacao) for publicacao in publicacoes]