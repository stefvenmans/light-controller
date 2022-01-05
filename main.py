import sched, time, requests, json
from datetime import datetime,timedelta
from gpiozero import LED
import logging
logging.basicConfig(filename='logfile.log', encoding='utf-8', level=logging.DEBUG)
logging.info('Software started succesfull')

relay_state = 0;
relay_1 = LED(17);

t_sunrise = 0;
t_sunset = 0;
t_morning = 0;
t_night = 0;

t_sunrise_dt = 0;
t_sunset_dt = 0;
t_morning_dt = 0;
t_night_dt = 0;

t_morning_s = '6:0:0 AM'
t_night_s = '10:30:0 PM'

time_to_set = 0;

def main():
    if(datetime.combine(datetime.today(), datetime.strptime(t_night_s, "%I:%M:%S %p").time())<datetime.now()):
        get_time_data(datetime.today() + timedelta(days=1));
    else:
        get_time_data(datetime.today());
        
    init_relay();
    timer();

def get_time_data(day):
    global t_sunrise
    global t_sunset
    global t_morning
    global t_night
    
    global t_sunrise_dt
    global t_sunset_dt
    global t_morning_dt
    global t_night_dt
    
    utc_1 = timedelta(hours=1);
    winter_time = (3,23)
    sumer_time = (10,30)
    current_time = (day.month, day.day);
    
    if winter_time < current_time < sumer_time:
        winter_summer_offset = timedelta(hours=1);
    else:
        winter_summer_offset = timedelta(hours=0);
    print("Times for " + day.strftime("%Y.%m.%d"));

    response = requests.get('https://api.sunrise-sunset.org/json?lat=50.930062&lng=5.336959&date='+day.strftime("%Y-%m-%d"));
    
    #Sample JSON response
    #json_response =  json.loads('{"results":{"sunrise":"1:2:00 PM","sunset":"1:3:00 PM","solar_noon":"11:42:39 AM","day_length":"16:32:26","civil_twilight_begin":"2:42:33 AM","civil_twilight_end":"8:42:46 PM","nautical_twilight_begin":"1:33:11 AM","nautical_twilight_end":"9:52:07 PM","astronomical_twilight_begin":"12:00:01 AM","astronomical_twilight_end":"12:00:01 AM"},"status":"OK"}')
    
    json_response = json.loads(response.text);
    json_results = json_response['results']
    
    temp = json_results['sunrise']
    in_time = datetime.combine(day, datetime.strptime(temp, "%I:%M:%S %p").time()) + utc_1 + winter_summer_offset
    t_sunrise_dt = in_time;
    t_sunrise = datetime.strftime(in_time, "%H:%M")
    print("Sunrise = " + t_sunrise)

    temp = json_results['sunset']
    in_time = datetime.combine(day, datetime.strptime(temp, "%I:%M:%S %p").time()) + utc_1 + winter_summer_offset
    t_sunset_dt = in_time;
    t_sunset = datetime.strftime(in_time, "%H:%M")
    print("Sunset = " + t_sunset)
    
    temp = t_morning_s
    in_time = datetime.combine(day, datetime.strptime(temp, "%I:%M:%S %p").time()) + utc_1 + winter_summer_offset
    t_morning_dt = in_time;
    t_morning = datetime.strftime(in_time, "%H:%M")
    print("Morning = " + t_morning)
    
    temp = t_night_s
    in_time = datetime.combine(day, datetime.strptime(temp, "%I:%M:%S %p").time()) + utc_1 + winter_summer_offset
    t_night_dt = in_time;
    t_night = datetime.strftime(in_time, "%H:%M")
    print("Night = " + t_night)
    

def timer():
    global time_to_set
    global relay_state
    # Set up scheduler
    s = sched.scheduler(time.time, time.sleep);
    # Schedule when you want the action to occur
    
    if(datetime.today().timestamp()<t_morning_dt.timestamp()):
        time_to_set = t_morning_dt
        relay_state = 1;
    elif(datetime.today().timestamp()<t_sunrise_dt.timestamp()):
        time_to_set = t_sunrise_dt
        relay_state = 0;
    elif(datetime.today().timestamp()<t_sunset_dt.timestamp()):
        time_to_set = t_sunset_dt
        relay_state = 1;
    else:#(datetime.today().timestamp()<t_night_dt.timestamp()):
        time_to_set = t_night_dt
        relay_state = 0
        get_time_data(datetime.today() + timedelta(days=1));
    
    print("Timer set for : ", time_to_set.strftime("%d.%m.%Y - %H:%M"));
    
    s.enterabs(time_to_set.timestamp(), 0, update_relay,argument = ());
    # Block until the action has been run
    s.run();
    timer();
    
def update_relay():
    print("Lights : ", relay_state);
    message = 'Relay status: ' + str(relay_state)
    logging.info(message)
    if(relay_state == 0):
        print("off")
        relay_1.on();
    elif(relay_state == 1):
        print("on")
        relay_1.off();
    #print();
    
def init_relay():
    global relay_state
    if(datetime.today().timestamp()<t_morning_dt.timestamp()):
        relay_state = 0;
    elif(datetime.today().timestamp()<t_sunrise_dt.timestamp()):
        relay_state = 1;
    elif(datetime.today().timestamp()<t_sunset_dt.timestamp()):
        relay_state = 0;
    else:#(datetime.today().timestamp()<t_night_dt.timestamp()):
        relay_state = 1
    update_relay();
    
main();
