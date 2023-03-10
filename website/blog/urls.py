from django.urls import path

from blog.views import HomeView, PostDetailView, AddPostView, UpdatePostView, DeletePostView, \
    CategoryView, AddCategoryView, UpdateCategoryView, DeleteCategoryView, PostsByCategory, PostsByUser, \
    search_blogs, like_post, send_email_to_staff, send_email_to_staff_success


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('add-post/', AddPostView.as_view(), name='post-add'),
    path('update-post/<slug:slug>/', UpdatePostView.as_view(), name='post-update'),
    path('delete-post/<slug:slug>/', DeletePostView.as_view(), name='post-delete'),

    path('post-search/', search_blogs, name='post-search'),
    path('user-posts/', PostsByUser.as_view(), name='user-posts'),

    path('categories/', CategoryView.as_view(), name='categories'),
    path('add-category/', AddCategoryView.as_view(), name='category-add'),
    path('update-category/<slug:slug>/', UpdateCategoryView.as_view(), name='category-update'),
    path('delete-category/<slug:slug>/', DeleteCategoryView.as_view(), name='category-delete'),
    path('category/<slug:slug>/', PostsByCategory.as_view(), name='posts-by-category'),

    path('like/<slug:slug>/', like_post, name='like-post'),

    path('email/', send_email_to_staff, name='send-email'),
    path('email-success/', send_email_to_staff_success, name='send-email-success'),
]
