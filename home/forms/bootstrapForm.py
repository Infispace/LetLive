"""
:synopsis: Form and form fields with bootstrap classes
"""
class BootstrapForm():
    """
    Add Bootrap classes to forms and their fields
    """
    def add_form_control(self, form_fields):
        """
        Add Bootrap `form-control` class
        """
        for field in form_fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })

