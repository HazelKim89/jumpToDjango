from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    """
    계정 생성
    :param request:
    :return:
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # 사용자 인증 authenticate 함수는 사용자명과 비밀번호가 정확한지 검증하는 함수이다.
            user = authenticate(username=username, password=raw_password)
            login(request, user) # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})