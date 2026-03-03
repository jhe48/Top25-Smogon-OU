import urllib.request
import re

# UPDATE THIS VARIABLE if you want to hardcode a specific month. 
# Leave it as None to automatically fetch the most recent month.
# Example format: "2026-02"
TARGET_MONTH = None 

def get_latest_month():
    url = "https://smogon.com/stats/"
    # A User-Agent header is required so the server does not block the request
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            # Find all folder links that match the YYYY-MM format
            months = re.findall(r'<a href="(\d{4}-\d{2})/">', html)
            if not months:
                print("Could not find any month folders.")
                return None
            
            # Sort descending and pick the newest month
            months.sort(reverse=True)
            return months[0]
            
    except Exception as e:
        print(f"Error fetching stats directory: {e}")
        return None

def fetch_top_pokemon(month, tier="gen9ou-1695.txt", top_n=25):
    url = f"https://smogon.com/stats/{month}/{tier}"
    print(f"Fetching data from: {url}\n")
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            text = response.read().decode('utf-8')
            lines = text.split('\n')
            
            pokemon_list = []
            data_started = False
            
            for line in lines:
                # Detect the start of the data table
                if line.startswith(' | Rank'):
                    data_started = True
                    continue
                
                # Skip the ASCII borders
                if line.startswith(' +'):
                    continue
                    
                # Parse the rows
                if data_started and line.startswith(' | '):
                    parts = [p.strip() for p in line.split('|')]
                    
                    if len(parts) > 2:
                        pokemon_name = parts[2]
                        pokemon_list.append(pokemon_name)
                        
                        if len(pokemon_list) >= top_n:
                            break
                            
            return pokemon_list
            
    except Exception as e:
        print(f"Error fetching tier data: {e}")
        return []

if __name__ == "__main__":
    month_to_fetch = TARGET_MONTH if TARGET_MONTH else get_latest_month()
    
    if month_to_fetch:
        top_25 = fetch_top_pokemon(month_to_fetch)
        
        print(f"Top 25 Pokémon for {month_to_fetch}:")
        for i, name in enumerate(top_25, 1):
            print(f"{i}. {name}")
    else:
        print("Failed to determine the month to fetch.")