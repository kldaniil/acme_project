from django.shortcuts import get_object_or_404, redirect, render

from .forms import BirthdayForm
from .utils import calculate_birthday_countdown
from .models import Birthday


def delete_birthday(request, pk):
    instance = get_object_or_404(Birthday, pk=pk)
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('birthday:list')
    return render(request, 'birthday/birthday.html', context)


def birthday(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None
    # if request.GET:
    #     form = BirthdayForm(request.GET)
    #     if form.is_valid():
    #         pass
    # else:
    #     form = BirthdayForm()
    # form = BirthdayForm(request.POST or None)  # Более короткая запись

    form = BirthdayForm(request.POST or None, instance=instance) 
    context = {'form': form}

    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
            )
        context.update({'birthday_countdown': birthday_countdown})

    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    birthdays = Birthday.objects.all()
    context = {'birthdays': birthdays}
    return render(request, 'birthday/birthday_list.html', context)
