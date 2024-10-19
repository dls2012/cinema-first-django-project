from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Cinema, Comment, Profile


# Форма для Авторизации
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))

# Форма для регистрации пользователя
class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите фамилию'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите почту'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2') # fields отвечат за то как будут выстроены поля в форме



# Форма для добавления видео
class CinemaForm(forms.ModelForm):

    class Meta:
        model = Cinema
        fields = ('title', 'content', 'image', 'trailer', 'video', 'category')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название'
            }),
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Описание'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Изображение'
            }),
            'trailer': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Треилер'
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кинофильм'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Категория'
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Оставьте комментарий'
            })
        }


class EditAccountFrom(UserChangeForm):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))

    old_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'old_password', 'new_password', 'confirm_password')




class EditProfileForm(forms.ModelForm):
    photo = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
    }))

    about = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))


    class Meta:
        model = Profile
        fields = ('about', 'city', 'photo')
        widgets = {
            'city': forms.Select(attrs={
                'class': 'form-select',
            })
        }






