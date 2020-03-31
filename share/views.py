from django.http import HttpResponse
# Module 3 imports
# import three functions: authentication, login, logout
from django.contrib.auth import authenticate, login, logout
# import redirect
from django.shortcuts import render, redirect, get_object_or_404
# import all the models created so far
from .models import Script, Problem, Coder
# import User model
from django.contrib.auth.models import User

def signup(request):
    if request.user.is_authenticated:
        return redirect("share:index")
    return render(request, 'share/signup.html')
def create(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        coder_yet = request.POST.get('coder_yet_checkbox' , False)

        if username is not None and email is not None and password is not None: # checking that they are not None
            if not username or not email or not password: # checking that they are not empty
                return render(request, "share/signup.html", {"error": "Please fill in all required fields"})
            if User.objects.filter(username=username).exists():
                return render(request, "share/signup.html", {"error": "Username already exists"})
            elif User.objects.filter(email=email).exists():
                return render(request, "share/signup.html", {"error": "Email already exists"})
            # save our new user in the User model
            user = User.objects.create_user(username, email, password)
            coder = Coder.objects.create(user= user, coder_yet = coder_yet).save()
            user.save()

            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            # this logs in our new user, backend means that we are using the  Django specific auhentication and not 3rd party

        return redirect("share:index")

    else:
        return redirect("share:signup")
def login_view(request):
    if request.user.is_authenticated:
        return redirect("share:index")
    return render(request, 'share/login.html')
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not username or not password:
            return render(request, "share/login.html", {"error":"One of the fields was empty"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("share:index")
        else:
            return render(request, "share/login.html", {"error":"Wrong username or password"})
    else:
        return redirect("share:index")
def logout_view(request):
    logout(request)
    return redirect("share:login")
def index(request):
    # Testing http request object inside a view function
    print('*********** Testing request obj ************')
    print('request:' , request)
    print('request.headers: ', request.headers)
    print('request.headers["host"]:', request.headers['host'])
    print('request.method: ', request.method)
    print('request.user:' , request.user)
    print('*******************************')

    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            all_problems = Problem.objects.all()   # all_problems is a list object [   ]

            return render(request, "share/index.html", {"user":user, "all_problems": all_problems})
        else:
            return redirect("share:login")
    else:
        return HttpResponse(status=500)
def dashboard(request):
    # retieve user, my_problems, my-scripts
    # builds my_problems_scripts dict
    # renders dashboard.html
    # each problem should have a link show more details of a particular problem,
    # this link starts route show_my_problem

    # Testing http request object inside a view function
    print('*********** Testing request obj ************')
    print('request:' , request)
    print('request.headers: ', request.headers)
    print('request.headers["host"]:', request.headers['host'])
    print('request.method: ', request.method)
    print('request.user:' , request.user)
    print('*******************************')

    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            my_problems = Problem.objects.filter(coder=user.coder.id)   # Problem table has a coder field (FK)
            my_scripts =  Script.objects.filter(coder=user.coder.id)

            print('*********** Testing objs retrieved from DB ************')
            print('my_problems:', my_problems)
            print('my_scripts:', my_scripts)
            print('*******************************')

            return render(request, "share/dashboard.html", {"my_scripts": my_scripts, "my_problems": my_problems })
def publish_problem(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            return render(request, "share/publish_problem_form.html", {"user":user} )


def create_problem(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")

        coder = user.coder
        title = request.POST["title"]
        description = request.POST["description"]
        discipline = request.POST["discipline"]
        make_public = request.POST.get('make_public', False)
        if make_public == 'on':
            make_public = True
        else:
            make_public = False

        if not title and not description:
            return render(request, "share/publish_problem_form.html", {"error":"Please fill in all required fields"})

        try:
            problem = Problem.objects.create(coder=coder, title=title, description=description, discipline=discipline, make_public=make_public)
            problem.save()

            problem = get_object_or_404(Problem, pk=problem.id)
            scripts = Script.objects.filter(problem=problem.id)

            return render(request, "share/problem.html",{"user":user, "problem":problem, "scripts": scripts})

        except:
            return render(request, "share/publish_problem_form.html", {"error":"Can't create the problem"})

    else:
        # the user enteing    http://127.0.0.1:8000/problem/8/create
        user = request.user
        all_problems = Problem.objects.all()
        return render(request, "share/index.html", {"user":user, "all_problems": all_problems, "error":"Can't create!"})
def show_problem(request, problem_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            # make sure to import the fucntion get_object_or_404 from  django.shortcuts
            problem = get_object_or_404(Problem, pk=problem_id)
            scripts = Script.objects.filter(problem=problem_id)

            # Module 6
            if problem.make_public or problem.coder.user.id == user.id:
                return render(request, "share/problem.html",
                {"user":user, "problem":problem, "scripts": scripts})
            else:
                # the problem is private and you are not the author
                return render(request, "share/index.html",
                {"error":"The problem you clicked is still private and you are not the author"})
def edit_problem(request, problem_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")

        problem = get_object_or_404(Problem, pk=problem_id)

        # does this problem have any scripts? if yes you can't update or delete
        scripts = Script.objects.filter(problem=problem_id)

        if problem.coder.user.id == user.id and not scripts and not problem.make_public:
            return render(request, "share/edit_problem.html", {"problem":problem})
        elif not problem.coder.user.id == user.id:
            return render(request, "share/index.html",
            {"error":"You are not the author of the problem that you tried to edit."})
        elif problem.coder.user.id == user.id:
            return render(request, "share/index.html",
            {"error":"You problem has scripts and you cannot edit it."})
def update_problem(request, problem_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        problem = get_object_or_404(Problem, pk=problem_id)

        if not request.POST["title"] or not request.POST["description"] or not request.POST["discipline"]:
            return render(request, "share/edit_problem.html", {"problem":problem,
            "error":"One of the required fields was empty"})

        else:
            title = request.POST["title"]
            description = request.POST["description"]
            discipline = request.POST["discipline"]

            make_public = request.POST.get('make_public', False)
            print('***********************')
            print('user input make_public:', make_public)    # it shows as on

            if make_public == 'on':
                make_public = True
            else:
                make_public = False

            print('******** Testing *************')
            print('make_public:', make_public)
            print('***********************')

            if problem.coder.user.id == user.id:
                Problem.objects.filter(pk=problem_id).update(title=title,
                description=description, discipline=discipline, make_public=make_public)
                return redirect("share:dashboard")
            else:
                return render(request, "share/edit_problem.html",
                {"problem":problem, "error":"You are not the author of this problem. Can't edit!"})



    else:
        user = request.user
        all_problems = Problem.objects.all()
        return render(request, "share/index.html",
        {"problem":problem, "user": user, "all_problems": all_problems,
        "error":"Can't update!"})
def delete_problem(request, problem_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        problem = get_object_or_404(Problem, pk=problem_id)

        if problem.coder.user.id == user.id and not scripts and not problem.make_public:
            Problem.objects.get(pk=problem_id).delete()
            return redirect("share:dashboard")
        else:
            return render(request, "share/edit_problem.html",
            {"problem":problem, "error":"You are not the author of this problem. Can't delete!"})

    else:
        return HttpResponse(status=500)
def show_script(request, script_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")
        else:
            # make sure to import the fucntion get_object_or_404 from  django.shortcuts
            script = get_object_or_404(Script, pk=script_id)
            problem = get_object_or_404(Problem, pk=script.problem.id)

            # Module 7
            if script.coder.user.id == user.id or script.make_public:
                return render(request, "share/script.html",
                {"user":user, "problem":problem, "script": script})
            else:
                # you are not the author
                all_problems = Problem.objects.all()
                return render(request, "share/index.html",
                {"user":user, "all_problems": all_problems,
                "error":"The script you clicked is not public and you are not the author"})
def edit_script(request, script_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("share:login")

        script = get_object_or_404(Script, pk=script_id)
        problem = get_object_or_404(Problem, pk=script.problem.id)

        if script.coder.user.id == user.id:
            return render(request, "share/edit_script.html", {"user":user, "script":script})

        else:
            return render(request, "share/script.html",
            {"user":user, "script":script, "problem":problem, "error":"You can't edit this script!"})
def update_script(request, script_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        script = get_object_or_404(Script, pk=script_id)
        problem = get_object_or_404(Problem, pk=script.problem.id)

        if not request.POST["title"]:  # this does not work with textarea  form elements
            return render(request, "share/edit_script.html",
            {"user": user, "script":script,
            "error":"One of the required fields was empty"})
        else:
            title = request.POST["title"]
            description = request.POST["description"]
            code = request.POST["code"]
            url = request.POST["url"]
            input = request.POST["input"]
            output = request.POST["output"]
            working_code = request.POST.get('working_code', False)
            make_public = request.POST.get('make_public', False)

            if working_code == 'on':
                working_code = True
            else:
                working_code = False

            if make_public == 'on':
                make_public = True
            else:
                make_public = False

            if script.coder.user.id == user.id:
                Script.objects.filter(pk=script_id).update(title=title,
                description=description, code=code, url=url, output=output,
                input=input, make_public=make_public, working_code=working_code)

                script = get_object_or_404(Script, pk=script_id)  # get new update record

                return render(request, "share/script.html",
                {"user": user, "problem":problem, "script":script,
                "error":"Script updated!"})

            else:
                return render(request, "share/script.html",
                {"user":user, "script":script, "problem":problem,
                "error":"You can't edit this script!"})
    else:
        # the user entering http://127.0.0.1:8000/problem/8/update
        user = request.user
        all_problems = Problem.objects.all()
        return render(request, "share/index.html",
        {"user":user, "all_problems": all_problems, "error":"It was not a POST request!"})
def delete_script(request, script_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)

        script = get_object_or_404(Script, pk=script_id)

        if script.coder.user.id == user.id:
            Script.objects.get(pk=script_id).delete()
            return redirect("share:dashboard")
        else:
            all_problems = Problem.objects.all()
            return render(request, "share/index.html",
            {"user":user, "all_problems": all_problems, "error":"Can't delete the script!"})

    else:
        return HttpResponse(status=500)
