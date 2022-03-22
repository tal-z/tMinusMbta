
#from dotenv import load_dotenv
from requests import session
import datetime
from time import sleep
import math
import os
import pytz

#load_dotenv()

est = pytz.timezone('America/New_York')


sess = session()
API_KEY = os.getenv('MBTA_API_KEY')


# Custom function to round numbers in the normal human way, and not the bizarre python way.
def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier



class Timer:
    """Class to hold and modify attributes related to
    keeping time,
    keeping track of status alerts,
    and logic for displaying messages to the end user"""

    def __init__(self, name, predictions_url, schedule_url,duration=0):
        self.name = name
        self.predictions_url = predictions_url
        self.predictions = sess.get(self.predictions_url, headers={"x-api-key": API_KEY}).json()
        self.schedule_url = schedule_url
        self.schedule = sess.get(self.schedule_url, headers={"x-api-key": API_KEY}).json()
        self.duration = duration
        self.arrival_time = None
        self.departure_time = None
        self.status = None
        self.display = None

    @property
    def time_until_arrival(self):
        current_time = datetime.datetime.now(est)
        return est.localize(self.arrival_time) - current_time




    def decrement(self):
        """
        DEPRECATED. This functionality was moved to JavaScript. 
        This ticks down the timer.       
        """
        sleep(1)
        if self.duration > 0:
            self.duration -= 1
        return self.duration


    def set_display(self):
        print(self.duration)
        if self.status == 'No Live Prediction Available':
            if self.duration <= 30:
                self.display = 'Arriving - Not Live'
            elif self.duration <= 60:
                self.display = 'Approaching - Not Live'
            elif self.duration > 60:
                val = self.duration / 60
                minutes = int(round_half_up(val))
                if minutes > 20:
                    self.display = '20+ min - Not Live'
                else:
                    self.display = f'{minutes} min - Not Live'
        elif self.status:
            self.display = self.status
        elif self.duration <= 30:
            self.display = 'Arriving'
        elif self.duration <= 60:
            self.display = 'Approaching'
        elif self.duration > 60:
            val = self.duration/60
            minutes = int(round_half_up(val))
            if minutes > 20:
                self.display = '20+ min'
            else:
                self.display = f'{minutes} min'
        return self.display

    def set_schedule(self):
        print('checking for schedule')
        print(API_KEY)
        self.schedule = sess.get(self.schedule_url, headers={"x-api-key": API_KEY}).json()
        #print(self.schedule)

        if 'data' in self.schedule:
            future_schedules = self.schedule['data']
            future_schedules = [sched for sched in future_schedules if
                                sched['attributes']['departure_time'] is not None]
            future_schedules = [sched for sched in future_schedules if
                                est.localize(datetime.datetime.strptime(sched['attributes']['departure_time'],
                                                           '%Y-%m-%dT%H:%M:%S-04:00'))
                                > datetime.datetime.now(est)]
            if future_schedules:
                future_schedules = sorted(future_schedules,
                                          key=lambda x: datetime.datetime.strptime(
                                              x['attributes']['departure_time'],
                                              '%Y-%m-%dT%H:%M:%S-04:00'))
                #print("future schedules:", future_schedules)
                upcoming_schedule = future_schedules[0]
                self.status = 'No Live Prediction Available'
                self.arrival_time = datetime.datetime.strptime(
                    upcoming_schedule['attributes']['departure_time'],
                    '%Y-%m-%dT%H:%M:%S-04:00')
                self.duration = self.time_until_arrival.seconds


    def set_prediction(self):
        response = sess.get(self.predictions_url, headers={"x-api-key": API_KEY})
        self.predictions = response.json()
        print("checking for predictions")
        print("URL:", self.predictions_url)
        print(self.predictions)
        print(response.headers)

        if 'data' in self.predictions:
            if self.predictions['data']:
                json_data = self.predictions['data']
                future_predictions = [pred for pred in json_data
                                      if pred['attributes']['departure_time'] is not None]
                if not future_predictions:
                    future_predictions = [pred for pred in json_data
                                          if pred['attributes']['arrival_time'] is not None]
                try:
                    future_predictions = [pred for pred in future_predictions
                                        if est.localize(datetime.datetime.strptime(pred['attributes']['arrival_time'],
                                                                        '%Y-%m-%dT%H:%M:%S-04:00'))
                                        > datetime.datetime.now(est)]
                except TypeError: 
                    future_predictions = []
                    
                print("current time: ", datetime.datetime.now(est))
                print("filtered predictions:", future_predictions)
                if future_predictions:
                    future_predictions = sorted(future_predictions,
                                                key=lambda x: datetime.datetime.strptime(
                                                    x['attributes']['arrival_time'],
                                                    '%Y-%m-%dT%H:%M:%S-04:00'))
                    upcoming_prediction = future_predictions[0]
                    print("upcoming prediction:", upcoming_prediction)
                    self.status = upcoming_prediction['attributes']['status']
                    self.arrival_time = datetime.datetime.strptime(upcoming_prediction['attributes']['arrival_time'],
                                                                   '%Y-%m-%dT%H:%M:%S-04:00')
                    self.duration = self.time_until_arrival.seconds
                else:
                    self.set_schedule()
            else:
                self.set_schedule()
        else:
            self.set_schedule()

    def set_timer(self):
        try:
            self.set_prediction()
        except TypeError:
            self.status = 'type error'
            self.arrival_time = None
            self.duration = -99
        except IndexError:
            self.status = 'index error'
            self.arrival_time = None
            self.duration = -99
        except KeyError:
            self.status = 'key error'
            self.arrival_time = None
            self.duration = -99

        self.set_display()




b_countdown = 30
c_countdown = 20
d_countdown = 10

b_timer = Timer(duration=b_countdown,
                name='b',
                predictions_url='https://api-v3.mbta.com/predictions'
                                '?filter[stop]=place-chill'
                                '&filter[route]=Green-B'
                                '&filter[direction_id]=1',
                schedule_url='https://api-v3.mbta.com/schedules'
                             '?filter[stop]=place-chill'
                             '&filter[route]=Green-B'
                             '&filter[direction_id]=1')
c_timer = Timer(duration=c_countdown,
                name='c',
                predictions_url='https://api-v3.mbta.com/predictions'
                                '?filter[stop]=place-clmnl'
                                '&filter[route]=Green-C'
                                '&filter[direction_id]=1',
                schedule_url='https://api-v3.mbta.com/schedules'
                             '?filter[stop]=place-clmnl'
                             '&filter[route]=Green-C'
                             '&filter[direction_id]=1')
d_timer = Timer(duration=d_countdown,
                name='d',
                predictions_url='https://api-v3.mbta.com/predictions'
                                '?filter[stop]=place-rsmnl'
                                '&filter[route]=Green-D'
                                '&filter[direction_id]=1',
                schedule_url='https://api-v3.mbta.com/schedules'
                             '?filter[stop]=place-rsmnl'
                             '&filter[route]=Green-D'
                             '&filter[direction_id]=1')

timers = {'b_timer': b_timer, 'c_timer': c_timer, 'd_timer': d_timer}