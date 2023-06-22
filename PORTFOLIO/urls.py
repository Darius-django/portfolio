from .views import success, index, post_comments
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
    path('blog', views.blog, name='blog_without_slash'),
    # anew one path scrap.html...
    path('scrap/', my_view, name='my_view'),
    #video downloader
    path('video', views.video, name='video'),
    #chortener
    path('short/',views.short,name='short'),
    path('shorten/', views.shorten_multiple, name='shorten_multiple'),
    #quiz
    path('questions/', views.QuestionListView.as_view(), name='question-list'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz_results/', views.quiz_results, name='quiz_results'),
    #converter
    path('converter', views.converter, name='converter'),
    path('blog/converter_results/', views.converter_results, name='converter_results'),
    #email
    #path('send_email', views.send_email, name='send_email'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

