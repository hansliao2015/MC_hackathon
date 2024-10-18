import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# 預設的碳排放係數
default_carbon_factors = {
    "汽車": 0.2,
    "大客車": 0.5,
    "大貨車": 0.7,
    "小客車": 0.1,
    "小貨車": 0.4,
    "特種車": 0.6,
    "機車": 0.05,
    "公車": 0.3
}

# 預設的載客量
default_capacity = {
    "汽車": 4,
    "大客車": 45,
    "大貨車": 2,
    "小客車": 4,
    "小貨車": 2,
    "特種車": 2,
    "機車": 2,
    "公車": 40
}

st.title('兩兩車種碳排放比較')

# 創建兩列來放置下拉選單
col1, col2 = st.columns(2)

# 選擇車種1和車種2
with col1:
    vehicle_1 = st.selectbox('選擇車種 1', list(default_carbon_factors.keys()), key="vehicle_1")

with col2:
    vehicle_2_options = list(default_carbon_factors.keys())
    vehicle_2 = st.selectbox('選擇車種 2', vehicle_2_options, index=vehicle_2_options.index("公車"), key="vehicle_2")

# 創建兩列來放置共乘人數輸入
col5, col6 = st.columns(2)

# 共乘人數輸入
with col5:
    passengers_1 = st.number_input(
        f'{vehicle_1} 搭乘人數',
        min_value=1,
        max_value=default_capacity[vehicle_1],
        value=1,
        key="passengers_1"
    )

with col6:
    passengers_2 = st.number_input(
        f'{vehicle_2} 搭乘人數',
        min_value=1,
        max_value=default_capacity[vehicle_2],
        value=default_capacity[vehicle_2],
        key="passengers_2"
    )

# 創建兩列來放置滑動條
col3, col4 = st.columns(2)

# 碳排放係數滑桿調整
with col3:
    carbon_factor_1 = st.slider(f"{vehicle_1} 碳排放係數", 0.0, 1.0, default_carbon_factors[vehicle_1], key="carbon_factor_1")

with col4:
    carbon_factor_2 = st.slider(f"{vehicle_2} 碳排放係數", 0.0, 1.0, default_carbon_factors[vehicle_2], key="carbon_factor_2")

# 路程輸入
distance = st.number_input('輸入行駛路程（公里）', min_value=1, value=10, key="distance_input")

# 計算總碳排放和人均碳排放
total_emission_1 = carbon_factor_1 * distance
total_emission_2 = carbon_factor_2 * distance

per_person_emission_1 = total_emission_1 / passengers_1
per_person_emission_2 = total_emission_2 / passengers_2

# 顯示結果
st.write(f'{vehicle_1} 的總碳排放: {total_emission_1:.2f} kg CO2, {vehicle_1} 的人均碳排放: {per_person_emission_1:.2f} kg CO2/人')
st.write(f'{vehicle_2} 的總碳排放: {total_emission_2:.2f} kg CO2, {vehicle_2} 的人均碳排放: {per_person_emission_2:.2f} kg CO2/人')

# 顯示較低碳排放的選擇（基於人均碳排放）
if per_person_emission_1 > per_person_emission_2:
    st.write(f'改用 {vehicle_2} 每人可節省碳排放: {(per_person_emission_1 - per_person_emission_2):.2f} kg CO2')
else:
    st.write(f'改用 {vehicle_1} 每人可節省碳排放: {(per_person_emission_2 - per_person_emission_1):.2f} kg CO2')

# 創建條形圖來比較兩車種的人均碳排放
df_bar = pd.DataFrame({
    'Vehicle': [f'{vehicle_1}\n({passengers_1}人)', f'{vehicle_2}\n({passengers_2}人)'],
    'Per Person Emissions': [per_person_emission_1, per_person_emission_2]
})
bar_chart = alt.Chart(df_bar).mark_bar().encode(
    x='Vehicle',
    y='Per Person Emissions'
).properties(title='人均碳排放比較')
st.altair_chart(bar_chart, use_container_width=True)

# 創建折線圖來展示隨路程變化的人均碳排放量
distances = np.arange(1, 101)
emissions_1 = (carbon_factor_1 * distances) / passengers_1
emissions_2 = (carbon_factor_2 * distances) / passengers_2
df_line = pd.DataFrame({
    'Distance (km)': distances,
    f'{vehicle_1} ({passengers_1}人)': emissions_1,
    f'{vehicle_2} ({passengers_2}人)': emissions_2
})
line_chart = alt.Chart(df_line).transform_fold(
    [f'{vehicle_1} ({passengers_1}人)', f'{vehicle_2} ({passengers_2}人)'],
    as_=['Vehicle', 'Emissions']
).mark_line().encode(
    x='Distance (km):Q',
    y='Emissions:Q',
    color='Vehicle:N'
).properties(title='隨路程變化的人均碳排放比較')
st.altair_chart(line_chart, use_container_width=True)