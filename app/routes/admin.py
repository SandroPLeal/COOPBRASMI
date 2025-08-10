# app/routes/admin.py
from flask import Blueprint, render_template
from datetime import datetime, timedelta
import random
from app.utils.authz import admin_required


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# (opcional) mock de proteção — troque depois por login real
def login_required_mock():
    return True  # substitua por verificação de sessão/token

@admin_bp.get("/dashboard")
@admin_required
def dashboard():
    if not login_required_mock():
        # return redirect(url_for("auth.login"))
        pass

    # --- dados mock (substitua pelo banco) ---
    kpis = {
        "cooperados_total": 124,
        "operacoes_mes": 56,
        "volume_ouro_kg": 18.7,
        "pendencias_conformidade": 3,
    }

    # série semanal (últimos 7 dias)
    labels = []
    valores = []
    for i in range(6, -1, -1):
        dia = (datetime.now() - timedelta(days=i)).strftime("%d/%m")
        labels.append(dia)
        valores.append(random.randint(2, 15))

    recentes = [
        {"nome": "Maria Silva", "email": "maria@exemplo.com", "tipo": "Associado", "data": "10/08/2025"},
        {"nome": "João Almeida", "email": "joao@exemplo.com", "tipo": "Motorista", "data": "10/08/2025"},
        {"nome": "L. Mineração", "email": "contato@lmineracao.com", "tipo": "Fornecedor", "data": "09/08/2025"},
        {"nome": "Carlos Teixeira", "email": "carlos@exemplo.com", "tipo": "Associado", "data": "09/08/2025"},
    ]

    return render_template(
        "admin/dashboard.html",
        kpis=kpis,
        chart_labels=labels,
        chart_values=valores,
        recentes=recentes,
    )
