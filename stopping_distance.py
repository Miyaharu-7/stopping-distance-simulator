from math import isclose
def calculate_stopping_distance(speed_kmh, reaction_time_s, deceleration_mps2):
    speed_mps = speed_kmh / 3.6
    reaction_distance_m = speed_mps * reaction_time_s
    braking_distance_m = speed_mps ** 2 / (2 * deceleration_mps2)
    return reaction_distance_m + braking_distance_m


def judge_stopping_position(stopping_distance_m, obstacle_distance_m):
    margin_m = obstacle_distance_m - stopping_distance_m

    if isclose(margin_m, 0.0, abs_tol=1e-9):
        return 0.0, "停止位置が障害物と一致"
    if margin_m > 0:
        return margin_m, "障害物の手前で停止"
    return margin_m, "障害物までの距離が不足"


if __name__ == "__main__":
    stopping_distance_m = calculate_stopping_distance(36, 1.0, 5.0)
    print(f"停止距離（試算） {stopping_distance_m:.1f} m")

    for obstacle_distance_m in (30, 20, 15):
        margin_m, judgment = judge_stopping_position(
            stopping_distance_m, obstacle_distance_m
        )
        print(f"障害物まで {obstacle_distance_m} m → 余裕 {margin_m:.1f} m／{judgment}")