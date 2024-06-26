import streamlit as st
import time

st.set_page_config(layout="wide")

st.title("Welcome to Flight Finder")
st.subheader("Did you know that not all connecting flight combinations are searchable on Google Flights? Flight Finder finds hidden flight combinations not marketed by the airlines or on Google Flights.")

#    with st.spinner('finding hidden flights...connecting you to the world.'):
#        time.sleep(5)
#    st.success('start exploring!')

Origin = st.text_input("Origin Airport Code", 'ORD')
Dest = st.text_input("Destination Airport Code")
Date = '2024-08-01'

with st.status("finding hidden flights...connecting you to the world.", expanded=True) as status:
   st.write("(step 1/3) finding layover points...")
   time.sleep(10)
   st.write("(step 2/3) finding flights...")
   time.sleep(35)
   st.write("(step 3/3) comparing prices...")

   import pandas as pd
   import requests
   import re
   from bs4 import BeautifulSoup
   import streamlit as st
   from datetime import datetime
   from datetime import timedelta
   import streamlit as st
   from st_aggrid import AgGrid, GridUpdateMode, JsCode
   from st_aggrid.grid_options_builder import GridOptionsBuilder
   import streamlit.components.v1 as components
   
   # Origin = 'ORD'
   # Dest = 'AKL'
   # Date = '2024-08-01'
   Minlayover = 2
   Convertdate = datetime.strptime(Date, "%Y-%m-%d")
   Nextdateraw = Convertdate + timedelta(days=1)
   Nextdate = Nextdateraw.strftime('%Y-%m-%d')
   
   URL = 'https://direct-flights.com/chicago-{}'.format(Origin)
   page = requests.get(URL)
   
   # print(page.text)
   
   soup = BeautifulSoup(page.content, "html.parser")
   
   results = soup.find(id='root')
   
   # print(results)
   
   destinations = results.find_all('div', class_='list-value-grow')
   
   originiata = []
   origincity = []
   
   for destination in destinations:
     #print(destination.text)
     info = destination.text
     iata = info[info.find('(')+1:info.find(')')]
     city = info[0:info.find('(')-1]
     originiata.append(iata)
     origincity.append(city)
     # print(info)
     # print(iata)
     # print(city)
     # print()
     # print(iata)
   
   origindf = pd.DataFrame({'iata':originiata,'city':origincity})
   
   # print(URL)
   # print(origindf)
   
   URL = 'https://direct-flights.com/chicago-{}'.format(Dest)
   page = requests.get(URL)
   
   # print(page.text)
   
   soup = BeautifulSoup(page.content, "html.parser")
   
   results = soup.find(id='root')
   
   # print(results)
   
   destinations = results.find_all('div', class_='list-value-grow')
   
   destiata = []
   destcity = []
   
   for destination in destinations:
     #print(destination.text)
     info = destination.text
     iata = info[info.find('(')+1:info.find(')')]
     city = info[0:info.find('(')-1]
     destiata.append(iata)
     destcity.append(city)
     # print(info)
     # print(iata)
     # print(city)
     # print()
     # print(iata)
   
   destdf = pd.DataFrame({'iata':destiata,'city':destcity})
   
   layoverpoints = pd.merge(origindf, destdf, on=['iata','city'], how='inner')
   # print(layoverpoints)
   
   googleurlsleg1 = []
   googleurlsleg2 = []
   
   for i in layoverpoints.iata:
     googleurlsleg1 += [
     'https://www.google.com/travel/flights?hl=en&q=Flights%20to%20{dest}%20from%20{origin}%20on%20{date}%20oneway%20nonstop'.format(
         dest = i.lower(),
         origin = Origin.lower(),
         date = Date
     )
     ]
     googleurlsleg1 += [
     'https://www.google.com/travel/flights?hl=en&q=Flights%20to%20{dest}%20from%20{origin}%20on%20{date}%20oneway%20nonstop'.format(
         dest = i.lower(),
         origin = Origin.lower(),
         date = Nextdate
     )
   ]
   
   for i in layoverpoints.iata:
     googleurlsleg2 += [
     'https://www.google.com/travel/flights?hl=en&q=Flights%20to%20{dest}%20from%20{origin}%20on%20{date}%20oneway%20nonstop'.format(
         dest = Dest.lower(),
         origin = i.lower(),
         date = Date
     )
     ]
     googleurlsleg2 += [
     'https://www.google.com/travel/flights?hl=en&q=Flights%20to%20{dest}%20from%20{origin}%20on%20{date}%20oneway%20nonstop'.format(
         dest = Dest.lower(),
         origin = i.lower(),
         date = Nextdate
     )
   ]
   
   # print(googleurls)
   
     layover = []
     prices = []
     cleanprices = []
     times = []
     airlines = []
     totaltimes = []
     stops = []
     logourls = []
     adttms = []
     ddttms = []
   
   for i in googleurlsleg1:
   
     URL = i
     page = requests.get(URL)
     
     # print(page.text)
     
     soup = BeautifulSoup(page.content, "html.parser")
     
     results = soup.find(id='yDmH0d')
     
     # print(results)
     
     flights = results.find_all('li', class_='pIav2d')
     
     # experimenting with clicks in selenium to get to spans within each flight
     # driver.find_element_by_xpath("//button[@class='button__373c0__3lYgT secondary__373c0__1bsQo activated__373c0__1moG8 ']").click()
     
     # spans = flight.find_all('span')
     # for span in spans:
     #     print(span.text)
     
     for flight in flights:
         layoveriata = str(i)[61:64].upper()
         price = str(flight.find('div', class_='BVAVmf I11szd POX3ye').text)
         cleanprice = price[price.find('$')+1:len(price)]
         time = str(flight.find('div', class_='zxVSec YMlIz tPgKwe ogfYpf').text)
         airline = str(flight.find('div', class_='sSHqwe tPgKwe ogfYpf').text)
         totaltime = str(flight.find('div', class_='gvkrdb AdWm1c tPgKwe ogfYpf').text)
         stop = str(flight.find('div', class_='EfT7Ae AdWm1c tPgKwe').text)
         logo = str(flight.find('div', class_='EbY4Pc P2UJoe'))
         logoclean = logo[logo.find('(')+1:logo.find(')')]
         # flightno = flight.find_all('span', attrs = {'class' : 'Xsgmwe QS0io'})
         dtime = time[time.find('M')+1:time.find('on')-1]
         dstring = time[time.find(',')+2:time.find('–')-1]
         ddate = dstring[-2:].lstrip(' ').zfill(2)
         ddttmstr = Date[:4]+dstring[:3]+ddate+dtime
         atime = time[time.find('–')+2:time.find('M',time.find('–')+2)+1]
         astring = time[time.find('on',time.find('–')+2)+8:len(time)]
         adate = astring[-2:].lstrip(' ').zfill(2)
         adttmstr = Date[:4]+astring[:3]+adate+atime
         ddttm = datetime.strptime(ddttmstr, '%Y%b%d%I:%M %p')
         adttm = datetime.strptime(adttmstr, '%Y%b%d%I:%M %p')
         ddttms.append(ddttm)
         adttms.append(adttm)
         layover.append(layoveriata)
         prices.append(price)
         cleanprices.append(cleanprice)
         times.append (time)
         airlines.append(airline)
         totaltimes.append(totaltime)
         stops.append(stop)
         logourls.append(logoclean)
     # print(price)
     # print(time)
     # print(airline)
     # print(totaltime)
     # print(stop)
     # print()
   
   leg1flightsdf = pd.DataFrame({'layover':layover,'price':prices,'cleanprice':cleanprices,'time':times,'airline':airlines,'totaltime':totaltimes,'stops':stops,'logo':logourls,'departuretime':ddttms,'arrivaltime':adttms})
   
   layover = []
   layovername = []
   prices = []
   cleanprices = []
   times = []
   airlines = []
   totaltimes = []
   stops = []
   logourls = []
   adttms = []
   ddttms = []
   
   for i in googleurlsleg2:
   
     URL = i
     page = requests.get(URL)
     
     # print(page.text)
     
     soup = BeautifulSoup(page.content, "html.parser")
     
     results = soup.find(id='yDmH0d')
     
     # print(results)
     
     flights = results.find_all('li', class_='pIav2d')
     
     # experimenting with clicks in selenium to get to spans within each flight
     # driver.find_element_by_xpath("//button[@class='button__373c0__3lYgT secondary__373c0__1bsQo activated__373c0__1moG8 ']").click()
     
     # spans = flight.find_all('span')
     # for span in spans:
     #     print(span.text)
     
     for flight in flights:
         layoveriata = str(flight.find('div', class_='QylvBf').text)[:3]
         layoverairport = str(flight.find('div', class_='QylvBf').text)[-len(str(flight.find('div', class_='QylvBf').text))+3:]
         price = str(flight.find('div', class_='BVAVmf I11szd POX3ye').text)
         cleanprice = price[price.find('$')+1:len(price)]
         time = str(flight.find('div', class_='zxVSec YMlIz tPgKwe ogfYpf').text)
         airline = str(flight.find('div', class_='sSHqwe tPgKwe ogfYpf').text)
         totaltime = str(flight.find('div', class_='gvkrdb AdWm1c tPgKwe ogfYpf').text)
         stop = str(flight.find('div', class_='EfT7Ae AdWm1c tPgKwe').text)
         logo = str(flight.find('div', class_='EbY4Pc P2UJoe'))
         logoclean = logo[logo.find('(')+1:logo.find(')')]
         dtime = time[time.find('M')+1:time.find('on')-1]
         dstring = time[time.find(',')+2:time.find('–')-1]
         ddate = dstring[-2:].lstrip(' ').zfill(2)
         ddttmstr = Date[:4]+dstring[:3]+ddate+dtime
         atime = time[time.find('–')+2:time.find('M',time.find('–')+2)+1]
         astring = time[time.find('on',time.find('–')+2)+8:len(time)]
         adate = astring[-2:].lstrip(' ').zfill(2)
         adttmstr = Date[:4]+astring[:3]+adate+atime
         ddttm = datetime.strptime(ddttmstr, '%Y%b%d%I:%M %p')
         adttm = datetime.strptime(adttmstr, '%Y%b%d%I:%M %p')
         ddttms.append(ddttm)
         adttms.append(adttm)
         layover.append(layoveriata)
         layovername.append(layoverairport)
         prices.append(price)
         cleanprices.append(cleanprice)
         times.append (time)
         airlines.append(airline)
         totaltimes.append(totaltime)
         stops.append(stop)
         logourls.append(logoclean)
     # print(price)
     # print(time)
     # print(airline)
     # print(totaltime)
     # print(stop)
     # print()
     
   leg2flightsdf = pd.DataFrame({'layover':layover,'layovername':layovername,'price':prices,'cleanprice':cleanprices,'time':times,'airline':airlines,'totaltime':totaltimes,'stops':stops,'logo':logourls,'departuretime':ddttms,'arrivaltime':adttms})
   
   # print(leg1flightsdf)
   # print(leg2flightsdf)
   
   allflights = pd.merge(leg1flightsdf, leg2flightsdf, on='layover')
   
   #print(allflights)
   
   gb = GridOptionsBuilder.from_dataframe(allflights, editable=False)
   gb.configure_grid_options(rowHeight=65)
   # gb.configure_selection(selection_mode="single", use_checkbox=True)
   
   thumbnail_renderer = JsCode("""
     class ThumbnailRenderer {
         init(params) {
   
         this.eGui = document.createElement('img');
         this.eGui.setAttribute('src', params.value);
         this.eGui.setAttribute('width', '60');
         this.eGui.setAttribute('height', '60');
         }
             getGui() {
             console.log(this.eGui);
   
             return this.eGui;
         }
     }
   """)
   
   gb.configure_column('logo_x', cellRenderer=thumbnail_renderer)
   gb.configure_column('logo_y', cellRenderer=thumbnail_renderer)
   
   grid = AgGrid(allflights,
             gridOptions=gb.build(),
             updateMode=GridUpdateMode.MODEL_CHANGED, #VALUE_CHANGED,
             allow_unsafe_jscode=True)

   st.empty()
   status.update(label = "your flight options are ready.", state="complete", expanded=True)
