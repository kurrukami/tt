from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages

from ze.shit import *
from ze.decorators import *

from django.core.exceptions import ObjectDoesNotExist

from ze.decorators import *

#from my_users.authentication import email_auth

# Create your views here.

decorators =[only_superusers]


class view(View):
    template_name = 'base.html'
    def get(self, request):
        return render(request, self.template_name, {})


from django.contrib.auth import logout
def log_out(request):
    logout(request)
    return redirect('login')


@only_superusers
def get_adminn_pk(request, pk):
    op = send_email(pk)
    if op.check_doctor():
        try:
            msg = 'send email process .........'
            from_me_to_me(msg=msg)
            pswd = op.generate_pswd()
            from_me_to_me(pswd='password generated ...')
            msg = op.generate_msg()
            from_me_to_me(msg='msg generated ...')
            doc = op.create_doctor()
            from_me_to_me(doctor='doctor created ...')
            op.send_him_mail()
            msg = 'send_email_process complited'
            from_me_to_me(msg=msg)
            messages.success(request, msg)

        except:
            msg = 'send email process failed'
            from_me_to_me(msg=msg)
            messages.success(request, msg)

    else:
        msg = 'this doctor is alrady here'
        from_me_to_me(msg=msg)
        messages.success(request, msg)

    del op
    try:
        from_me_to_me(op=op)
    except :
         from_me_to_me(op='op deleted')
    return redirect('admin_view')


from django.core.mail import send_mail
import random, math
class send_email:



    def __init__(self, pk):

        self.info = adminn_infos.objects.get(pk=pk)
        self.username = self.info.username
        self.send_email = self.info.email
        self.phone_num = self.info.phone_num
        self.msg = ''
        self.password = ''

    def check_doctor(self):
        try:
            doc = doctor.objects.get(email=self.send_email)
            return False
        except doctor.DoesNotExist:
            return True



    from_email = 'zahry.akram@gmail.com'
    subject = 'your password'


    def generate_msg(self):
        self.msg = f'we are glad u join our large community  {self.username}.\nhere is ur password : {self.password}.'
        from_me_to_me(msg=self.msg)
        return self.msg

    def generate_pswd(self):
        rn = random.random()*1000000
        rn = math.floor(rn)
        rn = str(rn)
        pwd = self.username+rn
        self.password = pwd
        from_me_to_me(pswd=self.password)
        return self.password

    def create_doctor(self):
        user = doctor.objects.create(username=self.username,
                                         email=self.send_email,
                                         phone_num=self.phone_num)
        user.set_password(self.password)
        user.save()
        msg = 'doctor has been created'
        from_me_to_me(msg=msg)
        return user


    def send_him_mail(self):
        try:
            send_mail(self.subject, self.msg, self.from_email, [self.send_email], fail_silently=False)
            msg = 'email has sent'
            from_me_to_me(msg=msg)
            return 11
        except:
            return 'error'




class admin_view(View):

    doctors = doctor.objects.all()
    doctors_infos = adminn_infos.objects.all()
    smtg = {
    "doctors": ("doctors.html", doctors),
    "doctors_infos": ("doctors_infos.html", doctors_infos)
    }
    @method_decorator(decorators)
    def get(self, request, key):
        if key in self.smtg.keys():
            if len(self.doctors) == 0:
                msg = 'no one want to join us yet :))'
                messages.success(request, msg)
            if len(self.doctors_infos) == 0:
                msg = 'u dt have any doctors yet :))'
                messages.success(request, msg)
            return render(request, self.smtg[key][0], {'smtg': self.smtg[key][1]})


class login_view(View):

    template_name = 'login.html'
    form = login_form

    def get(self, request):
        #from_me_to_me(request=dir(request))
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        f = self.form(request.POST)
        if f.is_valid():
            cd = f.cleaned_data
            #from_me_to_me(cd=cd)
            username = cd["username"]
            password = cd["password"]

            #user = adminn.objects.get(email=email)
            #from_me_to_me(user = user)
            #u = doctor.objects.get(username=username)

            #from_me_to_me(u=u)
            user = authenticate(request, username=username, password=password)
            from_me_to_me(user=user, ur=request.user)
            if user is not None and user.is_active:
                login(request, user)
                from_me_to_me(user=user, ur=request.user)
                if user.is_superuser:
                    admin = admin_view()
                    return admin.get(request, 'doctors_infos')

                msg = f'welcom {user.username}'
                from_me_to_me(msg=msg)
                return redirect("view")
            else:
                msg = 'user not found'
                from_me_to_me(msg=msg)
                return redirect("login")
        else:
            msg = 'form not valid'
            from_me_to_me(msg=msg)
            return redirect("login")


class send_infos_view1(View):
    template_name = 'send_infos1.html'
    def get(self, request):
        return render(request, self.template_name, {})


def send_infos_view(request):
    from_me_to_me(method=request.method)
    form = adminn_infos_form
    #from_me_to_me(form=form)
    if request.method == 'POST':
        f = form(request.POST)
        from_me_to_me(data=f)
        if f.is_valid():
            cd = f.cleaned_data
            from_me_to_me(cleaned_data=cd)
            infos = adminn_infos.objects.create(
            username = cd["username"],
            email = cd["email"],
            phone_num = cd["phone_num"]
            )
            from_me_to_me(infos=infos)
            msg = 'ur request has been sent, merci'
            messages.success(request, msg)
            return redirect("send_infos")
        else:
            msg = 'smtg went wrong'
            messages.error(request, msg)
            return redirect("send_infos")
    return render(request, "send_infos.html", {'form' : form })
