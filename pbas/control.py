from django.http import JsonResponse

from pbas.models import ProgressBar


def create_progress_bar(request):
    pb = ProgressBar.objects.create(
        title=request.POST.get('title', ''),
        total=request.POST['total'],
        current=request.POST.get('current', 0)
    )
    pb.save()
    return JsonResponse(pb.to_dict())


def update_progress_bar(request, code):
    pb = ProgressBar.objects.get(code=code).first()
    set_to = request.POST.get('set_to', None)

    if set_to is None:
        increment_by = request.POST.get('increment_by', 1)
        pb.increment(increment_by)
    else:
        pb.current = set_to

    pb.save()
    return JsonResponse(pb.to_dict())


def get_progress_bar(request, code):
    pb = ProgressBar.objects.get(code=code).first()
    return JsonResponse(pb.to_dict())
