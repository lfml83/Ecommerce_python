from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app=Flask(__name__)
app.config['SECRET_KEY']="minha_chave_123"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ecomerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view='login'
CORS(app)

# User (id, username, password)
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password= db.Column(db.String(80), nullable=True)


class Product (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable=False)# parametro nao pode ser nulo
    price = db.Column(db.Float) # number
    description = db.Column(db.Text, nullable=True)# parametro pode ser vazio

@login_manager.user_loader #verificar o usuario e entrar nas rotas apenas autenticado
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods =['POST'])
def login():
    data=request.json
    
    user=User.query.filter_by(username=data.get("username")).first()

    if user and data.get("password") == user.password:
            login_user(user)
            return jsonify({'message': 'logged in successfully'})
    
    return jsonify({'message': 'Unauthorized. Invalid credentials'}), 401

@app.route('/logout',methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout susscessufuly'})


#modelagem
#Produto (id, name, price, description)
# Definir uma r(ota raiz (pagina inicial) e a funcao que sera executada ao requisitar
@app.route('/api/products/add', methods = ['POST'])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data['name'], price=data['price'],description=data.get('description',""))
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': "Product added sucessfully"})
    return jsonify({'message': "Invalid product data"}), 400 # codigo erro

@app.route('/api/products/delete/<int:product_id>', methods =['DELETE'])#
@login_required
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

@app.route('/api/products/update/<int:product_id>', methods =['PUT'])#
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"Mmessage": "Product not found"}), 404
    data = request.json
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']
    db.session.commit()# para gravar no banco
    return jsonify({"message": "Product has been updated successfully"})

@app.route("/api/products", methods =['GET'])
def get_products():
    products= Product.query.all()
    product_list = []
    for product in products:
        product_data={
            "id": product.id,
            "name": product.name,
            "price": product.price,
        }
        product_list.append(product_data)
    
    
    
    return jsonify(product_list)

@app.route('/')
def hello_world():
    return 'Hello world'

if __name__ == "__main__":
    app.run(debug=True)

 