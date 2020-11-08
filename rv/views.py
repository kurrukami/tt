from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *

from ze.shit import *
from ze.decorators import *

from .models import *
from django import forms
from django.contrib import messages
# Create your views here.


class all_rv(View):

    template_name = 'all_rv.html'
    context = {}

    @method_decorator(only_doctors)
    def get(self, request):
        today = datetime.datetime.now()
        rvs = rv.objects.filter(rd_time__day=today.day)
        from_me_to_me(rv=rvs)
        if len(rvs) == 0:
            msg = 'u dont have any appointment for today'
            messages.error(request, msg)
        else:
            len_rvs = len(rvs)
            msg = f'u have {len_rvs} apointemnet today'
            messages.success(request, msg)
        self.context.setdefault('rvs', rvs)

        return render(request, self.template_name, self.context)






class rv_view(View):

    template_name = 'rv_view.html'
    type_ap = ['tommorw_ap', 'date_ap']
    context = {}



    def get(self, request, key):
        from_me_to_me(key1=key)
        rv = rv_form_view()
        from_me_to_me(context=self.context)

        if key in self.type_ap:
            return rv.get(request, key)

        #from_me_to_me(key2=key)
        return render(request, self.template_name, self.context)

    def post(self, request, key):
        rv_form = rv_form_view()
        form = rv_form.get_rv_form(key)
        from_me_to_me(msg=key)
        if form is not None:
            if key == 'tommorw_ap':
                f1 = form(request.POST)
                from_me_to_me(f1err=f1.errors)
                if f1.is_valid():
                    cd = f1.cleaned_data
                    date = rv_form.tomorow_date()
                    ap = rv.objects.create(
                    doc_name = cd["doc_name"],
                    name = cd["name"],
                    phone_num = cd["phone_num"],
                    cmnt = cd["cmnt"],
                    rd_time = date
                    )
                    msg = 'your appointment for tommorw was created'
                    from_me_to_me(msg=msg)
                    messages.success(request,msg)
                else:
                    msg = 'smtg is not valid, plz try again'
                    messages.error(request, f1.errors)
                    return self.get(request, key)

            if key == 'date_ap':
                f2 = form(request.POST)
                from_me_to_me(msg=f2.errors)
                if f2.is_valid():
                    cd = f2.cleaned_data
                    date = rv_form.wtvr_date(
                    year=cd["year"],
                    month = cd["month"],
                    day = cd["day"],
                    hour = cd["hour"]
                    )
                    check_rv = rv_form.check_rv(date)
                    from_me_to_me(msg=check_rv)
                    if not check_rv:
                        msg = f' {date} , this date alrady taken, plz try another day'
                        from_me_to_me(msg=msg)
                        messages.error(request, msg)
                        return self.get(request, key)

                    ap = rv.objects.create(
                    doc_name = cd["doc_name"],
                    name = cd["name"],
                    phone_num = cd["phone_num"],
                    cmnt = cd["cmnt"],
                    rd_time = date
                    )
                    msg = 'your appointment was created'
                    messages.error(request, msg)
                    from_me_to_me(msg=msg)
                else:
                    msg = 'smtg is not valid, plz try again'
                    from_me_to_me(msg=msg)
                    messages.error(request, f2.errors)
                    return self.get(request, key)

        return self.get(request, key)



class rv_form_view(View):

    form1 = rv_form_dt
    form2 = rv_form_tmrw
    template_name = 'rv_form_view.html'

    def get_rv_form(self, key):
        if key == 'tommorw_ap':
            return self.form2
        if key == 'date_ap':
            return self.form1
        else:
            return None

    
    def get(self, request, key):
        context = {
                 'key':key,
        }
        form = self.get_rv_form(key)
        if key == 'date_ap':
            form = form({
            'year' : self.date_now().year,
            'month' : self.date_now().month,
            'day' : self.date_now().day
            })


        context.setdefault('form', form)
        from_me_to_me(cnt=context)
        return render(request, self.template_name, context)

    def check_rv(self, date):
        try:
            r = rv.objects.get(rd_time=date)
            msg = 'date is alrady taken'
            return False
        except rv.DoesNotExist:
            return True


    def date_now(self):
        date = datetime.datetime.now()
        return date


    def tomorow_date(self):
        today = self.date_now()
        date = datetime.datetime(
        year=today.year,
        month = today.month,
        day = today.day +1,
        hour = today.hour,
        minute = today.minute
        )
        return date

    def wtvr_date(self, **args):

        date = datetime.datetime(
        year=int(args["year"]),
        month = int(args["month"]),
        day = int(args["day"]),
        hour = int(args["hour"])
        )
        return date
