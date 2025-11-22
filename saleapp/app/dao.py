import hashlib

from app import db, app
from app.models import Category, Product, User, UserRole
import cloudinary.uploader

def get_all_cates():
    return Category.query.all()

def get_all_products(kw = None, category_id = None, page=1):
    product = Product.query

    if kw:
        product = product.filter(Product.name.contains(kw))

    if category_id:
        product = product.filter(Product.category_id == category_id)
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    product = product.slice(start, start + page_size)
    return product.all()

def get_user_by_id(id):
    return User.query.get(id)

def is_auth(username, password):
    password =  str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User.query.filter(User.username.__eq__(username), User.password.__eq__(password))

    return user.first()

def count_products():
    return Product.query.count()

def add_user(name, username, password, avatar):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    u = User(name=name, username=username, password=password)
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get("secure_url")

    db.session.add(u)
    db.session.commit()


