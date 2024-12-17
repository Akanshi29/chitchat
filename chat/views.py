from django.shortcuts import render, redirect
from account.models import Contacts,UserProfile
from .models import Group
from django.db.models import Count


def chatPage(request,group_id):
    if not request.user.is_authenticated:
        return redirect("login-user")
    group = Group.objects.get(
        id=group_id
    )
    group_members = group.members.exclude(user=request.user).first()
    conatct_to = group_members if group.chat_type== "1on1" else group.title
    context = {"conatct_to": conatct_to, "group_id": group.id}
    return render(request, "chat/chatPage.html", context)



def activeUser(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    groups = Group.objects.filter(
            members=request.user.userprofile
        ).order_by('updated_at')
    context = {"groups": groups}
    return render(request, "chat/activeUserList.html", context)

def createGroup(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    if request.method == "POST":
        group_name = request.POST.get('group_name')
        contact_names = request.POST.getlist('contact_names')
        selected_contacts = request.POST.getlist('selected_contacts')
        if not group_name:
            group_name = "_".join(contact_names)
        user_admin = UserProfile.objects.get(user=request.user)
        contacts = Contacts.objects.filter(id__in=selected_contacts)
        user_members = contacts.values_list('user_member', flat=True)
        group = Group.objects.create(admin=user_admin, title=group_name, chat_type="group")
        group.members.add(user_admin, *user_members)
        context = {"conatct_to": group.title, "group_id": group.id}
        return render(request, "chat/chatPage.html", context)
    contacts = Contacts.objects.filter(user__user=request.user)
    context = {"contacts": contacts}
    return render(request, "chat/create_group.html", context)
    