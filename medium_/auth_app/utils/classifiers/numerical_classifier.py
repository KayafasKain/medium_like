import datetime
from django.apps import apps

ClientClass = apps.get_model('profile_app', 'ClientClass')

class NumericalClassifier():
    def __init__(self, profile):
        if profile:
            self.income_yearly = profile.income_yearly
            self.birth_date = profile.birth_date
            self.class_employment_value = profile.employment_type.value
        else:
            raise ValueError('Profile object does mot specified')

    def get_user_class(self):
        return self.calulate_user_class()

    def calulate_user_class(self):
        age = datetime.datetime.now().date() - self.birth_date
        age = age.days/365
        rait = (self.income_yearly * self.class_employment_value)/age
        return ClientClass.objects.filter(weight__lte=rait).order_by('-weight')[:1][0]