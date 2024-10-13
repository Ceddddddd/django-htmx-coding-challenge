from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts_app.forms import InviteUserForm
from accounts_app.models import UserInvitation


class InviteUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Instantiate the form for the GET request 
        form = InviteUserForm()
        
        # Render the template and pass the form to the context
        return render(request, "accounts_app/profile.html", {"inviteForm": form})

    def post(self, request, *args, **kwargs):
        form = InviteUserForm(request.POST)

        if form.is_valid():
            # We could further improve this here to first check if an invitation for this email already exists and is not expired
            UserInvitation.objects.filter(email=form.cleaned_data["email"]).delete()

            invitation = UserInvitation(email=form.cleaned_data["email"], invited_by=request.user)
            invitation.save()

            invitation.send_invitation_email()

            return render(request, "accounts_app/profile.html", {"inviteForm": form, "invited": True})
        else:
            return render(request, "accounts_app/profile.html", {"inviteForm": form})