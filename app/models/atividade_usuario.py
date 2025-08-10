from . import db

class AtividadeUsuario(db.Model):
    __tablename__ = "atividades_usuario"

    id = db.Column(db.Uuid, primary_key=True)
    usuario_id = db.Column(db.Uuid, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    titulo = db.Column(db.Text, nullable=False)
    detalhe = db.Column(db.Text)
    data_evento = db.Column(db.Date, nullable=False, server_default=db.func.current_date())
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
