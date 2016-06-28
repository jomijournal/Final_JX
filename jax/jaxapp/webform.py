from django import forms
from models import det_ax, cli_ax
import sys
reload(sys)
sys.setdefaultencoding("utf8")
print "Starting UTF script..."

class orgform(forms.Form):
    choice=[(x.id,str(x.org)) for x in cli_ax.objects.all().order_by('org')]
    organization = forms.ChoiceField(choice)

class commentform(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs={'size': '75'}))
