import streamlit as st
import time
from datetime import datetime
from datetime import timedelta
from io import BytesIO
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import streamlit.components.v1 as components
from PIL import Image

st.set_page_config(layout="wide")
st.title("Welcome to Flight Finder")
st.subheader("Did you know that not all connecting flight combinations are searchable on Google Flights? Flight Finder finds hidden flight itineraries not marketed by the airlines or on Google Flights.")
left, right = st.columns([2,4])
right.image('https://github.com/amcclure0/portfolio/blob/main/Boeing%20777%20Background.png?raw=true', width = 600)


# st.markdown(
#     """
#     <style>
#     [data-testid=stAppViewContainer] {
#         background: url('https://github.com/amcclure0/portfolio/blob/main/Boeing%20777%20Background.png?raw=true');
#         background-size: cover;
#     }
#    </style>
#     """,
#     unsafe_allow_html=True
# )

Origin = left.text_input("Origin Airport (use IATA 3 character code)")
Dest = left.text_input("Destination Airport (use IATA 3 character code)")
Dateraw = left.date_input("Departure Date", format="YYYY-MM-DD", label_visibility="visible")
Date = str(Dateraw)
Nextdateraw = Dateraw + timedelta(days=1)
Nextdate = Nextdateraw.strftime('%Y-%m-%d')
Minlayover = int(left.text_input("Minimum Layover (hours)", 2))
Maxlayover = int(left.text_input("Maximum Layover (hours)", 6))

while len(Dest)==3:

   URL = 'https://direct-flights.com/chicago-{origin}'.format(
      origin = Origin.upper()
   )
   page = requests.get(URL)
   
   # print(page.text)
   
   soup = BeautifulSoup(page.content, "html.parser")
   
   results = soup.find(id='root')
   
   # print(results)
   
   destinations = results.find_all('div', class_='list-value-grow')
   origin = results.find('div', class_='panel-header-info')
   
   originiata = []
   origincity = []
   originiataandcity = []
   origintext = origin.text
   completeorigin = f"{origintext[origintext.find('Departure city:')+16:origintext.find(',',origintext.find('Departure city:')+16)]} {Origin}"
   
   for destination in destinations:
       #print(destination.text)
       info = destination.text
       iata = info[info.find('(')+1:info.find(')')]
       city = info[0:info.find('(')-1]
       iatacitystr = f"{iata} {city}."
       originiata.append(iata)
       origincity.append(city)
       originiataandcity.append(iatacitystr)
       
       # print(info)
       # print(iata)
       # print(city)
       # print()
       # print(iata)
   
   origindf = pd.DataFrame({'iata':originiata,'city':origincity,'iataandcity':originiataandcity})

   URL = 'https://direct-flights.com/chicago-{}'.format(Dest)
   page = requests.get(URL)
   
   # print(page.text)
   
   soup = BeautifulSoup(page.content, "html.parser")
   
   results = soup.find(id='root')
   
   # print(results)
   
   destinations = results.find_all('div', class_='list-value-grow')
   origin = results.find('div', class_='panel-header-info')
   
   destiata = []
   destcity = []
   destiataandcity = []
   desttext = origin.text
   completedest = f"{desttext[desttext.find('Departure city:')+16:desttext.find(',',desttext.find('Departure city:')+16)]} {Dest}"
   
   for destination in destinations:
       #print(destination.text)
       info = destination.text
       iata = info[info.find('(')+1:info.find(')')]
       city = info[0:info.find('(')-1]
       iatacitystr = f"{iata} {city}."
       destiata.append(iata)
       destcity.append(city)
       destiataandcity.append(iatacitystr)
   
       # print(info)
       # print(iata)
       # print(city)
       # print()
       # print(iata)
   
   destdf = pd.DataFrame({'iata':destiata,'city':destcity,'iataandcity':destiataandcity})
   
   layoverpoints = pd.merge(origindf, destdf, on=['iata','city','iataandcity'], how='inner')
   # print(layoverpoints)
   
   # print(completeorigin)
   # print(completedest)
      
   # right.subheader('Flights Options to XX')
   # ###DISPLAY DEST IMAGE###
   # destcity = completedest[0:len(completedest)-3]
   # URL = 'https://stock.adobe.com/search?filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=0&filters%5Bcontent_type%3Azip_vector%5D=0&filters%5Bcontent_type%3Avideo%5D=0&filters%5Bcontent_type%3Atemplate%5D=0&filters%5Bcontent_type%3A3d%5D=0&filters%5Bcontent_type%3Aaudio%5D=0&filters%5Binclude_stock_enterprise%5D=0&filters%5Bis_editorial%5D=0&filters%5Bfree_collection%5D=0&filters%5Bcontent_type%3Aimage%5D=1&k={}&order=relevance&safe_search=1&search_type=filter-select&get_facets=1'.format(f"{destcity} Skyline")
   
   # page = requests.get(URL)

   # soup = BeautifulSoup(page.content, "html.parser")

   # results = soup.find(id='mosaic-container')

   # cityimgraw = str(results.find('div', class_='search-result-cell small-bottom-spacing js-search-result-cell ftl-thumb-mosaic js-hover-container'))
 
   # cityimg = cityimgraw[cityimgraw.find('src=')+5:cityimgraw.find('"/>',cityimgraw.find('src=')+4)]

   # def get_image():
   #    URL = cityimg
   #    r = requests.get(URL)
   #    return BytesIO(r.content)

   # right.image(get_image())

   break

while len(Origin)==3 and len(Dest)==3:
   with st.status("finding hidden flights...connecting you to the world.", expanded=True) as status:
      st.write("(step 1/3) finding layover points...")
      time.sleep(10)
      st.write("(step 2/3) finding flights...")
      time.sleep(35)
      st.write("(step 3/3) comparing prices...")
      
      googleurlsleg1 = []
      googleurlsleg2 = []
      
      for i in layoverpoints.iataandcity:
          googleurlsleg1 += [
          'https://www.google.com/travel/flights?hl=en&q=Flights%20to%20{dest}%20from%20{origin}%20on%20{date}%20oneway%20nonstop'.format(
              dest = i.lower(),
              origin = completeorigin.lower(),
              date = Date
          )
          ]
          googleurlsleg1 += [
          'https://www.google.com/travel/flights?hl=en&q=Flights%20to%20{dest}%20from%20{origin}%20on%20{date}%20oneway%20nonstop'.format(
              dest = i.lower(),
              origin = completeorigin.lower(),
              date = Nextdate
          )
      ]
      
      for i in layoverpoints.iataandcity:
          googleurlsleg2 += [
          'https://www.google.com/travel/flights?hl=en&q=Flights%20to%20{dest}%20from%20{origin}%20on%20{date}%20oneway%20nonstop'.format(
              dest = completedest.lower(),
              origin = i.lower(),
              date = Date
          )
          ]
          googleurlsleg2 += [
          'https://www.google.com/travel/flights?hl=en&q=Flights%20to%20{dest}%20from%20{origin}%20on%20{date}%20oneway%20nonstop'.format(
              dest = completedest.lower(),
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
            if flight.find('div', class_='BVAVmf I11szd POX3ye') == None:
               continue
            layoveriata = str(i)[61:64].upper()
            price = str(flight.find('div', class_='BVAVmf I11szd POX3ye').text)
            cleanprice = int(price[price.find('$')+1:len(price)].replace(',' , ''))
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
            if flight.find('div', class_='BVAVmf I11szd POX3ye') == None:
               continue
            layoveriata = str(flight.find('div', class_='QylvBf').text)[:3]
            layoverairport = str(flight.find('div', class_='QylvBf').text)[-len(str(flight.find('div', class_='QylvBf').text))+3:]
            price = str(flight.find('div', class_='BVAVmf I11szd POX3ye').text)
            cleanprice = int(price[price.find('$')+1:len(price)].replace(',' , ''))
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
      allflights['totalcost'] = allflights.cleanprice_x + allflights.cleanprice_y
      allflights['layoverarrive'] = pd.to_datetime(allflights.arrivaltime_x)
      allflights['layoverdepart'] = pd.to_datetime(allflights.departuretime_y)
      allflights['layoverhours'] = (allflights['layoverdepart'] - allflights['layoverarrive'])/pd.Timedelta(hours=1)
      
      displaycolumns = {'layover': 'Layover Aiport', 'logo_x': 'Leg 1 Airline', 'logo_y': 'Leg 2 Airline', 'totalcost': 'Total Cost', 'layoverhours': 'Layover Hours', 'departuretime_x': 'Leg 1 Departure', 'arrivaltime_x': 'Leg 1 Arrival', 'departuretime_y': 'Leg 2 Departure', 'arrivaltime_y': 'Leg 2 Arrival'}
      displayflights = allflights.rename(columns = displaycolumns)[[*displaycolumns.values()]]
      displayflights = displayflights[displayflights['Layover Hours'].between(Minlayover, Maxlayover)]
      displayflights = displayflights.sort_values(by=['Total Cost'])
      
      gb = GridOptionsBuilder.from_dataframe(displayflights, editable=False)
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
      
      gb.configure_column('Leg 1 Airline', cellRenderer=thumbnail_renderer)
      gb.configure_column('Leg 2 Airline', cellRenderer=thumbnail_renderer)
      
      grid = AgGrid(displayflights,
                gridOptions=gb.build(),
                updateMode=GridUpdateMode.MODEL_CHANGED, #VALUE_CHANGED,
                allow_unsafe_jscode=True)
   
      # st.empty()
      status.update(label = "your flight options are ready.", state="complete", expanded=True)
      Origin = 'X'
      Dest = 'X'
