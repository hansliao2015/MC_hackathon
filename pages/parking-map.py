import streamlit as st
import folium
from streamlit.components.v1 import html
from utils.load_data import get_data


# API URL for parking data
parking_data_url = "https://hispark.hccg.gov.tw/OpenData/GetParkInfo?1111104155049"

# Function to generate Folium map
def generate_map(parking_data):
    m = folium.Map(location=[24.80726, 120.969783], zoom_start=13)  # 地图中心
    for park in parking_data:
        latitude = float(park["LATITUDE"])
        longitude = float(park["LONGITUDE"])
        popup_info = f"""
        <b>{park['PARKINGNAME']}</b><br>
        地址: {park['ADDRESS']}<br>
        營業時間: {park['BUSINESSHOURS']}<br>
        平日費率: {park['WEEKDAYS']}<br>
        假日費率與充電設備: {park['HOLIDAY']}<br>
        汽車空閒/總車位數量: {park['FREEQUANTITY']}/{park['TOTALQUANTITY']}<br>
        殘障車位空閒/總數量: {park['FREEQUANTITYDIS']}/{park['TOTALQUANTITYDIS']}<br>
        更新時間: {park['UPDATETIME']}
        """
        marker = folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_info, max_width=300),
            tooltip=park["PARKINGNAME"]
        )
        marker.add_to(m)
    return m._repr_html_()

# Streamlit application part
st.title("新竹市停車場資訊地圖")

parking_data = get_data(parking_data_url)
if parking_data is not None:
    st.write("停車場數量:", len(parking_data))
    map_html = generate_map(parking_data)
    html(map_html, height=600)
else:
    st.error("未能載入停車場資料，請稍後再試。")
