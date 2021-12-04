from functools import wraps

from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy

from .models import Cart


def author_verification(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user != Cart.objects.get(pk=kwargs).user:
            return HttpResponseRedirect(reverse_lazy('product-list'))
        return function(request, *args, **kwargs)
    return wrap
