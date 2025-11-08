import hashlib

from app.models import Category, Product, User, UserRole


def get_all_cates():
    return Category.query.all()

def get_all_products(kw = None, category_id = None):
    product = Product.query

    if kw:
        product = product.filter(Product.name.contains(kw))

    if category_id:
        product = product.filter(Product.category_id == category_id)

    return product.all()

def get_user_by_id(id):
    return User.query.get(id)

def is_auth(username, password):
    password =  str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User.query.filter(User.username.__eq__(username), User.password.__eq__(password))

    return user.first()

def count_products():
    return Product.query.count()