from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
# from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    )
from django.urls import reverse_lazy

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
from .utils import calculate_birthday_countdown


# @login_required
# def simple_view(request):
#     return HttpResponse('Страница для залогиненных пользователей!')


# вместо add_comment
class CongratuletionCreateView(LoginRequiredMixin, CreateView):
    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    # Переопределяем get_success_url()
    def get_success_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
            )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        return context


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form) 


class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 5


# вместо функции использую CBV CongratulationCreateView
# @login_required
# def add_comment(request, pk):
#     birthday = get_object_or_404(Birthday, pk=pk)
#     form = CongratulationForm(request.POST)

#     if form.is_valid():
#         congratulation = form.save(commit=False)
#         congratulation.author = request.user
#         congratulation.birthday = birthday
#         congratulation.save()

#     return redirect('birthday:detail', pk=pk)


# def delete_birthday_old(request, pk):
#     instance = get_object_or_404(Birthday, pk=pk)
#     form = BirthdayForm(instance=instance)
#     context = {'form': form}
#     if request.method == 'POST':
#         instance.delete()
#         return redirect('birthday:list')
#     return render(request, 'birthday/birthday.html', context)


# def birthday(request, pk=None):
#     if pk is not None:
#         instance = get_object_or_404(Birthday, pk=pk)
#     else:
#         instance = None

#     form = BirthdayForm(
#         request.POST or None,
#         files=request.FILES or None,
#         instance=instance
#         )

#     context = {'form': form}

    # Так сохранять, если добавлять автора:
    # if form.is_valid():
    #      instance = form.save(commit=False)
    #      instance.author = request.user
    #      instance.save()
    #

#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#             )
#         context.update({'birthday_countdown': birthday_countdown})

#     return render(request, 'birthday/birthday.html', context)


# def birthday_list_old(request):
#     # Получаем список всех объектов с сортировкой по id.
#     # birthdays = Birthday.objects.all()
#     birthdays = Birthday.objects.order_by('id')
#     paginator = Paginator(birthdays, 5)

#     # Получаем из запроса значение параметра page.
#     page_number = request.GET.get('page')

#     # Получаем запрошенную страницу пагинатора.
#     # Если параметра page нет в запросе или его значение не приводится к чис
#     # вернётся первая страница.
#     page_obj = paginator.get_page(page_number)

#     # Вместо полного списка объектов передаём в контекст
#     # объект страницы пагинатора

#     # context = {'birthdays': birthdays}
#     context = {'page_obj': page_obj}

#     return render(request, 'birthday/birthday_list.html', context)
