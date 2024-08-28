import json
from typing import OrderedDict
from urllib import response
from warnings import filters
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django import forms
from blog.models import BlogPost, BlogComment
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core import serializers

# methode d'affichage des articles
class blogHomeView(ListView):
    model = BlogPost
    context_object_name = "posts"
    ordering = ['-created_on']

    # affiche les donnee en fonction de connecté ou pas
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(comment_count=Count('comments'))        
        if self.request.user.is_authenticated:
            return queryset
        
        return queryset.filter(published = True)
    

# vue de creation d'article (LoginRequiredMixin oblige l'utilisateur à se connecter avant d'acceder à la vu de creation d'article)
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog/add_article.html'
    fields = ['title','content','thumbnail','published']
    success_url = reverse_lazy('blog:home')
    


# selectionner automatiquement l'utilisateur connecté
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

#vue de modification d'article
class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=BlogPost
    template_name = "blog/update_article.html"
    fields = ['title','content', 'thumbnail','published']
    success_url = reverse_lazy('blog:home')

    def test_func(self):
        # Vérifie que l'utilisateur connecté est le propriétaire de l'article
        article = self.get_object()
        return self.request.user == article.author
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "Vous n'êtes pas le propriétaire de cet article.")
        return redirect('blog:home')

# Vue de suppression d'article
class BlogDeleteView(UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = "blog/delete_article.html"
    context_object_name = "articletodelete"
    success_url = reverse_lazy('blog:home')

    def test_func(self):
        # Vérifie que l'utilisateur connecté est le propriétaire de l'article
        article = self.get_object()
        return self.request.user == article.author
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "Vous n'êtes pas le propriétaire de cet article.")
        return redirect('blog:home')


class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['text']


# Vue detail des articles 
class BlogDetailView(DetailView):
    model = BlogPost
    context_object_name = "detailArticle"
    template_name = "blog/detail_article.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()  # Récupère tous les commentaires associés à l'article
        context['form'] = CommentForm()  # Ajoute le formulaire de commentaire au contexte
        return context
    
    def post(self, request, *args, **kwargs):
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog_post = self.get_object()  # Lien avec l'article actuel
                comment.author = request.user  # Auteur du commentaire
                comment.save()
                return redirect('blog:detail', slug=self.get_object().slug)  # Redirection vers la vue de détail
            return self.get(request, *args, **kwargs)  # Réaffiche la page avec les erreurs de formulaire


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(BlogComment, id=comment_id)
    blog_post = comment.blog_post  # On récupère l'article associé au commentaire

    if request.user == comment.author:  # Vérifie que l'utilisateur est l'auteur du commentaire
        comment.delete()    
    return redirect('blog:detail', slug=blog_post.slug)  

# API des articles
def ArticleApi(request):
    articles = BlogPost.objects.all()
    json = serializers.serialize("json",articles)
    return HttpResponse(json)