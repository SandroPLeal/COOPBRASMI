# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from uuid import uuid4
from app.models import db
from app.models.usuario import Usuario
from app.models.tipo_cooperado import TipoCooperado
from app.models.usuario_tipo import UsuarioTipo

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# GET: /auth/cadastro
@auth_bp.get("/cadastro")
def cadastro():
    fluxo = request.args.get("fluxo", "usuario")  # ex: ?fluxo=motorista
    return render_template("auth/cadastro.html", fluxo=fluxo)



@auth_bp.post("/cadastro")
def cadastro_post():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")
    telefone = request.form.get("telefone", "").strip()
    fluxo = request.form.get("fluxo", "usuario")
    tipo_slug = request.form.get("tipo_slug", "produtor").strip().lower()

    if not nome or not email or not senha:
        flash("Preencha nome, e-mail e senha.", "warning")
        return redirect(url_for("auth.cadastro", fluxo=fluxo))

    # já cadastrado?
    if Usuario.query.filter_by(email=email).first():
        flash("E-mail já cadastrado.", "warning")
        return redirect(url_for("auth.cadastro", fluxo=fluxo))

    # cria usuário
    u = Usuario(
        id=uuid4(),
        nome=nome,
        email=email,
        telefone=telefone,
    )
    u.set_password(senha)  # passlib/bcrypt
    db.session.add(u)

    # buscar tipo informado (ou padrão "produtor")
    tipo = TipoCooperado.query.filter_by(slug=tipo_slug).first()
    if not tipo:
        tipo = TipoCooperado.query.filter_by(slug="produtor").first()

    # vincular tipo ao usuário
    if tipo:
        db.session.add(UsuarioTipo(usuario_id=u.id, tipo_id=tipo.id))

    db.session.commit()

    flash("Cadastro realizado! Faça login.", "success")
    return redirect(url_for("auth.login"))


# GET: /auth/login
@auth_bp.get("/login")
def login():
    # se já logado, manda direto pro dashboard
    if session.get("uid"):
        return redirect(url_for("usuario.dashboard_usuario"))
    return render_template("auth/login.html")

# POST: /auth/login
@auth_bp.post("/login")
def login_post():
    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")

    if not email or not senha:
        flash("Informe e-mail e senha.", "warning")
        return redirect(url_for("auth.login"))

    u = Usuario.query.filter_by(email=email).first()
    if not u or not u.check_password(senha):
        flash("Credenciais inválidas.", "danger")
        return redirect(url_for("auth.login"))

    # ok: guarda sessão e redireciona
    session["uid"] = str(u.id)
    flash("Login efetuado com sucesso.", "success")
    return redirect(url_for("usuario.dashboard_usuario"))

# GET: /auth/logout
@auth_bp.get("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("home"))

# (opcional) pré-cadastro
@auth_bp.get("/pre-cadastro")
def pre_cadastro():
    return render_template("auth/pre_cadastro.html")
