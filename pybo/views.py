from django.shortcuts import render, get_object_or_404, redirect
from .forms import QuestionForm, AnswerForm
from .models import Question
from django.core.paginator import Paginator


def index(request):
    """
    Pybo 목록 출력
    :param request: page
    :return: 질문목록html
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징처리
    paginator = Paginator(question_list, 10) # 한 페이지당 10개씩 표시
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}

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


def answer_create(request, question_id):
    """
    pybo 답변 등
    :param request:
    :param question_id:
    :return: redirect 상세 내용 html
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    content = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', content)


def question_create(request):
    """
    pybo 질문 등록
    :param request: 
    :return: 
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST) # request.POST 에는 사용자가 입력한 내용들이 담겨있다.
        if form.is_valid():
            form.save(commit=True) # QuestionForm이Question모델과 연결된 폼이므로 'form.save()'이렇게 사용 가능
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
