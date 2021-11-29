from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from users.forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm, DashboardUpdateForm
from users.models import UserTimer
from timer.models import StoredTimer
from timer.Timer import Timer, timers
from django.db.utils import IntegrityError

# Create your views here.
def index(request):
    return redirect("dashboard")


# Create your views here.
def dashboard(request):
    context = {}
    if request.user.is_authenticated:
        timer_ids = UserTimer.objects.filter(user=request.user).order_by('display_order')
        print(timer_ids)
        user_timers = []
        for id in timer_ids:
            timer_data = StoredTimer.objects.get(timer_id=str(id.timers))
            if timer_data.timer_id in timers:
                timers[timer_data.timer_id].set_timer()
                user_timers.append(timers[timer_data.timer_id])
            else:
                timer = Timer(
                    duration=-1, 
                    name=timer_data.timer_id,
                    predictions_url=timer_data.predictions_url,
                    schedule_url=timer_data.schedule_url
                )
                timer.stop_name = timer_data.stop_name
                timer.route_name = timer_data.route_name
                timer.direction_name = timer_data.direction_name
                timers[timer_data.timer_id] = timer
                timer.set_timer()
                user_timers.append(timer)
        context['user_timers'] = user_timers
    else:
        timers['b_timer'].set_timer()
        timers['c_timer'].set_timer()
        timers['d_timer'].set_timer()
        context = {
            'b_display': timers['b_timer'].display,
            'b_seconds_remaining': timers['b_timer'].duration,
            'c_display': timers['c_timer'].display,
            'c_seconds_remaining': timers['c_timer'].duration,        
            'd_display': timers['d_timer'].display,
            'd_seconds_remaining': timers['d_timer'].duration,
        }
    return render(request, "users/dashboard.html", context=context)


@login_required
def edit_dashboard(request):
    timers = UserTimer.objects.filter(user=request.user).order_by('display_order')
    user_timers = []
    for timer in timers:
        timer_data = StoredTimer.objects.get(timer_id=str(timer.timers))
        user_timers.append(timer_data)
    
    context = {'user_timers': user_timers}
    return render(request, "users/edit_dashboard.html", context=context)

@login_required
def delete_timer(request, timer_id):
    timer = UserTimer.objects.filter(user=request.user, timers=timer_id)
    print(timer)
    timer.delete()
    all_timers = UserTimer.objects.filter(user=request.user).order_by('display_order')
    count = 1
    for timer in all_timers:
        timer.display_order = count
        timer.save()
        count += 1
    messages.info(request, "Your timer has been deleted!")
    return redirect("edit_dashboard")

@login_required
def move_up(request, timer_id):
    requested_timer = UserTimer.objects.get(user=request.user, timers=timer_id)
    if requested_timer.display_order > 1:
        swapping_timer = UserTimer.objects.get(user=request.user, display_order=requested_timer.display_order-1)
        requested_timer.display_order -= 1
        requested_timer.save()
        swapping_timer.display_order += 1
        swapping_timer.save()
    return redirect("edit_dashboard")

@login_required
def move_down(request, timer_id):
    user_timers = UserTimer.objects.filter(user=request.user)
    requested_timer = UserTimer.objects.get(user=request.user, timers=timer_id)
    if requested_timer.display_order < max(timer.display_order for timer in user_timers):
        swapping_timer = UserTimer.objects.get(user=request.user, display_order=requested_timer.display_order+1)
        requested_timer.display_order += 1
        requested_timer.save()
        swapping_timer.display_order -= 1
        swapping_timer.save()
    return redirect("edit_dashboard")



def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return render(request, "users/logout.html")


@login_required
def profile(request):
    context = {}
    if request.user.password and request.user.has_usable_password():
        context['has_password'] = True
    return render(request, 'users/profile.html', context=context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    

    context = {
        'u_form': u_form, 
        'p_form': p_form,
    }
    return render(request, 'users/edit_profile.html', context=context)




@login_required
def add_timer(request):
    if request.method == "POST":
        form = DashboardUpdateForm(request.POST)
        if form.is_valid():
            try:
                timers = form.save(commit=False)
                timers.user = request.user
                timers.save()
                messages.success(request, f'Your timer has been saved!')
            except IntegrityError:
                messages.info(request, f'Heads up! This timer is already in your dashboard.')
                pass
    return redirect('dashboard')
