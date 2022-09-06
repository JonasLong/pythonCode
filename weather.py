#This is a program that generates fake weather forecasts
#This can be imported and called from other python programs

import random

def forecast(place='Null Island', *args):
    place=str(place)
    current_weather = random.choice(['sunny', 'cloudy', 'stormy', 'foggy', 'snowing', 'sleeting', 'hailing', 'windy', 'humid'])
    percent_chance = random.randint(1,101)
    percent_chance = str(percent_chance)
    future_weather = random.choice(['rain', 'thunder and lightning', 'clouds', 'increased humidity', 'high winds', 'fog', 'storms', 'hail', 'sleet', 'tornado', 'snow', 'solar flare', 'tsunami', 'zombie apocalypse', 'raining tacos', 'wildfire', 'avalanche', 'sand storms', 'drought'])
    print(' '.join(['Right now, in', place+',', 'it is', current_weather, 'with a', percent_chance, 'percent chance of', future_weather+'.']))
    
if(__name__=="__main__"):
    forecast()
