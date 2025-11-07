from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

class Page(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
    (DRAFT, 'Borrador'),
    (PUBLISHED, 'Publicado'),
    ]


    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=300)
    content = RichTextField()
    image = models.ImageField(upload_to='pages/', blank=True, null=True)
    published_at = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)


    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-published_at', '-created']


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('page_detail', args=[self.slug])
        