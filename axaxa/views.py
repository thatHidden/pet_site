from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import *

from axaxa.forms import *


class SearchCar(ListView):
    model = Cars
    template_name = 'axaxa/home.html'
    context_object_name = 'lots'

    def get_queryset(self):
        car = self.request.path.split("/")[-1]
        query = Cars.objects.filter(brand__iexact=car)
        return query


class ShowPost(DetailView, FormView):
    model = Cars
    slug_url_kwarg = 'post_slug'
    template_name = 'axaxa/post.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post_id=self.get_object().id)
        return context

    def object(self, queryset=None):
        # Вернуть объект модели, который соответствует указанному slug
        slug = self.kwargs.get(self.slug_url_kwarg)
        return self.model.objects.get(slug=slug)

    def form_valid(self, form):
        comment = form.save(commit=False)  # commit = false - пока не сохраняет запись в бд
        comment.post = self.get_object()  # связываем поле post с текущим лотом
        comment.user = self.request.user  # связываем комментарий с пользователем
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Вернуть текущий URL в качестве URL после успешной отправки
        return reverse('post', kwargs={'post_slug': self.get_object().slug})


class AddLot(CreateView):
    form_class = AddLotForm
    template_name = 'axaxa/add_lot.html'

    def form_valid(self, form):
        form.save()
        return redirect('home')


class HomeView(ListView):
    context_object_name = 'lots'
    queryset = Cars.objects.all()
    template_name = 'axaxa/home.html'

    def get_queryset(self):
        return Cars.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available'] = Cars.objects.values('brand').annotate(count=Count('id')).order_by('brand')
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'axaxa/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'axaxa/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)

    return redirect('home')
