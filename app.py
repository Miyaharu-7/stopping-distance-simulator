import streamlit as st

from stopping_distance import calculate_stopping_distance, judge_stopping_position


st.set_page_config(page_title="停止距離シミュレーター")
st.title("停止距離シミュレーター")
st.caption("反応中は一定の速度で進み、ブレーキ中は一定の減速度で止まると仮定します。")

speed_col, obstacle_col = st.columns(2)
speed_kmh = speed_col.slider("速度（km/h）", 0, 120, 36)
obstacle_distance_m = obstacle_col.number_input(
    "障害物までの距離（m）",
    min_value=0.0,
    value=30.0,
    step=1.0,
)

with st.expander("反応時間と減速度を変更"):
    reaction_time_s = st.slider("反応時間（秒）", 0.0, 3.0, 1.0, 0.1)
    deceleration_mps2 = st.slider("減速度の大きさ（m/s²）", 0.5, 10.0, 5.0, 0.5)

stopping_distance_m = calculate_stopping_distance(
    speed_kmh, reaction_time_s, deceleration_mps2
)
margin_m, judgment = judge_stopping_position(stopping_distance_m, obstacle_distance_m)

distance_col, margin_col = st.columns(2)
distance_col.metric("停止距離（試算）", f"{stopping_distance_m:.1f} m")
margin_col.metric("距離の余裕（不足はマイナス）", f"{margin_m:.4g} m")

if margin_m > 0:
    st.success(judgment)
elif margin_m < 0:
    st.error(judgment)
else:
    st.warning(judgment)

st.subheader("速度と停止距離の関係")
speeds_kmh = list(range(121))
chart_data = {
    "速度（km/h）": speeds_kmh,
    "停止距離（m）": [
        calculate_stopping_distance(speed, reaction_time_s, deceleration_mps2)
        for speed in speeds_kmh
    ],
    "障害物まで（m）": [obstacle_distance_m] * len(speeds_kmh),
}
st.line_chart(
    chart_data,
    x="速度（km/h）",
    y=["停止距離（m）", "障害物まで（m）"],
    y_label="距離（m）",
)