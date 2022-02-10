from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question


def index(request):
    """
    Pybo 목록 출력
    :param request: page
    :return: 질문목록html
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')     # 페이지
    kw = request.GET.get('kw', '')          # 검색어
    so = request.GET.get('so', 'recent')    # 정렬기준

    # 정렬
    if so == 'recommend':       # 추천순
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':       # 인기순
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:                       # 최신순
        question_list = Question.objects.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |                  # 제목검색
            Q(content__icontains=kw) |                  # 내용검색
            Q(author__username__icontains=kw) |         # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)   # 답변 글쓴이검색
        ).distinct()
    # 페이징처리
    paginator = Paginator(question_list, 10) # 한 페이지당 10개씩 표시
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    :param request:
    :param question_id:
    :return: 상세 내용 html
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)