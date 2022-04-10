
def build_start_urls(self, cities: list):
    return [f'https://www.booking.com/searchresults.fr.html?lang=fr&dest_type=city&group_adults=1&no_rooms=1&ss={city}' for city in cities]
