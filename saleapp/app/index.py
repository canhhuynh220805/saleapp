import math

from flask import render_template, request, session, jsonify
from flask_login import login_user, logout_user
from werkzeug.utils import redirect

from app import app, dao, login, utils
from app.models import User


@app.route('/')
def index():
    page = request.args.get('page', 1)
    products = dao.get_all_products(kw=request.args.get("key"), category_id=request.args.get("category_id"))
    page_size = app.config["PAGE_SIZE"]
    total = dao.count_products()
    return render_template("index.html", products=products, pages=math.ceil(total / page_size))


@app.route('/login')
def login_view():
    return render_template('login.html')


@app.route('/register')
def register_view():
    return render_template('register.html')


@app.route('/cart')
def cart_view():
    return render_template('cart.html')

@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')


@app.route('/login', methods=['POST'])
def login_process():
    username = request.form.get("username")
    password = request.form.get("password")

    user = dao.is_auth(username=username, password=password)
    if user:
        login_user(user=user)
    next = request.args.get("next")
    return redirect(next if next else "/")


@app.route('/register', methods=['POST'])
def register_process():
    password = request.form.get('password')
    confirm = request.form.get('confirm')
    if password != confirm:
        err_msg = 'Mật khẩu không khớp'
        return render_template('register.html', err_msg=err_msg)
    avatar = request.files.get('avt')
    try:
        return dao.add_user(name=request.form.get('name'), username=request.form.get('username'), password=request.form.get('password'),
                       avatar=avatar)
    except Exception as e:
        print(e)
        return render_template('register.html', err_msg='Hệ thống có lỗi')


@app.route('/api/carts', methods=['POST'])
def add_to_cart():
    cart = session.get('cart')
    if not cart:
        cart={}

    id = str(request.json.get('id'))
    name = request.json.get('name')
    price = request.json.get('price')

    if id in cart:
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart

    print(cart)
    return jsonify(utils.stats_cart(cart))

@app.context_processor
def common_response():
    return {
        'categories': dao.get_all_cates(),
        'cart_stats': utils.stats_cart(session.get('cart'))
    }

@login.user_loader
def load_user(id):
    return dao.get_user_by_id(id)


if __name__ == "__main__":
    from app import admin

    app.run(debug=True)
