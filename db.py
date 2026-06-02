from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Piece(db.Model):
    __tablename__="wardrobe"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String, nullable=False) #nulllable=false means that this every item needs to have a  label
    color = db.Column(db.String, nullable=True)
    image=db.Column(db.String, nullable=False)
    






