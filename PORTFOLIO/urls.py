from .views import success, index, blog, post_comments
from . import views
from .views import PostDetail
from .views import my_view
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    path('', index, name='index'),
    path('success', success, name='success'),
    path('blog/', views.PostList.as_view(), name='blog'),
    path('blog/detail/<int:post_id>/', PostDetail.as_view(), name='post_detail'),
    path('post_comments/<int:post_id>/', post_comments, name='post_comments'),
    path('search', views.search, name='search'),
    # anew one path scrap.html...
    path('scrap', my_view, name='my_view'),
    #video downloader
    path('video', views.video, name='video'),
    #chortener
    path('short/',views.short,name='short'),
    path('shorten/', views.shorten_multiple, name='shorten_multiple'),
    #quiz
    path('questions/', views.QuestionListView.as_view(), name='question-list'),
    path('quiz/', views.quiz, name='quiz'),
    #converter
    path('blog/convert/', views.convert_length, name='convert_length'),
    path('converter', views.convert, name='converter'),
    path('convert', views.convert, name='convert'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
