from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.
from blog.models import BlogPost

# methode d'affichage des articles
class blogHomeView(ListView):
    model = BlogPost
    context_object_name = "posts"

    # affiche les donnee en fonction de connecté ou pas
    def get_queryset(self):
        queryset = super().get_queryset()
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

# Vue detail des articles 
class BlogDetailView(DetailView):
    model = BlogPost
    context_object_name = "detailArticle"
    template_name = "blog/detail_article.html"
