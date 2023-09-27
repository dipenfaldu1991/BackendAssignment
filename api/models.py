from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.CharField(max_length=255, blank=True)
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)
    followers = models.ManyToManyField('self',
                                       related_name='Follower',
                                       blank=True,
                                       symmetrical=False)
    bio = models.TextField('Bio', blank=True)
    email = models.EmailField(
        'email address',
        unique=True,
        blank=True,
        null=True,
        help_text='Required if mobile phone number is empty. 254 characters or fewer. A valid email address.',
        error_messages={
            'unique': 'A user with that email already exists.',
        },
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','mobile_phone','first_name','last_name','password']

    class Meta:
        db_table = 'User'
        ordering = ('pk',)
        get_latest_by = 'user'
    def __str__(self):
        if self.full_name:
            return f'{self.full_name} - {self.email}'
        return self.email



class Post(models.Model):
    author = models.ForeignKey(User,
                               related_name='Owner',
                               on_delete=models.CASCADE)
    image = models.ImageField('Image',
                              upload_to='post/')
    posted_time = models.DateTimeField('Post_posted_time', auto_now_add=True)
    caption = models.CharField('Caption', max_length=50, blank=True)
    location = models.CharField('Location', max_length=30, blank=True)

    def __str__(self):
        return "{}'s post({})".format(self.author, self.pk)