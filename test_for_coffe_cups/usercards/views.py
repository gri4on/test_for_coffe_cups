# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.forms.models import model_to_dict
from test_for_coffe_cups.usercards.models import UserCard
from test_for_coffe_cups.usercards.models import MiddlewareData
from test_for_coffe_cups.usercards.forms import CardForm
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.datastructures import MultiValueDictKeyError


def contact(request):
    """
    Handler for main page of test
    """
    c = {"card": UserCard.objects.all()[0]}
    return render_to_response("contacts.html", \
                                   RequestContext(request, c))


@login_required
def edit_card(request):
    """
    Edit User card
    """
    # Check if there is a submit form - then process it
    if request.method == "POST":
        # Check if there is a ajax form -
        #  then return just form html code without template ...
        if request.is_ajax():
            form = CardForm(request.POST, instance=UserCard.objects.all()[0])
            c = {"form": form}
            c['card'] = UserCard.objects.all()[0]
            if form.is_valid():
                form.save()
            return render_to_response("edit_form.html", \
                                   RequestContext(request, c))

        form = CardForm(request.POST, instance=UserCard.objects.all()[0])
        if form.is_valid():
            form.save()
    c = {"form": CardForm(initial=model_to_dict(UserCard.objects.all()[0]))}
    c['card'] = UserCard.objects.all()[0]
    c['nomenu'] = True
    c.update(csrf(request))
    return render_to_response("edit_card.html", \
                                   RequestContext(request, c))


@csrf_protect
def report_middleware(request):
    """
    Show all stored requests
    """
    # creating context
    c = {}
    c['error'] = False

    if request.method == "POST":
        # get form (set priority for object)
        midlware = MiddlewareData.objects.get(id=request.POST['id'])
        try:
            midlware.priority = int(request.POST['priority'])
            # save new priority
            midlware.save()
        except ValueError:
            # if error - just don`t do anything
                c['error'] = True
                c['error_obj_id'] = int(request.POST['id'])
                c['error_value'] = request.POST['priority']

    # Show only first 10 requests
    try:
        sorting = request.GET['sort']
        if sorting not in ['none', 'increase', 'decrease']:
            sorting = 'none'
    except MultiValueDictKeyError:
        sorting = 'none'
    if sorting == 'increase':
        order = "priority"
    elif sorting == "decrease":
        order = "-priority"
    else:
        # by default we order by id
        order = "id"
    c["middleware_list"] = MiddlewareData.objects.filter(id__lte=10).order_by(order)
    c['card'] = UserCard.objects.all()[0]
    c['sorting'] = sorting
    return render_to_response("middleware_report.html", \
                                   RequestContext(request, c))


def context_processor(request):
    """
    Show settings from settings file, by context processor
    """
    c = {"card": UserCard.objects.all()[0]}
    return render_to_response("settings.html", \
                                   RequestContext(request, c))
