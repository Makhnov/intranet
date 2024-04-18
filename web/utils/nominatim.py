from geopy.geocoders import Nominatim
geocoder = Nominatim(user_agent="my_geo_app")
        
def geocode(address1, address2, zip_code, city, country):
    try:
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