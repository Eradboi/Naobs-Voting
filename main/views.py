from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice, Check
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
"""def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Sing up successfully for ' + user)
            return redirect("signup")
        else:
            for msg in form.errors:
                ans = str(form.errors[msg]).split("<li>")[1].split("</li>")[0]
                messages.error(request, f"{msg}: {ans}")
    else:
        form = RegisterForm()
    return render(request, "main/signup.html", {"form":form,"errors":form.errors})"""
@login_required 
def vote(request, question_id):
    try:
        if request.method == 'POST':
            list = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
            votes = str(Check.objects.filter(user=request.user)).split(',')
            votes = len(votes)

            if votes == 7:
                return render(
                            request,
                            "main/index.html",
                            {
                                "votes": votes,  
                            },
                        )
            if int(request.POST["choice"])  in list:
                checker = Check.objects.filter(number=int(request.POST["choice"]), user=request.user)
                
                if int(request.POST["choice"])%2 != 0:
                    checker2 = Check.objects.filter(number=int(request.POST["choice"])+1, user=request.user)
                
                if int(request.POST["choice"])%2 == 0:
                    checker2 = Check.objects.filter(number=int(request.POST["choice"])-1, user=request.user)
                
                if str(checker) == '<QuerySet []>' and str(checker2) == '<QuerySet []>':
                    try:
                        question = get_object_or_404(Question, pk=question_id)
                    
                        selected_choice = question.choice_set.get(pk=request.POST["choice"])
                
                        selected_choice.votes += 1
                        selected_choice.save()
                        check = Check.objects.create(number=int(request.POST["choice"]), user=request.user)
                        check.save()
                    except (KeyError, Choice.DoesNotExist):
                        # Redisplay the question voting form.
                        return render(
                            request,
                            "main/index.html",
                            {
                                "question": question,
                                "error_message": "You didn't select a choice.",
                            },
                        )
                    else:   
                     
                        messages.success(request, "Your have voted succesfully")
                        return HttpResponseRedirect("/")
                else:
                    messages.success(request, "Your can not vote twice in one category")
                    return HttpResponseRedirect("/")
    except:
        messages.success(request, "You didn't select a candidate")
        return HttpResponseRedirect("/")
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "main/results.html", {"question": question, 'all':all})

@login_required
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:7]
    context = {"latest_question_list": latest_question_list}
    return render(request, "main/index.html", context)
def check2(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("This username is vaild")
    else:
        return HttpResponse("<div style='color: red; font-size: 12px;'>This username is not valid</div>")

def handling_404(request, exception):
    return render(request, 'main/404.html', {})

def error_500(request):
    return render(request, "main/500.html",{})