from django.contrib import admin
from task_manager.models import Task, SubTask, Category

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

# Инлайн форма для SubTask
class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

# Админка для Task с укороченным названием и инлайн
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'deadline', 'created_at')  # колонки в списке
    search_fields = ('title', 'description')  # поиск по заголовку и описанию
    list_filter = ('status', 'categories')  # боковые фильтры
    ordering = ('-created_at',)  # сортировка по дате создания
    fields = ('title', 'description', 'categories', 'status', 'deadline')  # поля формы
    list_per_page = 10

    inlines = [SubTaskInline]  # подключаем инлайн формы

    # Метод для укороченного отображения названия
    def short_title(self, obj):
        return (obj.title[:10] + '...') if len(obj.title) > 10 else obj.title
    short_title.short_description = 'Title'

admin.site.register(Task, TaskAdmin)

# Админка для SubTask с кастомным action
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'task')
    ordering = ('-created_at',)
    fields = ('title', 'description', 'task', 'status', 'deadline')
    list_per_page = 10

    # Action для отметки выбранных подзадач как Done
    actions = ['mark_as_done']

    def mark_as_done(self, request, queryset):
        updated_count = queryset.update(status='done')
        self.message_user(request, f"{updated_count} подзадач помечены как Done")

    mark_as_done.short_description = "Отметить выбранные подзадачи как Done"

admin.site.register(SubTask, SubTaskAdmin)

