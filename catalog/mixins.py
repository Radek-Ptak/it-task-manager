from django.contrib.auth.mixins import UserPassesTestMixin

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class StaffOrOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return (
            self.request.user.is_staff
            or obj == self.request.user
        )

class StaffOrTaskAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        task = self.get_object()
        return (
            self.request.user.is_staff
            or task.created_by == self.request.user
        )
