from django.http import HttpResponse


def index(request):
    return HttpResponse("안녕하세요 pybo에 오신걸 환영합니다.")

