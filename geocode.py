import csv
import os
import re
import json
import requests # will need requests package. Only using because urllib has python 2/3 compatibility issues 

mapboxkey = os.environ['MAPBOXKEY'] # you will need to export MAPBOXKEY (your mapbox api key)

multifamily_dicts = []

with open('multifamily.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	fieldnames = reader.fieldnames
	fieldnames.append('lon')
	fieldnames.append('lat')
	for row in reader:
		# Clean up input. First, remove "1/2" or "A/B" from addresses, since the geocoder
		# doesn't like these.
		half_match = re.match(r'^(.*) 1\/2$', row['location'])
		ab_match = re.match(r'^(.*) A\/B$', row['location'])
		if half_match:
			row['location'] = half_match.group(1)
		elif ab_match:
			row['location'] = ab_match.group(1)
		# Remove rows where sq_ft is 0. In virtually all of these cases, the assessor sums up the
		# square footage of multiple buildings under one building entry.
		if int(row['sq_ft']) == 0:
			print("Not added: " + row['location'])
			continue
		# Handle cases where the address is "UNKNOWN", "0 UNKNOWN", or "". These are usually condos.
		unknown_match = re.match(r'(?:0 )?UNKNOWN', row['location'])
		if unknown_match or row['location'] == "":
			if row['subdivision'] == "7 AT CROWN HEIGHTS":
				row['location'] = "1000 NW 37TH ST"
			elif row['subdivision'] == "HARVEY LOFTS":
				row['location'] = "1209 N HARVEY AVE"
			elif row['propertyid'] == "329449":
				row['location'] = "835 W Sheridan Ave"
			# For smaller buildings like duplexes, we may need to look them up on plats or
			# assessor GIS
			elif row['propertyid'] == "153951":
				row['location'] = "1808 N Gatewood Ave"
			elif row['propertyid'] == "347533":
				row['location'] = "2140 NW 12th St" # 2140-2144, but this is close enough

		# DONE with cleaning up input!

		# Finally...let's get the geocode from mapbox api
		url = "https://api.mapbox.com/geocoding/v5/mapbox.places/" + row['location'] +\
			" Oklahoma City OK.json?bbox=-97.587034,35.460296,-97.502931,35.524498&" \
			"access_token=" + os.environ['MAPBOXKEY']
		try:
			r = requests.get(url).text
			geocode_json = json.loads(r)
			coords = geocode_json['features'][0]['center']
			row['lon'] = coords[0]
			row['lat'] = coords[1]
		except Exception:
			print("Geocode failed: " + row['location'])

		# Add the row
		multifamily_dicts.append(row)
		print(row)

print(fieldnames)
with open('multifamily_coords.csv', 'w') as csvout:
	writer = csv.DictWriter(csvout, fieldnames=fieldnames)
	writer.writeheader()
	for row in multifamily_dicts:
		print(row)
		writer.writerow(row)
