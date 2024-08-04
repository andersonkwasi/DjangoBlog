from django.contrib import admin

# afficher les champs de notre modele (BlogPost) dans l'interface d'administration.
from blog.models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title" ,
                    "author",
                    "last_updated",
                    "created_on",
                    "content",
                    "thumbnail",
                    "published",
                    "slug",)
    
    list_editable = ("published",)


# relier le model d'affichage des champs (BlogPostAdmin) au model des champs (BlogPost)
admin.site.register(BlogPost, BlogPostAdmin)