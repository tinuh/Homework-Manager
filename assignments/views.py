from django.shortcuts import render
from classes.models import Class
from classes.models import class_linker
from .models import Assignment
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from .models import Model_assignment

# Create your views here.
@login_required
def view(request):
    profile = Profile.objects.get(user_id = request.user.id)
    if profile.teacher == False:
        response = '/homework/student/view'
    elif profile.teacher == True:
        response = '/homework/teacher/view'
    else:
        response = '/denied'
    return redirect(response)

@login_required
def add(request):
    profile = Profile.objects.get(user_id = request.user.id)
    if profile.teacher == False:
        response = '/homework/student/add'
    elif profile.teacher == True:
        response = '/homework/teacher/add'
    else:
        response = '/denied'
    return redirect(response)

@login_required
def assignmentsTeacher(request, *args, **kwargs):
    classes = Class.objects.all()
    assignments = Assignment.objects.all()
    model_assignments = Model_assignment.objects.all()
    assignmentNames = []
    count = -1

    for model_assignment in model_assignments:
        if model_assignment.linked_teacher == request.user:
            count += 1
            assignmentNames.append([model_assignment, [0, 0]])
            for assignment in assignments:
                if assignment.linked_model_assignment == model_assignment:
                    if assignment.done == True:
                        assignmentNames[count][1][0] += 1
                    else:
                        assignmentNames[count][1][1] += 1

    assignmentCount = len(assignmentNames)

    context = {
        'classes': classes,
        'assignmentNames': assignmentNames,
        'assignmentCount': assignmentCount,
    }

    print(args, kwargs)
    print(request.user)
    return render(request, 'assignments/teacher/index.html', context)


@login_required
def assignmentsStudent(request, *args, **kwargs):
    classes = Class.objects.all()

    if request.method == "POST":
        assignment = Assignment.objects.get(id=request.POST.get("assign-id"))
        assignment.submission = request.POST.get("submission")
        if "save_draft" not in request.POST:
            assignment.done = True
        assignment.save()

        return redirect("/homework/student/view/" + str(assignment.id))
    else:
        assignments = Assignment.objects.filter(user_id=request.user.id)
        AssignmentsA = 0
        AssignmentsD = 0

        for assignment in assignments:
            if assignment.user == request.user and assignment.done == False:
                AssignmentsA += 1

        for assignment in assignments:
            if assignment.user == request.user and assignment.done == True:
                AssignmentsD += 1


        context = {
            'classes': classes,
            'assignments': assignments,
            'AssignmentsA': AssignmentsA,
            'AssignmentsD': AssignmentsD,
        }

        print(args, kwargs)
        print(request.user)
        return render(request, 'assignments/student/index.html', context)

@login_required
def assignmentStudent_add(request, *args, **kwargs):
    classes = Class.objects.all()
    assignments = Assignment.objects.all()

    context = {
        'classes': classes,
        'assignments': assignments,
    }

    if request.method == "POST":
        assignments = Assignment()
        assignments.name = request.POST.get('name')
        assignments.description = request.POST.get('description')
        assignments.user_id = request.user.id
        assignments.save()

        response = redirect('/homework/view')
        return response
    print(args, kwargs)
    print(request.user)
    return render(request, 'assignments/student/add.html', context)

@login_required
def assignmentTeacher_add(request, *args, **kwargs):
    classes = Class.objects.all()
    assignments = Assignment.objects.all()
    classess = []

    for classe in classes:
        if classe.teacher_id == request.user.id:
            classess.append(classe)

    classes = classess
    context = {
        'classes': classes,
        'assignments': assignments,
    }

    if request.method == "POST":
        class_link = class_linker.objects.all()
        model_assiginments = Model_assignment.objects.all()
        try:
            model_assiginment = Model_assignment(name = request.POST.get('name'),description = request.POST.get('description') ,linked_teacher_id = request.user.id, linked_class_id = request.POST.get('class'))
            class_object = Class.objects.get(id=int(str(request.POST.get('class')))).id
            model_assiginment.save()
        except:
            return render(request, 'assignments/teacher/add.html', context)

        for student in class_link:
            if str(student.enrolled_class.id) == str(request.POST.get('class')):
                assignments = Assignment(name = request.POST.get('name'), description = request.POST.get('description'), linked_class_id = request.POST.get('class'), user_id = student.linked_user.id, linked_model_assignment_id = int(model_assiginment.id), linked_class_linker_id = int(student.id))
                assignments.save()


        response = redirect('/class/teacher/view/' + str(class_object))
        return response
    print(args, kwargs)
    print(request.user)
    return render(request, 'assignments/teacher/add.html', context)

@login_required
def deleteStudent(request, *args, id):

    assignment = Assignment.objects.get(pk = id)
    assignment.delete()

    response = redirect("/homework/view")
    return response

@login_required
def done(request, *args, id):

    assignment = Assignment.objects.get(pk = id)
    assignment.done = True
    assignment.save()

    response = redirect("/homework/view")
    return response

@login_required
def undone(request, *args, id):

    assignment = Assignment.objects.get(pk = id)
    assignment.done = False
    assignment.save()

    response = redirect("/homework/view")
    return response

def delete(request, *args, **kwargs):
    id = kwargs['id']
    try:
        assignment = Assignment.objects.get(pk=id)
    except:
        return redirect('/denied')
    if assignment.user.id == request.user.id:
        assignment.delete()

        response = redirect('/homework/view')
        return response
    else:
        response = redirect('/denied')
        return response

def model_delete(request, *args, **kwargs):
    id = kwargs['id']
    try:
        assignment = Model_assignment.objects.get(pk=id)
    except:
        return redirect('/denied')
    if assignment.linked_teacher.id == request.user.id:
        if kwargs['class'] == "1":
            classid = assignment.linked_class.id
            assignment.delete()
            response = redirect('/class/teacher/view/' + str(classid))
        else:
            assignment.delete()
            response = redirect('/homework/view')

        return response
    else:
        response = redirect('/denied')
        return response

def studentAssignmentSpecific(request, *args, **kwargs):
    id = kwargs['id']

    try:
        assignment = Assignment.objects.get(pk = id)
    except:
        return redirect("/denied")

    if request.method == "POST":
        assignment.submission = request.POST.get("submission")
        if "save_draft" not in request.POST:
            assignment.done = True
        assignment.save()
        
        return redirect("/homework/student/view/" + str(assignment.id))
    else:
        context = {
            'assignment': assignment,
        }

        if assignment.user.id == request.user.id:
            return render(request, "assignments/student/view.html", context)
        else:
            return redirect("/denied")


def teacherAssignmentSpecific(request, *args, **kwargs):
    id = kwargs['id']

    try:
        assignmentM = Model_assignment.objects.get(pk = id)
    except:
        return redirect("/denied")

    assignmentsS = Assignment.objects.filter(linked_model_assignment_id = assignmentM.id)
    done = []
    notdone = []
    for assignment in assignmentsS:
        if assignment.done:
            done.append(assignment)
        else:
            notdone.append(assignment)

    context = {
        'assignment': assignmentM,
        'done': done,
        'doneC': len(done),
        'notdone': notdone,
        'notdoneC': len(notdone),
    }

    if request.user.profile.teacher and assignmentM.linked_teacher.id == request.user.id:
        return render(request, "assignments/student/view.html", context)
    else:
        return redirect("/denied")

def teacher_edit(request, *args, **kwargs):
    id = kwargs["id"]

    if request.method != "POST":
        try:
            assignment = Model_assignment.objects.get(pk = id)
        except:
            return redirect('/denied')
    else:
        assignment = Model_assignment.objects.get(pk=id)

    classes = Class.objects.all()
    classess = []

    for classe in classes:
        if classe.teacher_id == request.user.id:
            classess.append(classe)
            
    context = {
        'assignment': assignment,
        'classes': classess,
    }

    old_class = assignment.linked_class_id
    
    if request.method == "POST":
        assignment.linked_class_id = classe = request.POST.get('class')
        assignment.name = name = request.POST.get('name')
        assignment.description = request.POST.get('description')
        assignment.save()
        assignment = Model_assignment.objects.get(pk=id)

        linked_assignments = Assignment.objects.filter(linked_model_assignment_id = assignment.id)

        if assignment.linked_class_id == old_class:
            for assign in linked_assignments:
                assign.name = assignment.name
                assign.description = assignment.description
                assign.save()
        else:
            for assign in linked_assignments:
                assign.delete()

            links = class_linker.objects.get(enrolled_class_id=assignment.linked_class_id)

            for person in links:
                assign = Assignment()
                assign.name = assignment.name
                assign.description = assignment.description
                assign.linked_class_id = person.enrolled_class.id
                assign.linked_class_linker_id = person.id
                assign.linked_model_assignment_id = assignment.id
                assign.save()
        
        return redirect("/homework/teacher/view/" + str(assignment.id))
    else:
        if not request.user.profile.teacher:
            return redirect('/denied')

        return render(request, 'assignments/teacher/edit.html', context)

def teacherAssignmentStudentSpecific(request, *args, **kwargs):
    id = kwargs['id']

    try:
        assignment = Assignment.objects.get(pk = id)
    except:
        return redirect("/denied")

    if request.method == "POST":
        assignment.submission = request.POST.get("submission")
        assignment.done = True
        assignment.save()
        
        return redirect("/homework/teacher/student/view/" + str(assignment.id))
    else:
        context = {
            'assignment': assignment,
        }

        if request.user.profile.teacher and assignment.linked_class.teacher_id == request.user.id:
            return render(request, "assignments/teacher/view.html", context)
        else:
            return redirect("/denied")