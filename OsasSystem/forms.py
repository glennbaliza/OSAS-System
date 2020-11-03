from django.forms import ModelForm
from .models import osas_r_userrole, osas_r_section_and_year, osas_r_personal_info
 

class osas_r_personal_infoForm(forms.ModelForm):
    class Meta:
        model =  osas_r_personal_info
        fields = [
            'stud_id',
            'stud_no',
            'stud_course_id',
            'stud_yas_id',
            'stud_lname',
            'stud_fname',
            'stud_mname',
            'stud_birthdate',
            'stud_gender',
            'stud_address',
            'stud_email',
            'stud_m_number',
            'stud_hs',
            'stud_hs_add',
            'stud_e_name',
            'stud_e_address',
            'stud_e_m_number',
        ]


        