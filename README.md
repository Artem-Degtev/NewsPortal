>>> from news.models import *
>>> u1 = User.objects.create_user(username='Semyon')
>>> u2 = User.objects.create_user(username='Maxim')
>>> Author.objects.create(authorUser=u1)
<Author: Author object (1)>

>>> Category.objects.create(name='IT')
<Category: Category object (1)>

>>> author = Author.objects.get(id=1)
>>> author
<Author: Author object (1)>

>>> Post.objects.create(author=author, categoryType='NW', title='Python', text='Python is really cool')
<Post: Post object (1)>
>>> Post.objects.get(id=1)
<Post: Post object (1)>
>>> Post.objects.get(id=1).title
'Python'

>>> Post.objects.get(id=1).postCategory.add(Category.objects.get(id=1))

>>> Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=Author.objects.get(id=1).authorUser, text='anytextbyauthor')
<Comment: Comment object (1)>
>>> Comment.objects.get(id=1).like()
>>> Comment.objects.get(id=1).rating
1

>>> Comment.objects.get(id=1).dislike()
>>> Author.objects.get(id=1)
<Author: Author object (1)>
>>> a = Author.objects.get(id=1)
>>> a.update_rating()
>>> a.ratingAuthor
-1
>>> Post.objects.get(id=1).like()
>>> a.update_rating()
>>> a.ratingAuthor
2
>>> a = Author.objects.order_by('-ratingAuthor')[:1]
>>> a
<QuerySet [<Author: Author object (1)>]>

>>> Author.objects.create(authorUser=u2)
<Author: Author object (2)>
>>> Category.objects.create(name='Юмор')
<Category: Category object (2)>
>>> Category.objects.create(name='Книги')
<Category: Category object (3)>
>>> Category.objects.create(name='Базы данных')
<Category: Category object (4)>
>>> author2 = Author.objects.get(id=2)
>>> author2
<Author: Author object (2)>
>>> Post.objects.create(author=author2, categoryType='AR', title='Joke #1', text='Встретились как-то два программиста')
<Post: Post object (2)>
>>> Post.objects.get(id=2).postCategory.add(Category.objects.get(id=2))

>>> Comment.objects.create(commentPost=Post.objects.get(id=2), commentUser=Author.objects.get(id=2).authorUser, text='фигня...')
<Comment: Comment object (2)>
>>> Post.objects.create(author=author2, categoryType='AR', title='Об SQL', text='SQL очень занятная штука')
<Post: Post object (3)>
>>> Post.objects.get(id=3).postCategory.add(Category.objects.get(id=4))
>>> Comment.objects.create(commentPost=Post.objects.get(id=3), commentUser=Author.objects.get(id=1).authorUser, text='Круто!')
<Comment: Comment object (3)>
>>> Comment.objects.create(commentPost=Post.objects.get(id=3), commentUser=Author.objects.get(id=2).authorUser, text='Спасибо)')
<Comment: Comment object (4)>
>>> Post.objects.get(id=2).like()
>>> Post.objects.get(id=3).like()
>>> Post.objects.get(id=3).like()

>>> a.update_rating()
>>> a.ratingAuthor
2
>>> b = Author.objects.get(id=2)
>>> b.update_rating()
>>> b.ratingAuthor
9
>>> a = Author.objects.order_by('-ratingAuthor')[:1]
>>> a
<QuerySet [<Author: Author object (2)>]>
>>> 
