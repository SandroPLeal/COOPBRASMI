from . import db

class Admin(db.Model):
    __tablename__ = "admins"
    usuario_id = db.Column(db.Uuid, db.ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    criado_em  = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    obs        = db.Column(db.Text)
