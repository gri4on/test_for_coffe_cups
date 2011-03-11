from django.shortcuts import render_to_response
from django.forms.models import model_to_dict
from test_for_coffe_cups.usercards.models import UserCard, MiddlewareData
from test_for_coffe_cups.usercards.forms import CardForm
from django.core.context_processors import csrf
from django.template import RequestContext


def contact(request):
    """
    Handler for main page of test
    """
    c = {"card": UserCard.objects.all()[0]}
    return render_to_response("contacts.html", RequestContext(request, c))


def edit_card(request):
    """
    Edit User card
    """
    if request.method == "POST":
        form = CardForm(request.POST, instance=UserCard.objects.all()[0])
        if form.is_valid():
            form.save()
    c = {"form": CardForm(initial=model_to_dict(UserCard.objects.all()[0]))}
    c.update(csrf(request))
    return render_to_response("edit_card.html", RequestContext(request, c))


def report_middleware(request):
    """
    Show all stored requests
    """
    c = {"middleware_list": MiddlewareData.objects.all()}
    return render_to_response("middleware_report.html", RequestContext(request, c))


def context_processor(request):
    """
    Show settings from settings file, by context processor
    """
    return render_to_response("settings.html", RequestContext(request, {}))
