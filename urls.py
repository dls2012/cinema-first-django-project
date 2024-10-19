from django.urls import path
from .views import *

urlpatterns = [
    # path('', index_view, name='main'),
    # path('category/<int:pk>/', cinema_category_view, name='category'),
    # path('cinema/<int:pk>/', cinema_detail_view, name='cinema'),
    # path('new_cinema/', add_cinema_view, name='add_cinema'),

    path('', CinemaListView.as_view(), name='main'),
    path('category/<int:pk>/', CinemaListByCategory.as_view(), name='category'),
    path('cinema/<int:pk>/', CinemaDetailView.as_view(), name='cinema'),
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('register/', register_view, name='registration'),
    path('new_cinema/', CinemaCreateView.as_view(), name='add_cinema'),
    path('cinema/<int:pk>/update/', CinemaUpdateView.as_view(), name='update'),
    path('cinema/<int:pk>/delete/', CinemaDeleteView.as_view(), name='delete'),
    path('search/', SearchResult.as_view(), name='search'),
    path('save_comment/<int:pk>/', save_comment, name='save_comment'),
    path('cinema/<int:pk>/update_comment/', CommentUpdate.as_view(), name='update_comment'),
    path('comment/<int:cinema_pk>/<int:comment_pk>/delete/', comment_delete, name='comment_delete'),
    path('profile/', profile, name='profile'),
    path('change/', edit_account_profile_view, name='change'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
    path('edit_account/', edit_account_view, name='edit_account')

]



