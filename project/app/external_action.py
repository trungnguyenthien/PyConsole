from django.http import JsonResponse
from .utils import log as logger
from .manager import slack as slackManager
from django.views.decorators.csrf import csrf_exempt

# ===============> Hook event from slack <===============
@csrf_exempt
def slack_hook(request):
  if request.method != 'POST':
    logger.log({'error': 'Only POST method is allowed.'})
    return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)

  return slackManager.slack_events(request)
