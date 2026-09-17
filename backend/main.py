from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import ensure_indexes
from routers import auth, expenses, categories, insights

app = FastAPI(title="Expense Intelligence System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(categories.router)
app.include_router(insights.router)


@app.on_event("startup")
async def startup():
    await ensure_indexes()


@app.get("/")
def home():
    return {"message": "Expense Intelligence System API is running"}
