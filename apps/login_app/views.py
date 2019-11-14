from django.shortcuts import render, redirect, HttpResponse
from .models import User, UserManager, Message, Comment
from django.contrib import messages
from datetime import datetime, timedelta
import bcrypt

# Create your views here.


def index(request):
    return render(request, "index.html")


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        first_name = request.POST["first"]
        last = request.POST["last"]
        email = request.POST["email"]
        pw = request.POST["pw"]
        bday = request.POST["bday"]
        # bday = datetime.strptime(bday, "%Y-%m-%d").date()
        pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        user = User.objects.create(
            first=first_name, last=last, email=email, bday=bday, pw=pw_hash)
        request.session["userid"] = user.id
        return redirect("/success")


def success(request):
    if "userid" in request.session:
        user = User.objects.get(id=request.session["userid"])
        messages = Message.objects.all()
        context = {
            "user": user,

            "messages": messages
        }
        return render(request, "home.html", context)
    else:
        return redirect("/")


def logout(request):
    if "userid" in request.session:
        del request.session["userid"]
    return redirect("/")


def login(request):
    if User.objects.filter(email=request.POST['email']):
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['pw'].encode(), user.pw.encode()):
            request.session["userid"] = user.id
            return redirect("/success")
        else:
            context = {
                "error": "Password is incorrect."
            }
    else:
        context = {
            "error": "There is no account with that email address."
        }
    return render(request, "index.html", context)


def post_message(request):
    userid = request.session["userid"]
    user = User.objects.get(id=userid)
    message = request.POST["message"]
    message = Message.objects.create(user_id=user, message=message)
    return redirect("/success")


def post_comment(request, message_id):
    userid = request.session["userid"]
    user = User.objects.get(id=userid)
    message = Message.objects.get(id=message_id)
    comment = request.POST["comment"]
    comment = Comment.objects.create(
        user_id=user, message_id=message, comment=comment)
    return redirect('/success')


def delete(request, message_id):
    userid = request.session["userid"]
    user = User.objects.get(id=userid)
    message = Message.objects.get(id=message_id)
    now = datetime.now()
    timediff = now - message.created_at
    timediff = timediff.total_minutes()
    if message.user_id.id == user.id and timediff < 30:
        message.delete()
    return redirect("/success")
