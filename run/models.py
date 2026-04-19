from django.db import models


class TaskManager(models.Manager):
    """مدير مخصص لتوليد التقارير والإحصائيات تلقائياً"""

    def get_report(self):
        total = self.count()
        completed = self.filter(completed=True).count()
        remaining = total - completed
        progress = (completed / total * 100) if total > 0 else 0
        return {
            'total': total,
            'completed_count': completed,
            'remaining_count': remaining,
            'progress': round(progress, 1)
        }

class Task(models.Model):
    # ... حقولك السابقة ...
    duration = models.IntegerField(default=0) # تخزين الوقت بالثواني

    def get_duration_display(self):
        import datetime
        return str(datetime.timedelta(seconds=self.duration))
class Task(models.Model):
    # خيارات التصنيف المحددة
    CATEGORY_CHOICES = [
        ('work', 'عمل 💼'),
        ('personal', 'شخصي 🏠'),
        ('study', 'دراسة 📚'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان المهمة")
    completed = models.BooleanField(default=False, verbose_name="مكتملة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    # حقل تخزين الوقت بالثواني (للساعة الموقوتة في الواجهة)
    duration = models.IntegerField(default=0, verbose_name="الوقت المستغرق بالثواني")

    # حقل التصنيف
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='personal',
        verbose_name="التصنيف"
    )

    # ربط المدير المخصص بالنموذج
    objects = TaskManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = "مهمة"
        verbose_name_plural = "المهام"

    def __str__(self):
        return self.title

    def get_duration_display(self):
        """تحويل الثواني إلى تنسيق (ساعة:دقيقة:ثانية) لعرضه في الواجهة"""
        hours, remainder = divmod(self.duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"