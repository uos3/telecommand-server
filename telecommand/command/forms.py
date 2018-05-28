from django import forms

class EnterCommandForm (forms.Form):
    command = forms.CharField(initial="do a flip",
                              help_text="this will eventually be dropdowns.")

    def clean_command (self):
        cmd = self.cleaned_data['command']

        # validation etc.

        return cmd
