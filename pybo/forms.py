from django import forms
from pybo.models import Question, Answer, Comment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        """
        {{ form.as_p }} 태그 HTML코드를 자동으로 생성하므로 부트스트랩이나 부수적인 요소를 적용하기 위해서는 
        아래와 같이 widget을 사용하면 된다. 그러나 보통 디자인적으로 제한이 많이 생기므로 수동으로 폼을 작성한다.(question_form.html참조)
        """
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # }
        """
        또한 모델의 컬럼명이 영문이 아닌 다른 언어로 표시하고 싶다면 labels속성을 지정해주면 된다.
        """
        labels = {
            'subject': '제목',
            'content': '내용',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }