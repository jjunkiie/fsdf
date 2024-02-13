from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import  Coalesce

article = 'AR'
news = 'NE'
POST_TYPES = [
    (news, 'Новость'),
    (article, 'Статья')
    ]
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.posts.aggregate (pr=Coalesce (Sum ('rating'), 0)).get('pr')
        comments_rating = self.user.comments.aggregate (cr=Coalesce (Sum ('rating'), 0)).get('cr')
        posts_comments_rating = self.posts.aggregate (pcr=Coalesce (Sum ('comment__rating'), 0)).get('pcr')


        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()

class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=100)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=2,
                                 choices=POST_TYPES,
                                 default=news)
    datetime_post = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[:124]}..."


class PostCategory(models.Model):
    one_to_many_relation = models.ForeignKey(Post, on_delete=models.CASCADE)
    one_to_many_relation1 = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    one_to_many_relation = models.ForeignKey(Post, on_delete=models.CASCADE)
    one_to_many_relation1 = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    date_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()