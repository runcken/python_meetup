from django.contrib import admin
from .models import (
    Event,
    Speaker,
    Speech,
    Participant,
    Question,
    Subscription,
    Donation
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_at')
    list_filter = ('is_active', 'date', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'
    ordering = ('-date',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'date')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_id', 'speeches_count')
    search_fields = ('name',)
    list_editable = ('telegram_id',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('name',)
        }),
        ('Telegram', {
            'fields': ('telegram_id',)
        }),
    )


@admin.register(Speech)
class SpeechAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'event', 'start_time')
    list_filter = ('is_active', 'event', 'speaker')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_time'
    ordering = ('-start_time',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'speaker', 'event')
        }),
        ('Время проведения', {
            'fields': ('start_time', 'end_time')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('get_display_name', 'telegram_id', 'company', 'position', 'questions_count', 'registered_at')
    search_fields = ('full_name', 'username', 'company')
    list_filter = ('experience', 'registered_at')
    date_hierarchy = 'registered_at'

    fieldsets = (
        ('Основная информация', {
            'fields': ('full_name', 'username', 'telegram_id')
        }),
        ('Профессиональная информация', {
            'fields': ('company', 'position', 'experience')
        }),
    )

    def get_display_name(self, obj):
        return obj.full_name or f"@{obj.username}" or str(obj.telegram_id)

    get_display_name.short_description = 'Имя участника'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('get_short_text', 'participant', 'speech', 'created_at', 'is_answered')
    list_filter = ('is_answered', 'speech', 'created_at')
    search_fields = ('question_text', 'participant__full_name')
    date_hierarchy = 'created_at'
    list_editable = ('is_answered',)

    fieldsets = (
        ('Вопрос', {
            'fields': ('question_text', 'speech', 'participant')
        }),
        ('Статус', {
            'fields': ('is_answered',)
        }),
    )

    def get_short_text(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text

    get_short_text.short_description = 'Текст вопроса'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('participant', 'event', 'subscribed_at')
    list_filter = ('event', 'subscribed_at')
    search_fields = ('participant__full_name', 'participant__username', 'event__title')
    date_hierarchy = 'subscribed_at'
    readonly_fields = ('subscribed_at',)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'amount', 'created_at')
    list_filter = ('created_at',)
