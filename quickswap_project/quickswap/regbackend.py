from registration.backends.default.views import RegistrationView
from quickswap.forms import TestForm
from quickswap.models import UserProfile


class MyRegistrationView(RegistrationView):

    form_class = TestForm

    def register(self, form_class):
        new_user = super(MyRegistrationView, self).register(form_class)
        print(new_user)
        w = form_class.cleaned_data['test']
        print('!!!'+w)
        new_profile = UserProfile.objects.create(user=new_user, test=w)
        print(vars(new_profile))
        print(dir(new_profile))
        new_profile.save()
        return new_profile
