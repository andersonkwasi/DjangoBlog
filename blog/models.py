from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.db import models

User = get_user_model()

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(verbose_name="Titre",unique=True, max_length=255)
    slug = models.SlugField(max_length=225, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_on = models.DateField(blank=True, null=True, auto_now_add=True)
    published = models.BooleanField(default=False)
    content = models.TextField(blank=True, verbose_name="Commentaire")


    class Meta:
        ordering = ['-created_on']
        verbose_name = "Article"


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

# Vrifie si le username existe
    @property
    def author_or_no(self):
        return self.author if self.author else "Indefine"