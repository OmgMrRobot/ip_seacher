

import requests as re
from pyfiglet import Figlet as Fl
import folium
from folium.plugins import MousePosition




def create_map(loc):
	area = folium.Map(location=[loc['lat'], loc['lon']])
	
	formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
	MousePosition(
	    position="topright",
	    separator=" | ",
	    empty_string="NaN",
	    lng_first=True,
	    num_digits=20,
	    prefix="Coordinates:",
	    lat_formatter=formatter,
	    lng_formatter=formatter,
	).add_to(area)	

	city = folium.map.FeatureGroup()


	# style the feature group (стиль группы объектов)
	city .add_child(
	    folium.features.CircleMarker(
	        [float(loc['lat']), float(loc['lon'])], radius = 5,  # широта и долгота Санкт-Петербурга
	        color = 'red', fill_color = 'Red'))

	
	area.add_child(city)
	area.save(f"{loc['region']}_{loc['city']}.html" )


def valid_ip(ip):
	ip_ = ip.split('.')
	if  len(ip_) != 4:
		print("Please check your ip (XXX.XXX.XXX.XXX)")
		return False

	for i in ip_:
		try:
			if int(i) > 255:
				print("Your is ip bigger than 255 \nRestart with correct ip")
				return False
		except ValueError as er:
			print("Please check your ip (XXX.XXX.XXX.XXX)")
			print("Restart with correct ip")
			return False

	return True





def get_info_by_ip(ip:str):

	try:

		response = re.get(url = f'http://ip-api.com/json/{ip}').json()
		data = {
				'[IP]': response.get('query'),
				'[Status]': response.get('status'),
				'[Int prov]': response.get('isp'),
				'[Org]': response.get('country'),
				'[Country]': response.get('country'),
				'[Region Name]': response.get('regionName'),
				'[City]': response.get('city'),
				'[Zip]': response.get('zip'),
				'Lat': response.get('lat'),
				'Lon': response.get('lon'),

		}

		for k, v in data.items():
			print(k, "->", v)

		if response.get('lat'):
			create_map({"lat": response.get('lat'), "lon": response.get('lon'), "region":response.get('regionName'), 'city': response.get('city')})

		
	except re.exceptions.ConnectionError:
		print('[!] Please check your connection')
	except AssertoinError:
		print("Please check your ip (XXX.XXX.XXX.XXX)")



if __name__ == "__main__":
	prev = Fl(font='slant')
	print(prev.renderText('IP INFO'))
	
	ip = input('Please enter a target IP: ')
	if valid_ip(ip):
		get_info_by_ip(ip)