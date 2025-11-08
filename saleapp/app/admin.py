from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from werkzeug.utils import redirect

from app import db, app
from app.models import Category, Product, UserRole

admin = Admin(app=app, name="App cua canh")

class AuthenticatedView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class AuthenticatedBaseView(BaseView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated
class CategoryView(AuthenticatedView):
    pass
class ProductView(AuthenticatedView):
    column_list = ['id', 'name', 'price', 'category']
    can_export = True
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name', 'price']
    create_modal = True
    column_editable_list = ['name']
    page_size = 5

class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect("/admin")

admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(LogoutView(name="Đăng xuất"))