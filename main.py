from fastapi import FastAPI
from routes.status import entry_root
from routes.publicacao import publicacoes_root
app = FastAPI()

app.include_router(entry_root)
app.include_router(publicacoes_root)

# This is important for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)