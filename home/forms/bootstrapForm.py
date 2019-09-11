"""
:synopsis: Form and form fields with bootstrap classes
"""
from django import forms


class BootstrapForm():
    """
    Add Bootrap classes to forms and their fields
    """
    def add_form_control(self):
        """
        Add Bootrap `form-control` class
        """
        for field in self.fields.values():
            if isinstance(field, forms.FileField):
                field.widget.attrs.update({
                    'class': 'custom-file-input',
                })

            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                })

