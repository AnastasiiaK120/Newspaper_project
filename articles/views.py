from django.shortcuts import render
from .models import Article
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CommentForms

# class ArticleListView(ListView):
#    model = Article
#    template_name = 'article_list.html'
#    # context_object_name = "XXX"

def article_list(request):
    object_list = Article.objects.all()
    return render(request, 'article_list.html', {'object_list': object_list})

#  class ArticleDetailView(LoginRequiredMixin, DetailView):
#    model = Article
#    template_name = 'article_detail.html'
#
#    login_url = 'login'

def article_detail(request, pk):
    object = get_object_or_404(Article, id=pk)

    comments = object.comments.all()
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForms(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = object
            new_comment.save()
    else:
        comment_form = CommentForms()

    return render(request, 'article_detail.html',
                      {'object': object,
                       'comments': comments,
                       'new_comment': new_comment,
                       'comment_form': comment_form
                       }
                      )


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'article_edit.html'
    fields = ['title', 'body']
    login_url = 'login'

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_create.html'
    fields = ['title', 'body', 'author']
    login_url = 'login'

    # def form_invalid(self, form):
    #    form.instance.author = self.request.user.id
    #    return super().form_valid(form)
