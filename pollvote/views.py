from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Region, User, Competition, PollVote
# Create your views here.

def index(request):
    competitions = Competition.objects.all()
    context = {
        'competitions':competitions
    }
    return render(request, 'pollvote/index.html', context)

def register(request):
    if request.method == "POST":
        print("post method")
        
        email= request.POST.get('email')
        name = request.POST.get('name')
        region = request.POST.get('region')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        
        print("post method is called ")
        
        user = User.objects.filter(email = email).exists()
        if user is True:
            messages.add_message(request, messages.INFO, "email already exists")
            return redirect('register')
        
        elif password != c_password:
            messages.add_message(request, messages.INFO, "password are not matching")
            print("passwords are not matching")
            return redirect('register')
        else:
            
            obj = User.objects.create_user(email=email, name=name, region=region, vote_status='unpolled', password=password)
            obj.save()
            messages.add_message(request, messages.INFO, "user created")           
            return redirect('register')
        
            
    else:
        regions = Region.objects.all()
        print(regions)
        context = {
            'regions':regions
        }
        return render(request, 'pollvote/register.html', context)
    

def loginuser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:       
            login(request, user)
            return redirect('profile')
        else:
            messages.add_message(request, messages.INFO, "user is not exists with this email and password")           
            return redirect('login')
    return render(request, 'pollvote/login.html')

@login_required(login_url='login')
def profile(request):
    competition = Competition.objects.filter(region=request.user.region)
    context = {
            'comp':competition,
            'user':request.user.id
        }
    try:
        myvote = PollVote.objects.get(user = request.user)
        context = {
            'comp':competition,
            'my_vote':myvote
        }
    except PollVote.DoesNotExist as e:
        context = {'vote_message':'poll your vote',
                   'comp':competition,
                   'user':request.user.id
                   }
    return render(request, 'pollvote/userprofile.html', context)


def election_competition(request, slug):
    objs = Competition.objects.get(slug=slug)
    candi_a_votes = objs.candidate_a.total_votes
    candi_b_votes = objs.candidate_b.total_votes
    vote_difference = ""
    if candi_a_votes > candi_b_votes:
        lead = candi_a_votes - candi_b_votes
        vote_difference = f'{objs.candidate_a.candidate_name} is leading with {lead} votes'
    elif candi_a_votes == candi_b_votes:
        vote_difference = f'scores of both candidate are level'
    else:
        lead = candi_b_votes - candi_a_votes
        vote_difference = f'{objs.candidate_b.candidate_name} is leading with {lead} votes'
        
        
    context = {
        'election_sts':objs,
        'leading_votes':vote_difference
    }
    return render(request, 'pollvote/election_compition.html', context)

def logout_user(request):
    
    logout(request)
    return redirect('home')