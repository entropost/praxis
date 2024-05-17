from django.forms import ModelForm
from .models import simGame, Company
from django.contrib.auth.forms import UserCreationForm


class HrForm(ModelForm):
    class Meta:
        model = Company
        fields = ['commercialRepHirings', 'commercialRepDismissals', 'commercialRepBaseSalary', 
                  'commercialRepCommisions', 'administrationDirHirings', 'administrationDirDismissals',
                    'administrationDirBaseSalary', 'administrationExecHirings', 'administrationExecDimissals', 'administrationExecBaseSalary',
                    'administrationEmpHirings', 'administrationEmpDismissals', 'administrationEmpBaseSalary']
        



class  MarketDecForm(ModelForm):
    class Meta:
        model = Company
        fields = ['priceP1', 'priceP2', 'priceP3', 'pubBrand', 'pubP1', 'pubP2', 'pubP3']


class  AdminFinDecForm(ModelForm):
    class Meta:
        model = Company
        fields = ['savingsInvestment', 'savingsWithdrawal']