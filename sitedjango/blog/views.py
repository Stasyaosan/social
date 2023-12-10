from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from blog.models import *
from blog.forms import *
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
import json

from itertools import groupby
from collections import Counter

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        mesg = ContactMessage()
        mesg.name = name
        mesg.email = email
        mesg.message = message
        mesg.save()
        request.session['a'] = 'Фома успешно отправленна'
        return redirect('/contact')
    else:
        suc = ''
        if 'a' in request.session:
            suc = request.session['a']
        form = ContactForm()

    return render(request, 'contact.html', context={'form': form, 'suc': suc})

def index(request):
    data = ''
    if 'login' in request.session:
        loginsession = request.session['login']
        data = User.objects.filter(login=loginsession).first()
        # user = User.objects.filter(id=data.id).first()

    news = News.objects.all()
    context = {
        'news': news,
        'user': data
    }
    return render(request, 'index.html', context=context)


def contacts(request):
    contacts = Contact.objects.all()
    context = {
        'contacts': contacts
    }
    return render(request, 'contacts.html', context=context)


def articles(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            articles = Article.objects.filter(title=query)
            print(articles)
        else:
            articles = Article.objects.all()
    else:
        form = SearchForm()
        articles = Article.objects.all()
    art_new = []
    for article in articles:
        art_new.append({
            'title': article.title,
            'description': article.description,
            'img': str(article.img)[5:],
            'id': article.id,
            'category': article.cat.title,
            'user': article.user,
            'date': article.date
        })

    context = {
        'articles': art_new,
        'form': form
    }
    return render(request, 'articles.html', context=context)


def articlesid(request, id):
    if request.method == 'POST':
        name = request.POST['name']
        comment = request.POST['comment']
        di = Article.objects.filter(id=id).first()
        com = Comentary()
        com.name = name
        com.title = comment
        com.article = di
        com.save()
    article = Article.objects.filter(id=id).first()
    article_new = {
        'title': article.title,
        'description': article.description,
        'img': str(article.img)[5:],
        'id': article.id,
        'category': article.cat.title,
        'fulltext': article.fulltext
    }
    comentary = Comentary.objects.filter(article=id).order_by('-date')
    context = {
        'article': article_new,
        'comentary': comentary
    }
    return render(request, 'articledetail.html', context=context)


def reg(request):
    errors = ''
    suc = ''
    if request.method == 'POST':
        name = request.POST['name']
        login = request.POST['login']
        email = request.POST['email']
        city = request.POST['city']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
        if (password_repeat == password) and (not User.objects.filter(login=login).exists()):
            user = User()
            user.name = name
            user.login = login
            user.email = email
            user.city = city
            user.password = password
            user.save()
            suc = 'Вы зарегистрировались'
        else:
            errors += 'Пароли не совпадают или такой пользователь под логином ' + login + ' уже зарегистрирован'
    context = {
        'errors': errors,
        'suc': suc
    }

    return render(request, 'reg.html', context=context)


def auth(request):
    errors = ''
    suc = ''
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        if User.objects.filter(login=login).exists() and User.objects.filter(password=password).exists():
            request.session['login'] = login
            suc += 'Вы авторизовались'
            return redirect('/panel')
        else:
            errors += 'Неправильный пароль или логин, либо такой пользователь не зарегистрирован'
    context = {
        'suc': suc,
        'errors': errors
    }
    return render(request, 'auth.html', context=context)

def panel(request):
    if 'login' in request.session:
        loginsession = request.session['login']
        data = User.objects.filter(login=loginsession).first()
        if request.method == 'POST':
            name = request.POST['name']
            login = request.POST['login']
            email = request.POST['email']
            password = request.POST['password']
            print(name, login, email, password)
            user = User.objects.filter(id=data.id).first()
            user.name = name
            user.login = login
            user.email = email
            user.password = password
            user.save()
            return redirect('/panel')

        context = {
            'data': data
        }
        return render(request, 'panel.html', context=context)
    else:
        return redirect('/auth')

def logout(request):
    if 'login' in request.session:
        del request.session['login']
    return redirect('/reg')

def addarticle(request):
    if 'login' in request.session:
        suc = ''
        if request.method == 'POST' and request.FILES:
            title = request.POST['title']
            description = request.POST['description']
            fulltext = request.POST['fulltext']
            cat = request.POST['cat']

            img = request.FILES['img']

            f = FileSystemStorage()
            f_name = f.save(img.name, img)

            art = Article()
            art.title = title
            art.description = description
            art.fulltext = fulltext
            art.user = User.objects.filter(login=request.session['login']).first()
            art.cat = Category.objects.filter(id=cat).first()
            art.img = 'blog/static/images/' + f_name
            art.save()

            article = Article.objects.order_by('-id').first()
            send_notif(request.session['login'], 'http://127.0.0.1:8000/' + str(article.id))

            suc = 'Вы создали новою статью'

            # return redirect('/addarticle')
        form = AddArticle()
    else:
        return render(request, '404.html')

    return render(request, 'addarticle.html', context={'form': form, 'suc': suc})

def listarticles(request):
    if 'login' in request.session:
        user = User.objects.filter(login=request.session['login']).first()
        articles = Article.objects.filter(user=user)
        return render(request, 'listarticles.html', context={'articles': articles})
    else:
        return render(request, '404.html')

def send_notif(user, link_article):
    subject = 'Оповещение создания статьи от пользователя ' + user
    message = 'Создана новая статья, которая доступна по ссылке' + link_article
    from_email = 'mawrin.stan@yandex.ru'

    users = User.objects.all()
    email_list = []
    for user in users:
        email_list.append(user.email)
    send_mail(subject, message, from_email, email_list)

def send(request):
    send_mail('tema', 'sdwadas', 'mawrin.stan@yandex.ru', ['mawrin.stan@yandex.ru'])

def users(request):
    filter_city = User.objects.values('city').annotate()
    s = []
    c1 = filter_city[0]['city']
    s.append(c1)
    for i in filter_city:
        if not i['city'] == c1:
            s.append(i['city'])
            c1 = i['city']

    current_user = get_object_or_404(User, login=request.session['login'])
    users = User.objects.all()

    return render(request, 'user/users.html', context={'users': users, 'current_user': current_user})

def userdetail(request, login):
    is_in_friend = False
    user = User.objects.filter(login=login).first()
    current_user = get_object_or_404(User, login=request.session['login'])
    if Friend.objects.filter(user=current_user, friend=user).exists():
        is_in_friend = True

    return render(request, 'user/userdetail.html', context={'user': user, 'is_in_friend': is_in_friend})

def addfriend(request):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.POST['id_friend'])
        current_user = get_object_or_404(User, login=request.session['login'])
        if user == current_user:
            return redirect('/users')

        if not Friend.objects.filter(user=current_user, friend=user).exists():
            Friend.objects.create(user=current_user, friend=user)

        return redirect('/users/' + user.login)

def chatid(request, id):
    user = get_object_or_404(User, login=request.session['login'])
    frienduser = get_object_or_404(User, id=id)
    if request.method == 'POST':
        message = request.POST['message']
        Chat.objects.create(user=user, friend=frienduser, message=message)

    chats = Chat.objects.filter(Q(user=user, friend=frienduser) | Q(user=frienduser, friend=user)).order_by('date')
    print(chats)

    return render(request, 'chat/chatid.html', context={'chats':chats, 'friend': id, 'user': request.session['login']})


def ajaxchat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = get_object_or_404(User, login=request.session['login'])
        frienduser = get_object_or_404(User, id=data['friend'])

        chats = Chat.objects.filter(Q(user=user, friend=frienduser) | Q(user=frienduser, friend=user)).order_by('date')

        r = ''
        for i in chats:
            r += '<div class="chat_message_item">'
            r += '<p>' + i.user.login + '' + str(i.date) +'</p>'
            r += '<p>' + i.message + '<p>'
            if user == i.user:
                r += '<p><a href="" onclick="deletemessage('+str(i.id)+')">Удалить</a></p>'
            r += '</div>'

        response_data = {'data': r}

        return JsonResponse(response_data)

def ajaxdelete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data['id']
        Chat.objects.filter(id=id).delete()
        response_data = {'data': 1}
        return JsonResponse(response_data)