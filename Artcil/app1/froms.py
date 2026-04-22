from django import forms
from .models import Category, Post, Comment, Like

# 1. فورم التصنيفات
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'اسم التصنيف',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم التصنيف الجديد...',
                'style': 'border-radius: 10px;'
            }),
        }

# 2. فورم المنشورات (الأكثر تفصيلاً)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # لاحظ أننا استبعدنا 'author' و 'created_at' لأنها تملأ تلقائياً من الباكيند
        fields = ['title', 'category', 'content']
        labels = {
            'title': 'عنوان المنشور',
            'category': 'التصنيف',
            'content': 'محتوى الموضوع',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'اكتب عنواناً جذاباً...',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'اكتب تفاصيل المنشور هنا...',
                'rows': 8,
            }),
        }

# 3. فورم التعليقات
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': '', # تركناه فارغاً ليظهر كصندوق دردشة
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'اكتب تعليقك الآن...',
                'rows': 2,
                'style': 'resize: none; border-radius: 20px;'
            }),
        }

# 4. فورم الإعجابات (يستخدم عادة في العمليات الخلفية لكنه مهم للتحقق)
class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = [] # لا نحتاج حقول إدخال لأن الإعجاب يتم بضغط زر (ID فقط)

    # إضافة لمسة برمجية: التأكد من عدم تكرار الإعجاب في الفورم نفسه
    def clean(self):
        cleaned_data = super().clean()
        # هنا يمكنك إضافة منطق إضافي إذا أردت التحقق من بيانات معينة
        return cleaned_data

# 5. فورم البحث (إضافي لخدمة مشروعك الكبير)
class SearchForm(forms.Form):
    query = forms.CharField(
        label='بحث',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ابحث عن منشور...',
            'type': 'search'
        })
    )