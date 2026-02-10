from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.status import entry_root
from routes.publicacao import publicacoes_root

app = FastAPI()

# Configurar CORS
allowed_origins = [
    "http://localhost:5173",                        # Vite desenvolvimento
    "https://joaocruzs.github.io",       # GitHub Pages produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(entry_root)
app.include_router(publicacoes_root)


# This is important for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)