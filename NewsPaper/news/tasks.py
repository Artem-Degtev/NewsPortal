from celery import shared_task
from .models import Post
from django.core.mail import send_mail


@shared_task()
def Post_created(post_id):
    post = Post.objects.get(id=post_id)
    subject = 'Post nr. {}'.format(post_id)
    message = 'Дорогой {},\n\nВы успешно создали пост.\
                    Ваш пост {}.'.format(post.first_name,
                                                 post.id)
    mail_sent = send_mail(subject,
                          message,
                          'admin@gmail.com',
                          [post.email])
    return mail_sent

