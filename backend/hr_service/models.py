from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Position(models.Model):
    """
    Модель для должностей
    """
    name = models.CharField(
        max_length=50,
        choices=[
            ('manager', 'Менеджер'),
            ('senior_dev', 'Senior-разработчик'),
            ('middle_dev', 'Middle-разработчик'),
            ('junior_dev', 'Junior-разработчик'),
        ],
        unique=True,
        verbose_name='Должность'
    )

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.get_name_display()


class Specialization(models.Model):
    """
    Модель для специализаций
    """
    name = models.CharField(
        max_length=50,
        choices=[
            ('python', 'Python'),
            ('devops', 'DevOps'),
            ('go', 'Go'),
            ('data_engineer', 'Data Engineer'),
        ],
        unique=True,
        verbose_name='Специализация'
    )

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.get_name_display()


class Employee(models.Model):
    """
    Модель сотрудника
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee',
        verbose_name='Пользователь'
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name='ФИО'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Должность'
    )
    specializations = models.ManyToManyField(
        Specialization,
        related_name='employees',
        verbose_name='Специализации'
    )
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates',
        verbose_name='Руководитель'
    )
    workplace_city = models.CharField(
        max_length=100,
        choices=[
            ('moscow', 'Москва'),
            ('spb', 'Санкт-Петербург'),
            ('paris', 'Париж'),
        ],
        verbose_name='Город'
    )
    workplace_country = models.CharField(
        max_length=100,
        default='Россия',
        verbose_name='Страна'
    )
    telegram_nick = models.CharField(
        max_length=100,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^@[\w]+$',
                message='Ник в Telegram должен начинаться с @ и содержать только буквы, цифры и подчеркивания'
            )
        ],
        verbose_name='Ник в Telegram'
    )
    about = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name='О себе'
    )
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_employees',
        verbose_name='Кем создан'
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    @property
    def short_name(self):
        """Возвращает фамилию и инициалы (Волков Я. В.)"""
        parts = self.full_name.split()
        if len(parts) >= 3:
            return f"{parts[0]} {parts[1][0]}. {parts[2][0]}."
        return self.full_name


class EmployeeDraft(models.Model):
    """
    Модель черновика изменений сотрудника
    """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='drafts',
        verbose_name='Сотрудник'
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name='ФИО',
        blank=True
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Должность'
    )
    specializations = models.ManyToManyField(
        Specialization,
        related_name='draft_employees',
        blank=True,
        verbose_name='Специализации'
    )
    manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='draft_subordinates',
        verbose_name='Руководитель'
    )
    workplace_city = models.CharField(
        max_length=100,
        choices=[
            ('moscow', 'Москва'),
            ('spb', 'Санкт-Петербург'),
            ('paris', 'Париж'),
        ],
        blank=True,
        verbose_name='Город'
    )
    workplace_country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Страна'
    )
    telegram_nick = models.CharField(
        max_length=100,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^@[\w]+$',
                message='Ник в Telegram должен начинаться с @ и содержать только буквы, цифры и подчеркивания'
            )
        ],
        verbose_name='Ник в Telegram'
    )
    about = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name='О себе'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Ожидает подтверждения'),
            ('approved', 'Подтверждено'),
            ('rejected', 'Отклонено'),
        ],
        default='pending',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Черновик сотрудника'
        verbose_name_plural = 'Черновики сотрудников'

    def __str__(self):
        return f"Черновик для {self.employee.full_name}"


class NewsArticle(models.Model):
    """
    Модель для новостей
    """
    author = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок'
    )
    content = models.TextField(
        verbose_name='Текст статьи'
    )
    published_at = models.DateTimeField(
        verbose_name='Дата публикации'
    )
    source_url = models.URLField(
        blank=True,
        verbose_name='Источник'
    )
    fetched_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата получения'
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_at']

    def __str__(self):
        return self.title
