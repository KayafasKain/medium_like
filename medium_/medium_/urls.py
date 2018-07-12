"""medium_ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from auth_app import views as auth_views
from auth_app import views_api as auth_views_api
from post_app import views as post_views
from post_app import views_api as post_views_api
from profile_app import views as profile_views
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from rest_framework.authtoken import views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='My API')


router = DefaultRouter()
router.register(r'categories', post_views_api.CategoryViewSet)
router.register(r'statuses', post_views_api.StatusViewSet)
router.register(r'posts', post_views_api.PostViewSet)
router.register(r'users', auth_views_api.UserViewSet)



LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
#edit_profile
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', post_views.article_post_list, name='article-list'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('create_profile/<str:pk>', auth_views.create_profile, name='register-profile'),
    path('register/', auth_views.register, name='register'),
    path('oauth', include('social_django.urls', namespace='social')),
    path('own_article_list/', login_required(post_views.own_article_post_list), name='own-article-list'),
    path('show_article/<str:pk>', post_views.show_single_article, name='show-article'),
    path('create_article/', login_required(post_views.create_article), name='article-create'),
    path('edit_article/<str:pk>', login_required(post_views.edit_article), name='article-edit'),
    path('edit_profile/', login_required(profile_views.edit_profile), name='edit-profile'),
    path('change_password/', login_required(profile_views.change_password), name='ch-password'),
    path('verify_code/<str:pk>', auth_views.verify_view, name='verify-code'),
    url(r'api/api-token-auth', views.obtain_auth_token),
    url(r'api/', include(router.urls)),
    url(r'api/map/', schema_view),

    # path('api/users/', auth_views_api.user_list, name='api-user-list'),
    # path('api/posts/', post_views_api.post_view, name='api-post'),
    # path('api/posts/<str:pk>', post_views_api.post_view, name='api-post'),
    # path('api/posts/categories/', post_views_api.category_view, name='api-category'),
    # path('api/posts/statuses/', post_views_api.status_view, name='api-status'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
