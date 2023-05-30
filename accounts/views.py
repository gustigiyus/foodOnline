from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            ########### CREATED THE USER USING THE USER CREATE MODEL ###########

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registered successfully")


            ########### CREATED THE USER USING THE FORM ###########
            # password = form.cleaned_data['password']
            # # That means the form ready to be saved (You can configure if u want to add some fields, before send it)
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # # Form acctually saved to the database
            # user.save()

            return redirect("registerUser")
        else:
            print("invalid form")
            print(form.errors)
            # return redirect("registerUser")
    else:
        form = UserForm()


    context = {
        "form": form,
    }
    return render(request, 'accounts/registerUser.html', context)