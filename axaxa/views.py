import allauth.account.views
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import redirect, render
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
        slug = self.kwargs.get(self.slug_url_kwarg)
        return self.model.objects.get(slug=slug)

    def form_valid(self, form):
        comment = form.save(commit=False)  # commit = false - пока не сохраняет запись в бд
        comment.post = self.get_object()
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'post_slug': self.get_object().slug})


class AddLot(CreateView):
    form_class = AddLotForm
    template_name = 'axaxa/add_lot.html'

    def form_valid(self, form):
        lot = form.save(commit=False)
        lot.user = self.request.user
        lot.save()
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


@login_required
def profile(request):
    return render(request, 'axaxa/profile.html')


@login_required
def profile_bids(request):
    context = {'bids': Cars.objects.filter(bid_holder=request.user)}
    return render(request, 'axaxa/profile_bids.html', context=context)


@login_required
def profile_lots(request):
    context = {'lots': Cars.objects.filter(user=request.user).order_by('-time_end')}
    return render(request, 'axaxa/profile_lots.html', context=context)


class ProfileEditInfo(FormView):
    form_class = UpdateContactInfo
    template_name = 'axaxa/profile_contact_info.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):  # hope it's a right way to save changes
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.email = form.cleaned_data['email']
        user.phone_number = form.cleaned_data['phone_number']
        user.save()
        return super().form_valid(form)


class ProfileEditPicture(FormView):
    form_class = UpdateUserPicture
    template_name = 'axaxa/profile_pic_upd.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        user = self.request.user
        user.photo = form.cleaned_data['photo']
        user.save()
        return super().form_valid(form)


def logout_user(request):
    logout(request)

    return redirect('home')
