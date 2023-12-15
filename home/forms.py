from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.helper import FormHelper


class CustomLoginForm(LoginForm):
    """
    Custom login form
    """

    def __init__(self, *args, **kwargs):
        """
        Add custom classes to the form.
        Remove the Forgot Password link.
        """
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = "block mb-2 text-customblack font-bold"

        self.fields["password"].help_text = False


class CustomSignupForm(SignupForm):
    """
    Custom sign up form
    """

    def __init__(self, *args, **kwargs):
        """
        Add custom classes to the form.
        """
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = "block mb-2 text-customblack font-bold"
