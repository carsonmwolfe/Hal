from datetime import datetime

days = {
        0:"Monday",
        1:"Tuesday",
        2:"Wednesday",
        3:"Thursday",
        4:"Friday",
        5:"Saturday",
        6:"Sunday",
        }
months={
        1:"January",
        2:"February",
        3:"March",
        4:"April",
        5:"May",
        6:"June",
        7:"July",
        8:"August",
        9:"September",
        10:"October",
        11:"November",
        12:"December"
        }

endings={
        1:"st",
        2:"nd",
        3:"rd"
        }

def get_footer():
    
    now = datetime.now()
    weekday = days.get(datetime.today().weekday())
    month = months.get(int(now.strftime("%m")))
    year = now.strftime("%Y")
    hour=int(now.strftime("%H"))
    minute=now.strftime("%M")
    day=int(now.strftime("%d"))
    ampm="AM"
    if hour>=12:
        ampm="PM"
    if hour>12:
        hour= hour-12
    if hour == 0:
        hour = "12"
    if day<4:
        ending=endings.get(int(day))
    else:
        ending="th"
    footer = ("HAL | "+weekday+" "+month+" "+str(day)+ending+", "+str(year)+" at "+str(hour)+":"+minute+" "+ampm+" PST")
    return footer
