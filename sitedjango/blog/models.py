from django.db import models

# Create your models here.
class Contact(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    link = models.CharField(max_length=100, verbose_name='Ссылка')

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Новость:')

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название котегории')

    def __str__(self):
        return self.title

# class City(models.Model):
#     title = models.CharField(max_length=200, verbose_name='Город')
#
#     def __str__(self):
#         return self.title

class User(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    login = models.CharField(max_length=100, verbose_name='Login')
    city = models.CharField(verbose_name='Город', max_length=200, default='Москва')
    email = models.CharField(max_length=100, verbose_name='Email')
    password = models.CharField(max_length=100, verbose_name='Пароль')
    avatar = models.ImageField(upload_to='static/user', default='static/user/default.png')

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок статьи')
    description = models.TextField(verbose_name='Описание статьи')
    img = models.ImageField(upload_to='blog/static/images', verbose_name='Картинка')
    fulltext = models.TextField(verbose_name='Полный текст статьи')
    cat = models.ForeignKey(Category, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE, default=1)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comentary(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя', default='User')
    title = models.TextField(verbose_name='Текст коментария')
    date = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article, models.CASCADE)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.CharField(max_length=100, verbose_name='Email')
    message = models.TextField(verbose_name='Текст сообщения')

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.name} - {self.friend.name}'

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_chat')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_chat')
    message = models.TextField(verbose_name='Сообщение')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.name} - {self.friend.name}'