from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Board, Topic, Post
from .forms import NewTopicForm
# Create your views here.


# def home(request):
#     boards = Board.objects.all()
#     board_names = list()
#
#     for board in boards:
#         board_names.append(board.name)
#
#     response_html = '<br>'.join(board_names)
#
#     return HttpResponse(response_html)

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, id):
    # try:
    #     board = Board.objects.get(pk=id)
    # except Board.DoesNotExist:
    #     raise Http404
    board = get_object_or_404(Board, pk = id)
    return render(request, 'topics.html', {'board': board})

# def new_topic(request, id):
#     board = get_object_or_404(Board, pk = id)
#     return render(request, 'new_topic.html', {'board': board})

'''
def new_topic(request, id):
    board = get_object_or_404(Board, pk = id)

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()  # TODO: get the currently logged in user

        topic = Topic.objects.create(
            subject=subject,
            board=board,
            starter=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )

        return redirect('board_topics', id = board.pk)  # TODO: redirect to the created topic page

    return render(request, 'new_topic.html', {'board': board})
'''

def new_topic(request, id):
    board = get_object_or_404(Board, pk=id)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', id = board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


