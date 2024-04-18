from geopy.geocoders import Nominatim
geocoder = Nominatim(user_agent="my_geo_app")
        
def geocode(address1=None, address2=None, zip_code=None, city=None, country=None):
    try:        
        print(f"Geocoding: {address1}, {address2}, {zip_code}, {city}, {country}")
        if (not address1 or address1 == "") and (not address2 or address2 == "") and (not zip_code or zip_code == "") and (not city or city == "") and (not country or country == ""):
            print("No valid address components provided besides the country.")
            return None, None
        else:
            country = 'FRANCE'
                        
        parts_full = [part for part in [address1, address2, zip_code, city, country] if part]
        address = ', '.join(parts_full)
        location = geocoder.geocode(address)        
        if location:
            print(f"Geocoding full: {address} -> {location.latitude}, {location.longitude}")
            return location.latitude, location.longitude
        else:
            parts_short = [part for part in [address1, zip_code, city, country] if part]
            adress_short = ', '.join(parts_short)            
            location = geocoder.geocode(adress_short)            
            if location:
                print(f"Geocoding short: {adress_short} -> {location.latitude}, {location.longitude}")
                return location.latitude, location.longitude
            else:
                parts_shorter = [part for part in [zip_code, city, country] if part]
                adress_shorter = ', '.join(parts_shorter)
                location = geocoder.geocode(adress_shorter)                
                if location:
                    print(f"Geocoding shorter: {adress_shorter} -> {location.latitude}, {location.longitude}")
                    return location.latitude, location.longitude
                else:
                    return None, None                
    except Exception as e:
        print(f"Error during geocoding: {e}")
        return None, None