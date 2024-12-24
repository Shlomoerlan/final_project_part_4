import folium
from typing import List, Dict, Any


def create_map_from_results(results: List[Dict[str, Any]]) -> str:
    m = folium.Map(location=[0, 0], zoom_start=2)

    print(f"Creating map with {len(results)} results")

    for result in results:
        print(f"Processing result: {result}")
        if 'coordinates' in result:
            coords = result['coordinates']
            print(f"Adding marker at {coords}")
            folium.Marker(
                location=[coords['lat'], coords['lon']],
                popup=f"""
                <b>{result['title']}</b><br>
                Date: {result['publication_date']}<br>
                Category: {result['category']}<br>
                Location: {result['location']}
                """,
                icon=folium.Icon(color='red')
            ).add_to(m)

    return m._repr_html_()