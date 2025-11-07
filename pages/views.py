from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Page

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class PageListView(ListView):
    model = Page
    template_name = 'pages/list.html'
    context_object_name = 'pages'
    paginate_by = 8

    def get_queryset(self):
        return Page.objects.filter(status=Page.PUBLISHED)

class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/detail.html'
    context_object_name = 'page'
    slug_field = 'slug'

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    fields = ['title', 'slug', 'summary', 'content', 'image', 'published_at', 'status']
    template_name = 'pages/form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Página creada correctamente')
        return super().form_valid(form)

class PageUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Page
    fields = ['title', 'slug', 'summary', 'content', 'image', 'published_at', 'status']
    template_name = 'pages/form.html'
    slug_field = 'slug'

    def form_valid(self, form):
        messages.success(self.request, 'Página actualizada')
        return super().form_valid(form)

class PageDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Page
    success_url = reverse_lazy('page_list')
    template_name = 'pages/confirm_delete.html'
    slug_field = 'slug'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Página eliminada')
        return super().delete(request, *args, **kwargs)

@login_required
def search_pages(request):
    q = request.GET.get('q', '').strip()

    if q == "":
        messages.info(request, "Ingresá un texto para buscar.")
        return redirect('page_list')

    pages = Page.objects.filter(status=Page.PUBLISHED, title__icontains=q)

    if not pages:
        messages.info(request, f"No se encontraron resultados para: {q}")

    return render(request, 'pages/list.html', {'pages': pages, 'query': q})
