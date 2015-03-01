# -*- coding: utf-8 -*-
from django.contrib import admin
from mybudget.models import Account, Category, Expense, Organisation, Tag


class TagAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class ExpenseAdmin(admin.ModelAdmin):
    list_filter = ('account__organisation', 'account')
    list_display = ('date', 'category', 'amount', 'account', 'comment')


class AccountAdmin(admin.ModelAdmin):
    pass


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


class AccountInline(admin.TabularInline):
    model = Account
    extra = 0

    def expenses_count(self, instance):
        # assuming get_full_address() returns a list of strings
        # for each line of the address and you want to separate each
        # line by a linebreak
        return 3
            # instance.e
            # mark_safe('<br/>'),
            # '{0}',
            #((line,) for line in instance.get_full_address()),


class OrganisationAdmin(admin.ModelAdmin):
    inlines = [AccountInline, CategoryInline, ]


admin.site.register(Account, AccountAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Expense, ExpenseAdmin)
