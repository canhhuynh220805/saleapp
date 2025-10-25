from flask import render_template, request

from app import app, utils


@app.route('/')
def index():
    categories = utils.get_all_cates()
    products = utils.get_all_products(kw=request.args.get("key"), category_id=request.args.get("category_id"))
    return render_template("index.html", categories=categories, products=products)

# @app.route('/products/search/', methods=['POST'])
# def search_product():
#     key = request.form.get("key")
#     products = utils.get_product_by_name(key)
#     return


if __name__ == "__main__":
    app.run(debug=True)
