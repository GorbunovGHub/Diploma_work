from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30, verbose_name='Логин')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    password = models.CharField(min_length=8, verbose_name='Введите пароль')
    repeat_password = models.CharField(min_length=8, verbose_name='Повторите пароль')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']
