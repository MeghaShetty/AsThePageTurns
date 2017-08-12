from django.conf.urls import url
from . import views

app_name = 'Home'

urlpatterns = [

    url(r'^$', views.Index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^registration/$', views.UserFormView.as_view(), name='register'),
    url(r'^log_in/$', views.Log_in, name='log_in'),
    url(r'^log_out/$', views.Log_out, name='log_out'),
    url(r'^myprofile/$', views.ProfileView, name='profile'),
    url(r'^edit/$', views.UserProfileFormView, name='profileedit'),
    url(r'^category/(?P<genre>\d+)/$', views.CategoryBook, name='category'),
    url(r'^search/$', views.UserSearch, name='search'),
    url(r'^createstory/$', views.CreateStory, name='createstory'),
    url(r'^myworks/$', views.MyWorks, name='myworks'),
    url(r'^prologue/(?P<bok_id>\d+)/(?P<author>\w+)$', views.Prologue, name='prologue'),
    url(r'^profile/(?P<author>\w+)$', views.Other_User, name='other_user'),
    url(r'^read/(?P<bok_id>\d+)$', views.ReadBook, name='readbook'),
    url(r'^write/(?P<bok_id>\d+)$', views.WriteBook, name='writebook'),
    url(r'^works/(?P<author>\w+)$', views.User_Works, name='user_works'),
    url(r'^delete/(?P<bok_id>\d+)$', views.Delete, name='deletebook'),
    url(r'^community/$', views.community, name='community'),
    url(r'^detail/(?P<forum_id>\d+)$', views.detail, name='detail'),
    url(r'^create_forum/$', views.create_forum, name='create_forum'),
    url(r'^create_post/(?P<forum_id>\d+)$', views.create_post, name='create_post'),
    url(r'^(?P<bok_id>\d+)$', views.Addtopc, name='add'),
    url(r'^mycollection/', views.MyCollection, name='mycollection'),
    url(r'^publish/(?P<bok_id>\d+)$', views.Publish, name='publish'),
    url(r'^unpublish/(?P<bok_id>\d+)$', views.UnPublish, name='unpublish'),
    url(r'^like/(?P<bok_id>\d+)$', views.Like, name='like'),
    url(r'^unlike/(?P<bok_id>\d+)$', views.UnLike, name='unlike'),
    url(r'^likedbooks/', views.MyLikes, name='likedbooks'),
    url(r'^bookmark/(?P<bok_id>\d+)/(?P<chapter_no>\d+)$', views.Book_Mark, name='bookmark'),
    url(r'^gotostart/(?P<bok_id>\d+)$', views.GoToStart, name='gtstart'),
    url(r'^remove/(?P<bok_id>\d+)$', views.RemoveFromPC, name='removefrompc'),
    url(r'^deletepost/(?P<post_id>\d+)/(?P<forum_id>\d+)$', views.DelPost, name='delpost'),
    url(r'^deleteforum/(?P<forum_id>\d+)$', views.DelForum, name='delforum'),
    url(r'^termsofprivacy/$', views.TermsOfPrivacy, name='termspri'),
    url(r'^aboutdevelopers/$', views.AboutUs, name='aboutus'),
]