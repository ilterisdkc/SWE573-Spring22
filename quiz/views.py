from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView

from .models import *
from .forms import UpdateUserForm, UpdateProfileForm, LearningSpaceForm
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm
from django.forms import inlineformset_factory
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect


@login_required(login_url='/login')
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.success(request, 'Your profile is updated successfully')
            return redirect(to='user_profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required(login_url='/login')
def index(request):
    quiz = Quiz.objects.all()
    para = {'quiz': quiz}
    return render(request, "index.html", para)


@login_required(login_url='/login')
def quiz(request, myid):
    quiz = Quiz.objects.get(id=myid)
    return render(request, "quiz.html", {'quiz': quiz})


def quiz_data_view(request, myid):
    quiz = Quiz.objects.get(id=myid)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.content)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def save_quiz_view(request, myid):
    if is_ajax(request=request):
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(content=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(id=myid)

        score = 0
        marks = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.content)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.content:
                        if a.correct:
                            score += 1
                            correct_answer = a.content
                    else:
                        if a.correct:
                            correct_answer = a.content

                marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                marks.append({str(q): 'not answered'})

        Marks_Of_User.objects.create(quiz=quiz, user=user, score=score)

        return JsonResponse({'passed': True, 'score': score, 'marks': marks})


def Signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password != confirm_password:
            return redirect('/signup')

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')
    return render(request, "signup.html")


def Login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html")
    return render(request, "login.html")


def Logout(request):
    logout(request)
    return redirect('/')


def add_quiz(request):
    if request.method == "POST":
        form = QuizForm(data=request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.creator = request.user
            quiz.save()
            obj = form.instance
            return render(request, "add_quiz.html", {'obj': obj})
    else:
        form = QuizForm()
    return render(request, "add_quiz.html", {'form': form})


def add_question(request):
    questions = Question.objects.all()
    questions = Question.objects.filter().order_by('-id')
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.creator = request.user
            quiz.save()
            return render(request, "add_question.html")
    else:
        form = QuestionForm()
    return render(request, "add_question.html", {'form': form, 'questions': questions})


def delete_question(request, myid):
    question = Question.objects.get(id=myid)
    if request.method == "POST":
        question.delete()
        return redirect('/add_question')
    return render(request, "delete_question.html", {'question': question})


def delete_subject(request, myid):
    subject = Subject.objects.get(id=myid)
    if request.method == "POST":
        subject.delete()
        return redirect('/subject_list')
    return render(request, "delete_subject.html", {'subject': subject})


def add_options(request, myid):
    question = Question.objects.get(id=myid)
    QuestionFormSet = inlineformset_factory(Question, Answer, fields=('content', 'correct', 'question'), extra=4)
    if request.method == "POST":
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            for form in formset:
                f = form.save(commit=False)
                f.owner = request.user
                f.save()
            # formset.save()
            alert = True
            return render(request, "add_options.html", {'alert': alert})
    else:
        formset = QuestionFormSet(instance=question)
    return render(request, "add_options.html", {'formset': formset, 'question': question})


def results(request):
    marks = Marks_Of_User.objects.all()
    return render(request, "results.html", {'marks': marks})


def delete_result(request, myid):
    marks = Marks_Of_User.objects.get(id=myid)
    if request.method == "POST":
        marks.delete()
        return redirect('/results')
    return render(request, "delete_result.html", {'marks': marks})


def subject_view(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    contributors = subject.contributors.all()

    user_authenticated = False
    user_id = None
    if request.user.is_authenticated:
        user_authenticated = True
        user_id = request.user.id

    response = {
        'subject': subject,
        'contributors': contributors,
        'user_id': user_id,
        'user_authenticated': user_authenticated
    }

    return render(request, 'subject.html', response)


def subject_list_view(request):
    subjects = Subject.objects.all()

    user_authenticated = False
    user_id = None

    if request.user.is_authenticated:
        user_authenticated = True
        user_id = request.user.id

    response = {
        'subjects': subjects,
        'user_authenticated': user_authenticated,
        'user_id': user_id
    }

    return render(request, 'subject_list.html', response)


class SubjectCreateView(CreateView):
    model = Subject
    fields = ['title', 'description', 'fileinput']
    template_name = 'subject_form.html'

    def form_valid(self, form):
        subject = form.save(commit=False)
        subject.creator = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('subject', kwargs={'subject_id': self.object.pk})


class SubjectEditView(UpdateView):
    model = Subject
    fields = ['title', 'description', 'fileinput']
    template_name = 'subject_edit_form.html'
    success_url = '/subject_list/'

    #
    # def get_object(self, queryset=None):
    #     return get_object_or_404(Subject, pk=self.get_object().id)

    def form_valid(self, form):
        # subject = form.save(commit=False)
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('subject', kwargs={'pk': self.get_object().pk})


class CreateLearningSpace(CreateView):
    model = LearningSpace
    form_class = LearningSpaceForm
    template_name = 'learning_space_form.html'

    # success_url = reverse_lazy('/')

    # def form_valid(self, form):
    #     learning_space = form.save(commit=False)
    #
    #     return super().form_valid(form)
    #
    def get_success_url(self):
        return reverse('learning_space', kwargs={'learning_space_id': self.object.pk})


def learning_space_view(request, learning_space_id):
    learning_space = LearningSpace.objects.get(pk=learning_space_id)
    subjects = learning_space.subjects.all()
    quizzes = learning_space.quizzes.all()
    coLearners = learning_space.coLearners.all()
    print(coLearners)
    print(learning_space_id)

    user_coLearn = False

    for cl in coLearners:
        if cl.user.id == request.user.id:
            user_coLearn = True

    if request.method== 'POST':
        print(request)
        session_user = Profile.objects.get(user_id=request.user.id)
        if user_coLearn:
            learning_space.coLearners.remove(session_user)
            learning_space.save()
        else:
            learning_space.coLearners.add(session_user)
            learning_space.save()
        print("user_coLearn: ", str(user_coLearn))
        return redirect('/learning_space/%d' % learning_space_id)

    print("user_coLearn: ", user_coLearn)
    user_auth = False
    user_id = None
    if request.user.is_authenticated:
        user_auth = True
        user_id = request.user.id

    response = {
        'learning_space': learning_space,
        'subjects': subjects,
        'quizzes': quizzes,
        'coLearners': coLearners,
        'user_id': user_id,
        'user_authenticated': user_auth,
        'user_coLearn': user_coLearn
    }

    return render(request, 'learning_space.html', response)


def learning_space_list_view(request):
    learning_spaces = LearningSpace.objects.all()

    user_auth = False
    user_id = None

    if request.user.is_authenticated:
        user_auth = True
        user_id = request.user.id

    response = {
        'learning_spaces': learning_spaces,
        'user_authenticated': user_auth,
        'user_id': user_id
    }

    return render(request, 'learning_space_list.html', response)


def search_learning_spaces(request):
    user_auth = False

    if request.user.is_authenticated:
        user_auth = True

    if request.method == 'GET':
        query = request.GET.get('q')

        submit_button = request.GET.get('submit')

        if query is not None:
            lookups = Q(title__icontains=query) | Q(description__icontains=query)

            results = LearningSpace.objects.filter(lookups).distinct()

            context = {
                'results': results,
                'submit_button': submit_button,
                'user_authenticated': user_auth
            }

            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html')

    else:
        return render(request, 'search.html')
