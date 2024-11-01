from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.db import connection
from .models import Form, Question
from django.views.decorators.csrf import csrf_exempt
from .create_all import CreateForm
from .answer import Answer, ShowAnswer
import json

def home(request):
    return HttpResponse('<a href="create">Create Form</a>')

@csrf_exempt
def index(request):
    form = Form.objects.values("id", "name", "description", "gen_date")
    context = {'form':form}
    return render(request, 'index.html', context)


@csrf_exempt
def forms(request, form_id):
    form = Form.objects.filter(id=form_id).values("name", "description")
    questions_choices = list(Question.objects.filter(form_id=form_id).values('question_type_id', 'question', 'choices', 'id'))
    if request.method == "POST":
        Answer(request).answer()
        return HttpResponse('Success')  
    context = {'form_id':form_id, 'form':form, 'questions_choices':questions_choices}

    return render(request, 'forms.html', context)


@csrf_exempt
def answers(request):   
    form = Form.objects.values("id", "name")
    data = []

    if request.method == "POST":
        datas = ShowAnswer(request)
        data = datas.show_answer()
  
    context = {'form':form, 'data':data}
    return render(request, 'answers.html', context)


@csrf_exempt
def create(request):
    if request.method == "POST":
        CreateForm(request).forms()
        return HttpResponse('Success')  
    return render(request, 'create.html')
































# def create(request):
#     QuestionFormSet = formset_factory(QuestionModelForm, extra=2)

#     if request.method == 'POST':
#         form_form = FormModelForm(request.POST)
#         question_formset = QuestionFormSet(request.POST, prefix='questions')

#         if form_form.is_valid() and question_formset.is_valid():
#             form_instance = form_form.save()

#             for question_form in question_formset:
#                 question_instance = question_form.save(commit=False)
#                 question_instance.form = form_instance
#                 question_instance.save()
                
#             return redirect('home')
#     else:
#         form_form = FormModelForm()
#         question_formset = QuestionFormSet(prefix='questions')

#     return render(request, 'create.html', {'form_form': form_form, 'question_formset': question_formset})

