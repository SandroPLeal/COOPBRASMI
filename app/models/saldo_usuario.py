from . import db

class SaldoUsuario(db.Model):
    __tablename__ = "saldo_usuario"

    usuario_id = db.Column(db.Uuid, db.ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    saldo_disponivel = db.Column(db.Numeric(14,2), nullable=False, server_default="0")
    cotas = db.Column(db.Integer, nullable=False, server_default="0")
    status_conformidade = db.Column(db.Numeric(5,4), nullable=False, server_default="0")
