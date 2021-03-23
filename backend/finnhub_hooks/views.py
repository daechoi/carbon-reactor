from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# Example from https://blog.bearer.sh/consume-webhooks-with-python/

@require_POST
@csrf_exempt
def example(request):
    return HttpResponse("Hello, world.  This is the webhook response.")

def test(request):
    return HttpResponse("Hello!  You got me")

