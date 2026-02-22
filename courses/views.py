from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required # The Lock
from django.contrib.auth.forms import UserCreationForm    # The Signup Form
from django.contrib.auth import login                     # To auto-login after signup
from .models import Lesson

# 1. The Home Page
def home(request):
    all_lessons = Lesson.objects.all()
    return render(request, 'home.html', {'lessons': all_lessons})

# 2. The Lesson Page (LOCKED!)
@login_required(login_url='login')  # <--- This is the magic lock
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'lesson_detail.html', {'lesson': lesson})

# The "Mark as Complete" Action
@login_required(login_url='login')
def mark_complete(request, lesson_id):
    # Find the lesson
    lesson = get_object_or_404(Lesson, id=lesson_id)
    # Add the currently logged-in student to the completed list!
    lesson.completed_by.add(request.user)
    # Send them back to the homepage
    return redirect('home')

# 3. The Signup Logic
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log them in immediately
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# 4. The SMART Chatbot Brain
def chatbot_api(request):
    # 1. Grab what the student typed
    user_message = request.GET.get('message', '').lower()
    
    # 2. Handle basic greetings
    if user_message in ['hi', 'hello', 'hey', 'help']:
        bot_reply = "Hi! I am your AI Study Assistant. Tell me what topic you want to learn (like 'Python')!"
        return JsonResponse({'reply': bot_reply})
        
    # 3. THE UPGRADE: Search the Database!
    # __icontains tells Django to search the titles ignoring uppercase/lowercase
    matching_lessons = Lesson.objects.filter(title__icontains=user_message)
    
    # 4. If we found a match, build a clickable HTML link!
    if matching_lessons.exists():
        bot_reply = "I found these lessons for you:<br>"
        for lesson in matching_lessons:
            # We are writing raw HTML that the chat window will turn into a real link
            bot_reply += f"<br>📘 <a href='/lesson/{lesson.id}/' style='color: #007bff; text-decoration: underline;'><b>{lesson.title}</b></a>"
    else:
        # If no lessons match what they typed
        bot_reply = "I don't see a lesson on that exact topic yet. Try searching for a different keyword!"
        
    return JsonResponse({'reply': bot_reply})