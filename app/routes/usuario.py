# app/routes/usuario.py
from flask import Blueprint, render_template
from datetime import datetime, timedelta

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuario")

# TODO: trocar por verificação real de sessão/token
def current_user_mock():
    return {
        "nome": "Sandro Leal",
        "email": "sandro@coopbras.com",
        "matricula": "CBR-10294",
        "nivel": "Cooperado Ouro",
        "cotas": 12,            # qtd de cotas subscritas
        "saldo_disponivel": 34750.00,
        "status_conformidade": 0.72,  # 72% completo
    }

@usuario_bp.get("/dashboard")
def dashboard_usuario():
    u = current_user_mock()

    # KPIs simples (mock)
    kpis = {
        "min_ultimas_operacoes": 5.4,      # ouro (kg) nas últimas operações
        "documentos_pendentes": 1,
        "ordens_em_andamento": 2,
        "beneficios_disponiveis": 3,
    }

    # atividades recentes (mock)
    atividades = [
        {"data": (datetime.now()-timedelta(days=0)).strftime("%d/%m/%Y"),
         "titulo": "Subscrição de cota confirmada", "detalhe": "Cota #12 – R$ 5.000,00"},
        {"data": (datetime.now()-timedelta(days=1)).strftime("%d/%m/%Y"),
         "titulo": "Envio de documento", "detalhe": "Comprovante de endereço aprovado"},
        {"data": (datetime.now()-timedelta(days=3)).strftime("%d/%m/%Y"),
         "titulo": "Operação registrada", "detalhe": "Venda 0,35 kg – liquidação D+1"},
        {"data": (datetime.now()-timedelta(days=5)).strftime("%d/%m/%Y"),
         "titulo": "Mensagem da Coopbras", "detalhe": "Assembleia geral marcada"},
    ]

    # série simples (mock) para gráfico de saldo/valor_cotas
    series = {
        "labels": [(datetime.now()-timedelta(days=i)).strftime("%d/%m") for i in range(6,-1,-1)],
        "saldo":  [32000, 32250, 32310, 33400, 33600, 34400, 34750],
    }

    return render_template(
        "usuario/dashboard.html",
        u=u, kpis=kpis, atividades=atividades, series=series
    )
