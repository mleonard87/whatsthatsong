from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import JsonResponse
from django.conf import settings

import urllib2, json


def game_controller(request):
    """
    Return the single page web app that is the game controller.
    """
    return render_to_response(
        'controller.html',
        context_instance=RequestContext(request)
        )
