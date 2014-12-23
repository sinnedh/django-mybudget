# -*- coding: utf-8 -*-
from django.contrib import admin
from mybudget.models import Account, Category, Expense, Organisation, Tag


class TagAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class ExpenseAdmin(admin.ModelAdmin):
    pass


class AccountAdmin(admin.ModelAdmin):
    pass


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


class AccountInline(admin.TabularInline):
    model = Account
    extra = 0


class OrganisationAdmin(admin.ModelAdmin):
    inlines = [AccountInline, CategoryInline, ]


admin.site.register(Account, AccountAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Expense, ExpenseAdmin)
