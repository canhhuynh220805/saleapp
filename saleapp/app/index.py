import math

from flask import render_template, request
from flask_login import login_user
from werkzeug.utils import redirect

from app import app, utils, login
from app.models import User


@app.route('/')
def index():
    categories = utils.get_all_cates()
    products = utils.get_all_products(kw=request.args.get("key"), category_id=request.args.get("category_id"))
    page_size = app.config["PAGE_SIZE"]
    total = utils.count_products()
    return render_template("index.html", categories=categories, products=products, pages=math.ceil(total/page_size))

@app.route('/login', methods=['GET','POST'])
def login_process():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = utils.is_auth(username=username, password=password)
        if user:
            login_user(user=user)
        next = request.args.get("next")
        return redirect(next if next else "/")

    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register_process():
    pass

@login.user_loader
def load_user(id):
    return utils.get_user_by_id(id)

if __name__ == "__main__":
    from app import admin
    app.run(debug=True)
