from datetime import datetime
import pytz

def display_clock(timezones=None):
    """
    Display current time in different time zones
    
    Args:
        timezones (list): List of timezone strings. Defaults to popular zones.
    """
    if timezones is None:
        timezones = [
            'US/Eastern',
            'US/Central',
            'US/Mountain',
            'US/Pacific',
            'Europe/London',
            'Europe/Paris',
            'Asia/Tokyo',
            'Asia/Dubai',
            'Australia/Sydney',
            'UTC'
        ]
    
    print("\n" + "="*60)
    print("WORLD CLOCK - Current Time in Different Time Zones")
    print("="*60)
    
    for tz_name in timezones:
        try:
            tz = pytz.timezone(tz_name)
            time_in_tz = datetime.now(tz)
            formatted_time = time_in_tz.strftime('%Y-%m-%d %H:%M:%S %Z')
            print(f"{tz_name:<25} {formatted_time}")
        except pytz.exceptions.UnknownTimeZoneError:
            print(f"{tz_name:<25} [Invalid timezone]")
    
    print("="*60 + "\n")

def display_clock_custom(timezone_dict):
    """
    Display clock with custom labels for time zones
    
    Args:
        timezone_dict (dict): Dict with format {'Label': 'Timezone'}
    """
    print("\n" + "="*60)
    print("WORLD CLOCK - Custom Time Zones")
    print("="*60)
    
    for label, tz_name in timezone_dict.items():
        try:
            tz = pytz.timezone(tz_name)
            time_in_tz = datetime.now(tz)
            formatted_time = time_in_tz.strftime('%H:%M:%S')
            print(f"{label:<20} {formatted_time}")
        except pytz.exceptions.UnknownTimeZoneError:
            print(f"{label:<20} [Invalid timezone]")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    # Display default time zones
    display_clock()
    
    # Display custom time zones with labels
    custom_zones = {
        "New York": "US/Eastern",
        "Los Angeles": "US/Pacific",
        "London": "Europe/London",
        "Tokyo": "Asia/Tokyo",
        "Dubai": "Asia/Dubai",
        "Sydney": "Australia/Sydney"
    }
    display_clock_custom(custom_zones)
