from django.contrib import admin
from .models import Task, SubTask, Category

# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)

# Админка для Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # отображаемое поле в списке
    search_fields = ('name',)  # поиск по имени
    ordering = ('name',)  # сортировка по имени
    fields = ('name',)  # поля формы редактирования
    list_per_page = 10  # количество объектов на странице

admin.site.register(Category, CategoryAdmin)

# Админка для Task
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')  # колонки в списке
    search_fields = ('title', 'description')  # поиск по заголовку и описанию
    list_filter = ('status', 'categories')  # боковые фильтры
    ordering = ('-created_at',)  # сортировка по дате создания
    fields = ('title', 'description', 'categories', 'status', 'deadline')  # поля формы
    list_per_page = 10

admin.site.register(Task, TaskAdmin)

# Админка для SubTask
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'task')
    ordering = ('-created_at',)
    fields = ('title', 'description', 'task', 'status', 'deadline')
    list_per_page = 10

admin.site.register(SubTask, SubTaskAdmin)

