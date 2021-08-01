from logging import Logger
from typing import Mapping
import requests
from bs4 import BeautifulSoup
#from requests.api import requestS


#url = "https://www.booking.com/js_tracking?sid=e9ba9a6c9dc28f914d44c04a61986811&ver=2&lang=fr&pid=67c048e5ff51012e&aid=304142&stype=1&ref_action=index&ete=&etg=&etcg=cCHObTYWeLJFfFdHMaMEAaXdJcCcCcCC|1,cCHObTYWeLJFfFdHMaMEAaXdJOOIBBO|1&ets=BPHAUbaTaTaBTdSPDUFYQJKDKGEXO|5&etgwv=&m=UmFuZG9tSVYkc2RlIyh9YR94sFeuFVXCBH08KDQbgyuAKwaKtQAAhoHw2x4bj17R9qhnnYlDgyhjqEO5vi2lwk6JCIsznvvRa9Wkwz2996lDeVcKMOw6cw9zSTMXI2AtTA3f6IM3srtfp_eGCO4ppQ5eh02kau7kVMyT1U7GMVEcaWcpz-AWCPQdPTX9Cz7rdQHVegbzDUGSqhEZ7s2m0Y0O70ewona-bGUfMvM04YdNxTmrvvwn2K8GizbE5uWmAbidB0ep5-9o6nnqGICGqX4ApVeFbNw4xSUYxdaHaAo"

def get_html():
    headers = {'Accept-Encoding': 'gzip, deflate, br',
    'Cookie': '_pxhd=mdYiLBcc63tit3jJibJ%2F040peMSCuLBfGugBouUMXLEC9jAGnm2o7oFJmsmFuu%2FJfX0aVmJSK%2FYdtgMj7tbMew%3D%3D%3Ar9UfQEUYE10y54DYjJFxq6l35IeHy2gOjxKu11tMXeVCb94QK6MGm5DByQUe5u71punk7p%2FVm4AiJXiL9AKGxFafdnJ9R60Ss%2FsLD%2F%2FBHVE%3D; cors_js=1; BJS=-; _ga=GA1.2.1687431912.1626384329; _gid=GA1.2.1200067750.1626384329; _pxvid=2c32b741-e5b3-11eb-8d93-8b8d2b0b649b; bkng_prue=1; _gcl_au=1.1.2085545831.1626384330; _scid=bc1f19c8-ed76-476a-9223-c3b3214bbdbb; _pin_unauth=dWlkPVpUWmpaV1ppTTJRdE1HTXdOaTAwT0RZMUxXRTBPRFF0WlRsalptUTNPVEpqTlRFMw; bkng_sso_session=e30; OptanonConsent=isIABGlobal=false&datestamp=Fri+Jul+16+2021+18%3A48%3A17+GMT%2B0200+(Central+European+Summer+Time)&version=6.13.0&hosts=&consentId=80a2ad46-1131-462b-b3e8-86525b213aff&interactionCount=1&landingPath=https%3A%2F%2Fwww.booking.com%2Fsearchresults.fr.html%3Flang%3Dfr%26ss%3Dmarseille; b=%7B%22countLang%22%3A4%7D; _uetsid=2e00a840e5b311eb8cc02b89a9c90c8c; _uetvid=2e00e5f0e5b311eb80339f010ae80e2e; bkng_sso_ses=eyJib29raW5nX2dsb2JhbCI6W3siaCI6IjUweHh2R3BmakNzT1hOcTBiOTdEbXhnb1h2dnkwbzB6ZGJCWlVDRDZTVFkiLCJhIjoxfV19; has_preloaded=1; lastSeen=0; _px3=58c646ee6d40044a4364cc94f311b6048ef2ac12196ac1a7bc8824f2da1557e4:TR9So7ahzX/IBYxS0nqERDt2fb4pVGALg7Y9N0jZDoqqt+hRPZYjjvyAfu9VMy+bYqM0juGlGiibsxxHfKXNqg==:1000:Kh8hB+6j3CrfULcuF/WBnz2nBAiuZr8Kz9hM96EUaT35TeVf2rfo/DxyfsjnaSINKMloOgEJ91k5jojij09RYWEwC+qNHyGIdGSQdmNcqRNPxZlFDAijUgzbpeCF1Rkwy6wmTCjHwpP2FlYJpf27Fmv9CmKdmT40FdGsZBPstl85CP5m8diF4mKVzgo1GTh/z4R0pNWed2LwgmqyRkAqNQ==; _gat=1; bkng=11UmFuZG9tSVYkc2RlIyh9YXjA6rtNF48dyfPzTHjBgvttBSFWKt4b%2FJsFX4xc2u4BUuXbdgM1scm2%2BLdf0W0naqCGB4B84g9P%2FCzkn%2BoLpnIMP1dZ4klXcZywzgQJ%2B3a0j2xtaKAMZV7AZ7BQgj1F0MSOlgJfuuMYGkgQzG2u00qLme5pYphAIKMqZqkNUWC%2F2hD55O7fwiM%3D; _pxde=82a04d2a329ae6aec4a13bfc3237f8f62610dd2e9dfdc33925102941fc0e9fcf:eyJ0aW1lc3RhbXAiOjE2MjY1MDgxOTcxOTgsImZfa2IiOjAsImlwY19pZCI6W119' ,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

   # url = 'https://www.booking.com/searchresults.es.html?lang=fr&ss=Paris'
    #url = "https://www.booking.com/searchresults.fr.html?label=gen173nr-1DCAEoggI46AdIM1gEaE2IAQGYAQ24ARfIAQzYAQPoAQGIAgGoAgO4AtLwxocGwAIB0gIkYWY0MGI5MzAtNDA3Yi00MDE0LWI5ZWQtZmZiM2Y4YWNkNjYz2AIE4AIB&lang=fr&sid=f7b24d12e53e7f2a0fabe8c4c2fda2e7&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.fr.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaE2IAQGYAQ24ARfIAQzYAQPoAQGIAgGoAgO4AtLwxocGwAIB0gIkYWY0MGI5MzAtNDA3Yi00MDE0LWI5ZWQtZmZiM2Y4YWNkNjYz2AIE4AIB%3Bsid%3Df7b24d12e53e7f2a0fabe8c4c2fda2e7%3Bsb_price_type%3Dtotal%3Bsig%3Dv1huPG3wo1%3B&ss=Paris%2C+%C3%8Ele-de-France%2C+France&is_ski_area=&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=Paris&ac_position=0&ac_langcode=fr&ac_click_type=b&dest_id=-1456928&dest_type=city&iata=PAR&place_id_lat=48.856682&place_id_lon=2.351476&search_pageview_id=07d536789110000c&search_selected=true&search_pageview_id=07d536789110000c&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0"
    url = "https://www.booking.com/searchresults.fr.html?aid=376366&label=fr-85Sbyi2evytni3mHZEi6UgS455401520398%3Apl%3Ata%3Ap1%3Ap22.563.000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9056144%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9Ye7BFAsTyVd6vvamF_no64o&sid=f35bfaa84676b7b9790807df7ca505ba&tmpl=searchresults&ac_click_type=b&ac_position=0&checkin_month=7&checkin_monthday=26&checkin_year=2021&checkout_month=7&checkout_monthday=31&checkout_year=2021&class_interval=1&dest_id=73&dest_type=country&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=country&room1=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=1&slp_r_match=0&src=index&src_elem=sb&srpvid=17d64b5024210213&ss=France&ss_all=0&ss_raw=France&ssb=empty&sshis=0&top_ufis=1&rows=25&offset=200"
    response = requests.get(url, headers=headers)
    if not response.ok: #= .status_code = 200
        print(f'Code:{response.status_code}, url: {url}')
        
    return response

def main():
    r = get_html()
    print(r.status_code)
    print(r.text[0:200])
    soup = BeautifulSoup(r.content, 'lxml')

    tags = soup.find_all('div', class_ = 'sr_item')
    print(f'tags qty: {len(tags)}')
    
if __name__ == '__main__':
    main()