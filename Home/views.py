from django.http import Http404, HttpResponse
from django.template import loader,RequestContext
from django.shortcuts import render, redirect,render_to_response,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, UserProfileForm, ChapterForm
from .models import UserProfile,Book,Genre,PersonalCollection,Chapter,Thread,Forum,LikedBook
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.utils.translation import ugettext_lazy as _


def Index(request):
    return render(request,'Home/index.html',{})

def home(request):
    book = Book.objects.all()
    gen = Genre.objects.all()
    return render(request,'Home/home.html',{'book':book, 'gen':gen})


class UserFormView(View):
    form_class = UserForm
    template_name = 'Home/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        eml = request.POST.get('email', '')
        domain = eml.split('@')[1]
        domain_list = ["gmail.com", "yahoo.com", "hotmail.com", "rediff.com", "gmail.in", "yahoo.in", "hotmail.co.in",
                       "rediff.co.in"]
        if domain not in domain_list:
            return render(request, 'Home/register.html', {'error_message': 'Invalid Email Domain'})
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.password1 = form.cleaned_data['password1']
            user.email = form.cleaned_data['email']
            user.set_password(user.password1)
            user.save()
            return redirect('Home:log_in')
        return render(request, self.template_name, {'form': form})


def Log_in(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('Home:home')
            else:
                return render(request, 'Home/log_in.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'Home/log_in.html', {'error_message': 'Invalid Login Details Supplied'})
    else:
        return render_to_response('Home/log_in.html', {}, context)


def Log_out(request):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        logout(request)
        return redirect('Home:home')


def ProfileView(request):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        try:
            upro = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return render(request, 'Home/profile.html', {})
        return render(request, 'Home/profile.html', {'profiles': upro})


def UserProfileFormView(request):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        form = UserProfileForm(request.POST or None, request.FILES)
        if UserProfile.objects.filter(user=request.user).exists():
            UserProfile.objects.get(user=request.user).delete()
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('Home:profile')
        context = {
            "form":form
        }
        return render(request,"Home/profileedit.html",context)


def CategoryBook(request,genre):
    book = Book.objects.filter(genre=genre)
    gen = Genre.objects.all()
    return render(request, 'Home/displaybooks.html', {'book': book, 'gen': gen})


def UserSearch(request):
    if request.method == 'GET':
        search_query = request.GET.get('searchbox',None)
    profile = UserProfile.objects.filter(user__username__icontains=search_query)
    book = Book.objects.filter(author__username__icontains=search_query)
    book1 = Book.objects.filter(title__icontains=search_query)
    gen = Genre.objects.all()

    return render(request, 'Home/search.html', {'book': book, 'gen': gen,'profile':profile,'book1':book1})


def CreateStory(request):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        gen = Genre.objects.all()
        if request.method == 'POST':
            book = Book()
            book.author = request.user
            book.title = request.POST.get('title','')
            book.coverpage = request.FILES['coverpage']
            book.genre = request.POST.get('genr','')
            book.prologue = request.POST.get('prologue', '')
            book.save()
            return redirect('Home:myworks')
        else:
            return render(request,'Home/createstory.html', {'gen':gen})


def MyWorks(request):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        gen = Genre.objects.all()
        upro = Book.objects.filter(author=request.user)
        author = request.user
        return render(request, 'Home/myworks.html', {'userr': upro, 'gen':gen,'author':author})


def User_Works(request,author):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        gen = Genre.objects.all()
        upro = Book.objects.filter(author__username=author)
        author = User.objects.get(username=author)
        return render(request, 'Home/user_works.html', {'userr': upro, 'gen':gen,'author':author})


def Other_User(request, author):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        upro = UserProfile.objects.get(user__username=author)
        userr = request.user
        if author == userr.username:
            return redirect('Home:profile')
        auth = User.objects.get(username=author)
        return render(request, 'Home/other_user.html', {'profiles': upro ,'author': auth})


def ReadBook(request, bok_id):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        if PersonalCollection.objects.filter(id_book=bok_id).filter(user_coll=request.user).exists():
            bk = PersonalCollection.objects.filter(user_coll=request.user).get(id_book=bok_id)
            if bk.bookmark:
                bm_no = bk.bookmark_no
                chap = Chapter.objects.filter(b_id=bok_id).filter(chapter_no__gte=bm_no).order_by('chapter_no')
            else:
                chap = Chapter.objects.filter(b_id=bok_id).order_by('chapter_no')
        else:
            chap = Chapter.objects.filter(b_id=bok_id).order_by('chapter_no')
        paginator = Paginator(chap, 1)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            obj = paginator.page(page)
        except (EmptyPage, InvalidPage):
            obj = paginator.page(paginator.num_pages)
        book = Book.objects.get(bok_id=bok_id)
        return render(request, 'Home/readbook.html', {'ch': chap, 'obj': obj,'book':book})


def WriteBook(request,bok_id):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        form = ChapterForm(request.POST or None)
        book = Book.objects.get(bok_id=bok_id)
        if form.is_valid():
            chapter_no = request.POST.get('chapter_no','')
            if Chapter.objects.filter(b_id = bok_id).filter(chapter_no = chapter_no).exists():
                    chapter_title = request.POST.get('chapter_title', '')
                    chapter_content = request.POST.get('chapter_content', '')
                    chapter_no = request.POST.get('chapter_no', '')
                    Chapter.objects.filter(b_id=bok_id).filter(chapter_no=chapter_no).update(chapter_title=chapter_title)
                    Chapter.objects.filter(b_id=bok_id).filter(chapter_no=chapter_no).update(chapter_content=chapter_content)
                    return redirect('Home:prologue', bok_id=bok_id, author=book.author)
            else:
                    chap = Chapter.objects.filter(b_id = bok_id)
                    ch = form.save(commit=False)
                    ch.b_id = Book.objects.get(bok_id=bok_id)
                    ch.save()
                    return redirect('Home:prologue', bok_id=bok_id, author=book.author)
        context = {
            "form":form,
            "book":book
        }
        return render(request,"Home/writebook.html",context)

def Delete(request,bok_id):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        Book.objects.get(bok_id=bok_id).delete()
        return redirect('Home:myworks')


def community(request):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        forums = Forum.objects.all()
        threads = Thread.objects.all()
        return render(request, 'Home/community.html', {'forums': forums, 'threads': threads})


def detail(request, forum_id):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        forum = get_object_or_404(Forum,forum_id=forum_id)
        thread = Thread.objects.all()
        return render(request, 'Home/detail.html', {'forum': forum, 'thread': thread})


def create_forum(request):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        thread = Thread.objects.all()
        if request.method == 'POST':
            forum = Forum()
            user = request.user
            forum.user_name = user.username
            forum.topic = request.POST.get('topic','')
            forum.content = request.POST.get('content','')
            forum.save()
            return render(request, 'Home/detail.html', {'forum': forum, 'thread':thread})
        return render(request, 'Home/create_forum.html', {})


def create_post(request, forum_id):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        if request.method == 'POST':
            forum = get_object_or_404(Forum, forum_id=forum_id)
            thread = Thread()
            thread.forum_no = forum
            thread.timestamp = timezone.now()
            user = request.user
            thread.user_name = user.username
            thread.post = request.POST.get('posts', '' )
            thread.save()
            return redirect( 'Home:detail',forum_id=forum_id)

        return render(request, 'Home/create_post.html', {})


def Addtopc(request,bok_id):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        if PersonalCollection.objects.filter(id_book=bok_id).filter(user_coll=request.user).exists():
            book = Book.objects.get(bok_id=bok_id)
            return redirect('Home:prologue',bok_id=bok_id,author=book.author)
        else:
            bk = PersonalCollection()
            book = Book.objects.get(bok_id=bok_id)
            bk.id_book = book
            bk.user_coll = request.user
            bk.bookmark = False
            bk.bookmark_no = 1
            bk.save()
            return redirect('Home:prologue',bok_id=bok_id,author=book.author)


def MyCollection(request):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        pc = PersonalCollection.objects.filter(user_coll=request.user)
        gen = Genre.objects.all()
        return render(request,'Home/mycollection.html',{'pc':pc,'gen':gen})


def Publish(request,bok_id):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        book = Book.objects.filter(bok_id=bok_id).update(publish=True)
        return redirect('Home:myworks')


def UnPublish(request,bok_id):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        book = Book.objects.filter(bok_id=bok_id).update(publish=False)
        return redirect('Home:myworks')

def Like(request,bok_id):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        book = Book.objects.get(bok_id=bok_id)
        book.no_of_likes = book.no_of_likes + 1
        book.save()
        addlike = LikedBook()
        addlike.user = request.user
        addlike.book = book
        addlike.save()
        return redirect('Home:prologue', bok_id=bok_id, author=book.author)


def UnLike(request,bok_id):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        book = Book.objects.get(bok_id=bok_id)
        book.no_of_likes = book.no_of_likes - 1
        book.save()
        LikedBook.objects.filter(book=book).filter(user=request.user).delete()
        return redirect('Home:prologue', bok_id=bok_id, author=book.author)


def Prologue(request,bok_id, author):
    book = Book.objects.get(bok_id=bok_id)
    userr = User.objects.get(username=author)
    gen = Genre.objects.all()
    if request.user.is_authenticated():
        pc = PersonalCollection.objects.filter(id_book=bok_id).filter(user_coll=request.user)
        lik = LikedBook.objects.filter(user=request.user).filter(book=book)
        if lik:
            liked = True
        else:
            liked = False
        return render(request, 'Home/prologue.html',{'book': book, 'gen': gen, 'userr': userr, 'pc': pc, 'liked': liked,'author':author})
    else:
        return render(request, 'Home/prologue.html', {'book': book, 'gen': gen, 'userr': userr,'author':author})




def MyLikes(request):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        lb = LikedBook.objects.filter(user=request.user)
        gen = Genre.objects.all()
        return render(request, 'Home/mylikes.html', {'lb':lb,'gen':gen})


def Book_Mark(request,bok_id,chapter_no):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        if PersonalCollection.objects.filter(id_book=bok_id).filter(user_coll=request.user).exists():
            bk = PersonalCollection.objects.filter(user_coll=request.user).filter(id_book=bok_id).update(bookmark=True)
            bk = PersonalCollection.objects.filter(user_coll=request.user).filter(id_book=bok_id).update(bookmark_no=chapter_no)
        else:
            bk = PersonalCollection()
            book = Book.objects.get(bok_id=bok_id)
            bk.id_book = book
            bk.user_coll = request.user
            bk.bookmark = True
            bk.bookmark_no = chapter_no
            bk.save()
        return redirect('Home:mycollection')


def GoToStart(request,bok_id):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        book = PersonalCollection.objects.filter(id_book=bok_id).filter(user_coll=request.user).update(bookmark=False)
        book = PersonalCollection.objects.filter(id_book=bok_id).filter(user_coll=request.user).update(bookmark_no=1)
        return redirect('Home:readbook',bok_id=bok_id)


def RemoveFromPC(request,bok_id):
    if not request.user.is_authenticated():
        return redirect('Home:log_in')
    else:
        PersonalCollection.objects.filter(user_coll=request.user).filter(id_book=bok_id).delete()
        return redirect('Home:mycollection')

def DelPost(request,post_id,forum_id):
    Thread.objects.get(pk=post_id).delete()
    return redirect('Home:detail',forum_id=forum_id)


def DelForum(request,forum_id):
    Forum.objects.get(forum_id=forum_id).delete()
    return redirect('Home:community')

def TermsOfPrivacy(request):
    return render(request,'Home/termspri.html',{})

def AboutUs(request):
    return render(request,'Home/aboutus.html',{})