from . import db

class UsuarioTipo(db.Model):
    __tablename__ = "usuario_tipos"
    usuario_id = db.Column(db.Uuid, db.ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    tipo_id    = db.Column(db.Uuid, db.ForeignKey("tipos_cooperado.id", ondelete="RESTRICT"), primary_key=True)
    criado_em  = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
