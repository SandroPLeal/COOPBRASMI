from . import db

class TipoCooperado(db.Model):
    __tablename__ = "tipos_cooperado"
    id = db.Column(db.Uuid, primary_key=True)
    slug = db.Column(db.Text, unique=True, nullable=False)
    nome = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.Integer, nullable=False, server_default="100")
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
