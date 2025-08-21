import phonenumbers
import requests
import folium
from phonenumbers import geocoder, carrier
from folium.plugins import MarkerCluster

# Function to validate and parse phone number
def parse_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        if phonenumbers.is_valid_number(parsed_number):
            return parsed_number
        else:
            raise ValueError("Invalid phone number")
    except phonenumbers.NumberParseException:
        raise ValueError("Error parsing phone number")

# Function to get geolocation data from Numverify API
def get_location_data(phone_number):
    api_key = 'YOUR_API_KEY'  # Replace with your Numverify API key
    url = f'http://apilayer.net/api/validate?access_key={api_key}&number={phone_number}&country_code=&format=1'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data['valid']:
            return {
                'country': data.get('country_name', 'Unknown'),
                'region': data.get('location', 'Unknown'),
                'carrier': data.get('carrier', 'Unknown')
            }
        else:
            raise ValueError("Invalid phone number or no data available")
    except requests.RequestException as e:
        raise Exception(f"API request failed: {e}")

# Function to get approximate coordinates (using phonenumbers geocoder or OpenCage)
def get_coordinates(region):
    # This is a placeholder; use OpenCage API for precise coordinates
    # For simplicity, we'll use hardcoded coordinates for some countries
    # In a real project, integrate with OpenCage Geocoder API
    coordinates = {
        'United States': [37.0902, -95.7129],
        'India': [20.5937, 78.9629],
        'United Kingdom': [55.3781, -3.4360],
        # Add more as needed
    }
    return coordinates.get(region, [0, 0])  # Default to [0, 0] if unknown

# Function to create a map
def create_map(location_data, coordinates):
    # Create a map centered at the coordinates
    my_map = folium.Map(location=coordinates, zoom_start=5)
    
    # Add a marker
    folium.Marker(
        location=coordinates,
        popup=f"Country: {location_data['country']}<br>Region: {location_data['region']}<br>Carrier: {location_data['carrier']}",
        icon=folium.Icon(color='blue')
    ).add_to(my_map)
    
    # Save the map to an HTML file
    my_map.save("phone_location_map.html")
    print("Map saved as 'phone_location_map.html'. Open it in a browser to view.")

# Main function
def main():
    phone_number = input("Enter the phone number (with country code, e.g., +1234567890): ")
    
    try:
        # Step 1: Parse and validate phone number
        parsed_number = parse_phone_number(phone_number)
        
        # Step 2: Get location data from API
        location_data = get_location_data(phone_number)
        
        # Step 3: Get approximate coordinates (you can enhance with OpenCage API)
        coordinates = get_coordinates(location_data['country'])
        if coordinates == [0, 0]:
            print(f"Warning: Could not find coordinates for {location_data['country']}. Using default [0, 0].")
        
        # Step 4: Display results
        print(f"Phone Number Details:")
        print(f"Country: {location_data['country']}")
        print(f"Region: {location_data['region']}")
        print(f"Carrier: {location_data['carrier']}")
        print(f"Approximate Coordinates: {coordinates}")
        
        # Step 5: Create and save the map
        create_map(location_data, coordinates)
        
    except Exception as e:
        print(f"Error: {e}")

if _name_ == "_main_":
    main()