from django.forms import ModelForm
from .models import osas_r_userrole, osas_r_section_and_year


class osas_r_userroleForm(ModelForm):
    class Meta:
        model = osas_r_userrole
        fields = '__all__'

class osas_r_section_and_yearForm(ModelForm):
    class Meta:
        model = osas_r_section_and_year
        fields = "__all__"