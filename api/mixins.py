class UserQuerySetMixin():
    user_field = 'user'
    allow_staff_view = False
    def get_queryset(self, *args, **kwargs):
        lookup_data = {}
        user = self.request.user
        lookup_data[self.user_field] = user.id
        qs = super().get_queryset(*args, **kwargs)
        if user.is_superuser:
            return qs
        if self.allow_staff_view and user.is_staff:
            return qs
        return qs.filter(**lookup_data)