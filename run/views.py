from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Task
from django.views.decorators.csrf import csrf_exempt

def home(request):
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    # جلب المهام مع الفلترة
    tasks = Task.objects.all().order_by('-id')
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)
    if category_filter:
        tasks = tasks.filter(category=category_filter)

    # حساب الإحصائيات
    total_count = tasks.count()
    completed_count = tasks.filter(completed=True).count()
    remaining_count = total_count - completed_count
    progress = int((completed_count / total_count) * 100) if total_count > 0 else 0

    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        Task.objects.create(title=title, category=category)
        return redirect('home')

    context = {
        'tasks': tasks,
        'search_query': search_query,
        'category_filter': category_filter,
        'progress': progress,
        'completed_count': completed_count,
        'remaining_count': remaining_count,
    }
    return render(request, 'home.html', context)

def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('home') # تم التعديل من task_list إلى home

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('home') # تم التعديل من task_list إلى home

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title).strip()
        task.category = request.POST.get('category', task.category)
        task.save()
    return redirect('home') # تم التعديل من task_list إلى home

@csrf_exempt
def update_duration(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        seconds = request.POST.get('seconds')
        if seconds is not None:
            task.duration = int(seconds)
            task.save()
            return JsonResponse({'status': 'success', 'duration': task.duration})
    return JsonResponse({'status': 'error'}, status=400)