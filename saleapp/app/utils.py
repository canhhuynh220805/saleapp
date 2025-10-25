from app.models import Category, Product


def get_all_cates():
    return Category.query.all()

def get_all_products(kw = None, category_id = None):
    product = Product.query

    if kw:
        product = product.filter(Product.name.contains(kw))

    if category_id:
        product = product.filter(Product.category_id == category_id)

    return product.all()