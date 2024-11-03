from flask import Flask, request,jsonify
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
@app.route('/api/products/add', methods = ['POST'])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data['name'], price=data['price'],description=data.get('description',""))
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': "Product added sucessfully"})
    return jsonify({'message': "Invalid product data"}), 400 # codigo erro

@app.route('/api/products/delete/<int:product_id>', methods =['DELETE'])#
def delete_product(product_id):
    #recuperar o produto
    #verificar se o produto existe.
    # Se existe, apagar da dado de bases
    # Se nao existe, retornar 404
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': "Product deleted sucessfully"})
    return jsonify({'message': "Product has been not found"}), 404 # codigo erro        

@app.route("/api/products/<int:product_id>", methods =['GET'])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"Mmessage": "Product not found"}), 404


@app.route('/')
def hello_world():
    return 'Hello world'

if __name__ == "__main__":
    app.run(debug=True)

 