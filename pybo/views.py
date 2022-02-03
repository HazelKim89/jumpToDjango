from django.shortcuts import render, get_object_or_404, redirect
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone


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


@login_required(login_url='common:login')
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
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    content = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', content)


@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    :param request: 
    :return: 
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST) # request.POST 에는 사용자가 입력한 내용들이 담겨있다.
        if form.is_valid():
            question = form.save(commit=False) # QuestionForm이Question모델과 연결된 폼이므로 'form.save()'이렇게 사용 가능
            question.author = request.user
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    :param request:
    :param question_id:
    :return:
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    :param request:
    :param question_id:
    :return:
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변 수정
    :param request:
    :param answer_id:
    :return:
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변 삭제
    :param request:
    :param answer_id:
    :return:
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)