from flask import Flask, render_template
from dotenv import load_dotenv
import os
from datetime import datetime

# --- carga de variáveis de ambiente ---
load_dotenv()

# --- app Flask ---
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")

# Banco (Supabase Postgres via SQLAlchemy) — só mapeando, sem create_all()
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")  # ex: postgresql+psycopg://postgres:...@db....supabase.co:5432/postgres
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # <- key correta

# Models (apenas mapeamento)
from app.models import db  # precisa existir app/models/__init__.py com: db = SQLAlchemy()
db.init_app(app)

# --- blueprints básicos ---
from app.routes.auth import auth_bp
from app.routes.usuario import usuario_bp

app.register_blueprint(auth_bp)
app.register_blueprint(usuario_bp)

# --- Admin só em ambientes autorizados ---
if os.getenv("ADMIN_UI") == "1":
    # Import tardio pra nem carregar o módulo em produção
    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

# --- contexto global (jinja) ---
@app.context_processor
def inject_globals():
    return {
        "now": datetime.now,
        "nome_cooperativa": os.getenv("NOME_COOPERATIVA", "COOPBRASMI – Cooperativa de Ouro do Brasil"),
        "cnpj": os.getenv("CNPJ", "00.000.000/0000-00"),
        "cidade_estado": os.getenv("CIDADE_ESTADO", "Marabá‑PA"),
        "csrf_token": lambda: "",  # fallback até habilitar CSRF real
    }

# --- rotas básicas ---
@app.route("/")
def home():
    return render_template("home.html")

@app.get("/health")
def health():
    return {"status": "ok"}

# --- entrada ---
if __name__ == "__main__":
    app.run(debug=True)
