from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .models import Category, Cinema, Comment, Profile, Ip
from .forms import LoginForm, RegisterForm, CinemaForm, CommentForm, EditAccountFrom, EditProfileForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .tests import get_user_ip

# Create your views here.
# Функции или классы созданные здь называються Вьюшками
# def index_view(request):
#     cinemas = Cinema.objects.all()
#     context = {
#         'cinemas': cinemas,
#         'title': 'CinemaGo смотреть бесплатно'
#     }
#
#     return render(request, 'cinema_go/index.html', context)

class CinemaListView(ListView):
    model = Cinema
    context_object_name = 'cinemas'
    template_name = 'cinema_go/index.html'
    extra_context = {
        'title': 'CinemaGo смотреть бесплатно'
    }


# ==================================================================================================
# Вьюшка для получения фильмов по категории
# def cinema_category_view(request, pk):
#     cinemas = Cinema.objects.filter(category_id=pk)
#     category = Category.objects.get(pk=pk)
#     context = {
#         'cinemas': cinemas,
#         'title': f'Смотерть: {category.title}'
#     }
#     return render(request, 'cinema_go/index.html', context)


class CinemaListByCategory(CinemaListView):

    # Метод что бы переназначить вывод данных по категории
    def get_queryset(self):
        cinemas = Cinema.objects.filter(category_id=self.kwargs['pk'])
        return cinemas

    # Метод что бы дополнительно ято то отправлять на страницу
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()  # Создали пустйо словарь метода
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Смотерть: {category.title}'
        return context


# ==================================================================================================
# Вьюшка для страницы детали кинофильма
# def cinema_detail_view(request, pk):
#     cinema = Cinema.objects.get(pk=pk)  # Получим фильм по id
#
#     context = {
#         'title': cinema.title,
#         'cinema': cinema
#     }
#
#     return render(request, 'cinema_go/cinema_detail.html', context)

class CinemaDetailView(DetailView):
    model = Cinema
    context_object_name = 'cinema'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        cinema = Cinema.objects.get(pk=self.kwargs['pk'])
        cinemas = Cinema.objects.filter(category=cinema.category)[::-1][:3]
        context['title'] = cinema.title
        context['cinemas'] = cinemas
        context['comments'] = Comment.objects.filter(cinema=cinema)

        ip = get_user_ip(self.request)
        user_ip = Ip.objects.filter(ip=ip, cinema=cinema)
        if not user_ip:
            ip = Ip.objects.create(ip=ip, cinema=cinema)
            ip.save()

        if self.request.user.is_authenticated:
            context['form'] = CommentForm()


        return context


# ==================================================================================================
def user_login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Методом пытаемся получить из БД пользователя
            if user:  # Если есть пользователь
                login(request, user)  # При помощи функции входим в аккаунт
                messages.success(request, f'Добро пожаловать {user.username}')
                return redirect('main')
            else:
                messages.error(request, 'Не верный логин или пароль')
                return redirect('login')
        else:
            messages.error(request, 'Не верный логин или пароль')
            return redirect('login')

    else:
        form = LoginForm()  # В прееменную

    context = {
        'title': 'Вход в аккаунт',
        'form': form
    }

    return render(request, 'cinema_go/login.html', context)


def user_logout_view(request):
    logout(request)
    messages.warning(request, 'Вы вышли из Аккаунта 😒')
    return redirect('main')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)  # При регистрации создаём профиль пользователю
            profile.save()  # Сохраняем
            messages.success(request, 'Регистрация прошла успешно.\nВойдите в Аккаунт')
            return redirect('login')
        else:
            for field in form.errors:  # Проходим циклом по полям в кторых есть ошибки
                messages.error(request, form.errors[field].as_text())
                return redirect('registration')
    else:
        form = RegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }

    return render(request, 'cinema_go/register.html', context)


# ===========================================================

# Вьюшка для добавления кинофильмов
# def add_cinema_view(request):
#     if request.user.is_staff:
#         if request.method == 'POST':
#             form = CinemaForm(request.POST, request.FILES) # Получим из формы текст и файлы
#             if form.is_valid():
#                 cinema = Cinema.objects.create(**form.cleaned_data)
#                 cinema.save()
#                 return redirect('cinema', cinema.pk)
#             else:
#                 messages.warning(request, 'Что то пошло не так')
#                 return redirect('add_cinema')
#
#         else:
#             form = CinemaForm()
#
#         context = {
#             'title': 'Добавить видео',
#             'form': form
#         }
#         return render(request, 'cinema_go/add_cinema.html', context)
#     else:
#         return redirect('main')

class CinemaCreateView(CreateView):
    model = Cinema
    form_class = CinemaForm
    template_name = 'cinema_go/add_cinema.html'
    extra_context = {
        'title': 'Добавить видео'
    }

    def form_valid(self, form): # В методе присваемаем Автора кинофильму
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Метод для проверки
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:  # Если статус пользователя не сотрудник
            return redirect('main')
        else:
            return super(CinemaCreateView, self).get(request, *args, **kwargs)


class CinemaUpdateView(UpdateView):
    model = Cinema
    form_class = CinemaForm
    template_name = 'cinema_go/add_cinema.html'
    extra_context = {
        'title': 'Изменить видео'
    }

    # Метод для проверки
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:  # Если статус пользователя не сотрудник
            return redirect('main')
        else:
            return super(CinemaUpdateView, self).get(request, *args, **kwargs)


class CinemaDeleteView(DeleteView):
    model = Cinema
    context_object_name = 'cinema'
    success_url = reverse_lazy('main')

    # Метод для проверки
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:  # Если статус пользователя не сотрудник
            return redirect('main')
        else:
            return super(CinemaDeleteView, self).get(request, *args, **kwargs)


class SearchResult(CinemaListView):
    def get_queryset(self):
        word = self.request.GET.get('q')
        cinemas = Cinema.objects.filter(title__iregex=word)
        return cinemas


def save_comment(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.cinema = Cinema.objects.get(pk=pk)
        comment.save()
        return redirect('cinema', pk)


class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'cinema_go/cinema_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        comment = Comment.objects.get(pk=self.kwargs['pk'])  # Получим комент по id
        cinema = Cinema.objects.get(pk=comment.cinema.pk)  # Получим кинофильм комментария
        cinemas = Cinema.objects.filter(category=cinema.category)[::-1][:3]  # Получим кинофильм категории фильма

        context['title'] = cinema.title
        context['cinema'] = cinema
        context['cinemas'] = cinemas
        context['comments'] = Comment.objects.filter(cinema=cinema)
        return context

    def get_success_url(self):
        return reverse('cinema', kwargs={'pk': self.object.cinema.pk})



# РЕализовать вьюшку для удаления комментария
def comment_delete(request, cinema_pk, comment_pk):
    user = request.user if request.user.is_authenticated else None
    comment = Comment.objects.get(user=user, pk=comment_pk, cinema=cinema_pk)
    comment.delete()
    return redirect('cinema', cinema_pk)

def profile(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        profile = Profile.objects.get(user=user)
        cinemas = Cinema.objects.filter(author=user)

        context = {
            'title': f'Профиль {user.username}',
            'profile': profile,
            'cinemas': cinemas
        }
        return render(request, 'cinema_go/profile.html', context)
    else:
        return redirect('login')


# Вьюшка для изменения Аккаунта
def edit_account_profile_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if profile:
            account_form = EditAccountFrom(instance=request.user)
            profile_form = EditProfileForm(instance=request.user.profile)

            context = {
                'title': f'Изменения данных {request.user.username}',
                'account_form': account_form,
                'profile_form': profile_form
            }
            return render(request, 'cinema_go/edit.html', context)
        else:
            return redirect('login')
    else:
        return redirect('login')


def edit_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            edit_profile = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if edit_profile.is_valid():
                edit_profile.save()
                messages.success(request, 'Данные изменены')
                return redirect('profile')
            else:
                messages.error(request, 'Вы указали не корректные данные')
                return redirect('change')


def edit_account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            edit_account_form = EditAccountFrom(request.POST, instance=request.user)
            if edit_account_form.is_valid():
                edit_account_form.save()
                data = edit_account_form.cleaned_data  # Получим форму в виде соваря
                user = User.objects.get(id=request.user.id)
                if user.check_password(data['old_password']):
                    if data['old_password'] and data['new_password'] == data['confirm_password']:
                        user.set_password(data['new_password'])
                        user.save()
                        update_session_auth_hash(request, user)  # Функция которая оставит нас авторизованными
                        messages.success(request, 'Данные успешно изменены')
                        return redirect('profile')
                    else:
                        for field in edit_account_form.errors:
                            messages.error(request, edit_account_form.errors[field].as_text())
                            return redirect('change')
                else:
                    for field in edit_account_form.errors:
                        messages.error(request, edit_account_form.errors[field].as_text())
                        return redirect('change')

                return redirect('profile')

            else:
                for field in edit_account_form.errors:
                    messages.error(request, edit_account_form.errors[field].as_text())
                    return redirect('change')






