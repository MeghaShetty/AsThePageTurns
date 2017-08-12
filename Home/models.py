from  __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User,default=1,on_delete=models.CASCADE)
	about = models.TextField(max_length=200,null=True, blank = True)
	blog = models.URLField(max_length=100,null=True, blank = True)
	coverpic = models.ImageField(upload_to='coverpic',null=True, blank = True)
	profilepic = models.ImageField(upload_to='profilepic', null=True, blank = True)

	def __str__(self):
		return self.about


class Genre(models.Model):
	genre_id = models.IntegerField(default=10)
	genre = models.CharField(max_length=20,default='General')

	def __str__(self):
		return self.genre


class Book(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE)
	bok_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=50,default='Blah Blah Blah')
	genre = models.IntegerField(default=10)
	coverpage = models.ImageField(upload_to='coverpage', null=True, blank=True)
	prologue = models.TextField(max_length=1000,default='No Prologue available')
	publish = models.BooleanField(default=False)
	no_of_likes = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.title



class PersonalCollection(models.Model):
	user_coll = models.ForeignKey(User,on_delete=models.CASCADE)
	id_book = models.ForeignKey(Book,on_delete=models.CASCADE)
	bookmark = models.BooleanField(default=False)
	bookmark_no = models.IntegerField(default=1)


class Chapter(models.Model):
	b_id = models.ForeignKey(Book,on_delete=models.CASCADE)
	chapter_no = models.IntegerField(default=1)
	chapter_title = models.CharField(max_length=20,null=True, blank = True)
	chapter_content = models.TextField(max_length=3000,null=True, blank = True)

	def __str__(self):
		return str(self.chapter_no)

class Forum(models.Model):
	forum_id = models.AutoField(primary_key = True)
	topic = models.CharField(max_length=100)
	content = models.CharField(max_length=1000)
	user_name = models.CharField(max_length=150, default="")

	def __str__(self):
		return self.topic


class Thread(models.Model):
	forum_no = models.ForeignKey(Forum, on_delete=models.CASCADE)
	post = models.CharField(max_length=5000)
	user_name = models.CharField(max_length=150)
	timestamp = models.DateTimeField(default=timezone.now())

	def __str__(self):
		return str(self.forum_no)

class LikedBook(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
