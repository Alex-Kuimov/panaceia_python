# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserMain, UserDoctor, Document, Specialty, Associations, Education, Qualification, Support, TimeZone, SpecialtyList, Service


class UserMainInline(admin.StackedInline):
    model = UserMain
    can_delete = False
    verbose_name_plural = 'Основная информация'


class UserDoctorInline(admin.StackedInline):
    model = UserDoctor
    can_delete = False
    verbose_name_plural = 'Информация о докторе'


class DocumentInline(admin.StackedInline):
    extra = 0
    model = Document


class SpecialtyInline(admin.StackedInline):
    extra = 0
    model = Specialty


class AssociationsInline(admin.StackedInline):
    extra = 0
    model = Associations


class EducationInline(admin.StackedInline):
    extra = 0
    model = Education


class QualificationInline(admin.StackedInline):
    extra = 0
    model = Qualification


class ServiceInline(admin.StackedInline):
    extra = 0
    model = Service


class UserAdmin(UserAdmin):
    inlines = (
        UserMainInline,
        UserDoctorInline,
        DocumentInline,
        SpecialtyInline,
        AssociationsInline,
        EducationInline,
        QualificationInline,
        ServiceInline,
    )


class SpecialtySlug(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Support)
admin.site.register(TimeZone)
admin.site.register(SpecialtyList, SpecialtySlug)
