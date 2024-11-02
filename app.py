from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ecomerce.db'
db = SQLAlchemy(app)

class Product (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable=False)# parametro nao pode ser nulo
    price = db.Column(db.Float) # number
    description = db.Column(db.Text, nullable=True)# parametro pode ser vazio





#modelagem
#Produto (id, name, price, description)
# Definir uma r(ota raiz (pagina inicial) e a funcao que sera executada ao requisitar
@app.route('/')
def hello_world():
    return 'Hello world'

if __name__ == "__main__":
    app.run(debug=True)

 