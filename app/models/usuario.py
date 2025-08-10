from . import db
from passlib.hash import bcrypt

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Uuid, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    senha_hash = db.Column(db.Text, nullable=False)
    telefone = db.Column(db.Text)
    nivel = db.Column(db.Text, default="Cooperado")
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    atualizado_em = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    def set_password(self, senha: str):
        self.senha_hash = bcrypt.hash(senha)

    def check_password(self, senha: str) -> bool:
        return bcrypt.verify(senha, self.senha_hash)
