from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        now = datetime.now()
        maxdate = now.replace(year=now.year - 13).date()
        bday = postData['bday']
        print(f"bday from form: {bday}")
        print(f"max date is {maxdate}")
        if len(postData['first'])<2 :
            errors['first'] = "First name should be at least 2 characters"
        if len(postData['last'])<2:
            errors['last']= "Last name should be at least 2 characters"
        if len(postData['pw'])<2:
            errors['pw']= "Password should be at least 8 characters"
        if postData['pw'] != postData['pw2']:
            errors['pw2'] = "Passwords do not match"
        if User.objects.filter(email = postData['email']):
            errors['email_not_unique']="Email address already is used for an existing account"
        if bday == "":
            errors['bday_required']="Birthday is a required field"
        else:
            bday = datetime.strptime(postData['bday'], "%Y-%m-%d").date()
            if maxdate <= bday:
                errors['age']="You must be at least 13 years old to register"
        try:
            validate_email(postData['email'])
        except ValidationError:
            errors["email"] = "Invalid email"
        return errors

class User(models.Model):
    first = models.CharField(max_length=45)
    last = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    bday = models.DateField(null=True)
    pw =models.CharField(max_length=180)
    objects = UserManager()
    #user_comments

class Message(models.Model):
    user_id= models.ForeignKey(User,related_name="user_messages", on_delete=models.CASCADE)
    message = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #message_comments

class Comment(models.Model):
    message_id = models.ForeignKey(Message,related_name="message_comments", on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,related_name="user_comments", on_delete=models.CASCADE)
    comment = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)