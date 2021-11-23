from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .Timer import Timer, timers
from users.forms import DashboardUpdateForm
from timer.forms import StoredTimerForm
from timer.models import StoredTimer
from users.models import UserTimer



def index(request):
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
    return render(
        request, "timer/index.html", context=context)


def new_timer(request):
    try:
        display_order = -1
        if request.user.is_authenticated:
            display_order = UserTimer.objects.filter(user=request.user)
            display_order = max([item.display_order for item in display_order] + [0]) + 1
        if request.method == 'POST':
            # Parse form data from post request
            stop_id = request.POST['stopid']
            route_id = request.POST['routeid']
            direction_id = request.POST['direction-options']
            timer_id = f"{stop_id}_{route_id}_{direction_id}".replace("-", "_")
            stop_name = request.POST['search']
            route_name = request.POST['route-name']
            direction_name = request.POST['direction-name']

            # Store timer_id in session, so that it can be referenced 
            # by users who aren't logged in or who haven't yet saved their current timer.

            # Format URLs for requesting predictions and schedule data from MBTA API
            predictions_url = f'https://api-v3.mbta.com/predictions/?filter[stop]={stop_id}&filter[route]={route_id}&filter[direction_id]={direction_id}'
            schedule_url=f'https://api-v3.mbta.com/schedules/?filter[stop]={stop_id}&filter[route]={route_id}&filter[direction_id]={direction_id}'
            
            request.session["timer_id"] = timer_id
            request.session["predictions_url"] = predictions_url
            request.session["schedule_url"] = schedule_url
            request.session["stop_name"] = stop_name
            request.session["route_name"] = route_name
            request.session["direction_name"] = direction_name

            # Create a new Timer object, which will be passed to the NewTimer view
            new_timer = Timer(duration=-1, predictions_url=predictions_url, schedule_url=schedule_url, name=timer_id)
            new_timer.stop_name = stop_name
            new_timer.route_name = route_name
            new_timer.direction_name = direction_name
            new_timer.set_timer()
            timers[timer_id] = new_timer
            
            
            # Store the timer's attributes in our DB
            if not StoredTimer.objects.filter(timer_id=timer_id):
                stored_timer_form = StoredTimerForm(data={
                    'stop_id': stop_id,
                    'route_id': route_id,
                    'direction_id': direction_id,
                    'timer_id': timer_id,
                    'predictions_url': predictions_url,
                    'schedule_url': schedule_url,
                    'stop_name': stop_name,
                    'route_name': route_name,
                    'direction_name': direction_name,
                    }
                )
                if stored_timer_form.is_valid():
                    stored_timer_form.save() 



            dash_update_form = DashboardUpdateForm(initial={'timers': timer_id, "display_order": display_order})
            context = {
                "stop_name":  new_timer.stop_name,
                "route_name": new_timer.route_name,
                "direction_name": new_timer.direction_name,
                "new_display": new_timer.display,
                "new_seconds_remaining": new_timer.duration,
                "timer_id": timer_id,
                "dash_update_form": dash_update_form,
                }
        else:
            timer_id = request.session["timer_id"]
            if timer_id in timers:
                new_timer = timers[timer_id]
                new_timer.set_timer()
            else:
                predictions_url = request.session["predictions_url"]
                schedule_url = request.session["schedule_url"]
                new_timer = Timer(duration=-1, predictions_url=predictions_url, schedule_url=schedule_url, name=timer_id)
                new_timer.set_timer()
                timers[timer_id] = new_timer

            dash_update_form = DashboardUpdateForm(initial={'timers': timer_id, "display_order": display_order})
            context = {
                "stop_name":  request.session["stop_name"],
                "route_name": request.session["route_name"],
                "direction_name": request.session["direction_name"],
                "new_display": new_timer.display,
                "new_seconds_remaining": new_timer.duration,
                "dash_update_form": dash_update_form,
                }
        return render(request, 'timer/NewTimer.html', context)
    except KeyError:
        return render(request, "timer/CreateTimer.html")

def create_timer(request):
    return render(request, 'timer/CreateTimer.html')


