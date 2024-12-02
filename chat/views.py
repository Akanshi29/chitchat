from django.shortcuts import render, redirect
from account.models import Contacts
def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/chatPage.html", context)


def activeUser(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    contacts = Contacts.objects.filter(user__user=request.user)
    print(contacts)
    context = {"contacts": contacts}
    return render(request, "chat/activeUserList.html", context)

