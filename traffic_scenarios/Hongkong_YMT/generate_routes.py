'''
Author: WANG Maonan
Date: 2025-07-17 13:01:58
LastEditors: WANG Maonan
Description: 车辆 Route 生成
LastEditTime: 2025-09-02 14:18:05
'''
from tshub.utils.init_log import set_logger
from tshub.utils.get_abs_path import get_abs_path
from tshub.sumo_tools.generate_routes import generate_route

# 初始化日志
current_file_path = get_abs_path(__file__)
set_logger(current_file_path('./'), file_log_level='WARNING', terminal_log_level='INFO')

# 开启仿真 --> 指定 net 文件
sumo_net = current_file_path("./networks/normal.net.xml")

traffic_flow_configs = {
    # 1. 稳定低密度车流 (Stable Low-Density Flow)
    "low_density": {
        '102454134#0': [6, 6, 6, 7, 6],
        '1200878753#0': [8, 9, 8, 8, 9],
        '30658263#0': [8, 8, 8, 8, 8], 
        '960661806#0': [7, 8, 9, 9, 8],
    },
    
    # 2. 波动通勤车流 (Fluctuating Commuter Flow)
    "fluctuating_commuter": {
        '102454134#0': [3, 8, 3, 5, 4],  # 高峰低谷交替
        '1200878753#0': [8,9, 9, 9, 10],  # 强波动性
        '30658263#0': [10, 12, 9, 17, 8],   # 中等波动
        '960661806#0': [8, 14, 8, 15, 10], # 中等波动
    },
    
    # 3. 饱和高密度车流 (Saturated High-Density Flow)
    "high_density": {
        '102454134#0': [19, 19, 19, 19, 19],  # 车道近饱和
        '1200878753#0': [18, 18, 18, 18, 18],  # 稳定高负载
        '30658263#0': [15, 15, 15, 15, 15],   # 持续高压
        '960661806#0': [18, 18, 18, 18, 18], # 稳定高负载
    },
    
    # 4. 随机扰动车流 (Random Perturbation Flow)
    "random_perturbation": {
        '102454134#0': [12, 3, 9, 5, 10], 
        '1200878753#0': [13, 2, 12, 8, 12], 
        '30658263#0': [12, 10, 5, 19, 15],
        '960661806#0': [13, 17, 17, 10, 15],
    },
    
    # 5. 递增需求车流 (Increasing Demand Flow)
    "increasing_demand": {
        '102454134#0': [4, 8, 12, 16, 12],  # 线性增长
        '1200878753#0': [8, 8, 15, 15, 4],  # 阶梯式增长
        '30658263#0': [8, 11, 15, 19, 25],  # 加速增长
        '960661806#0': [10, 10, 15, 15, 20], # 阶梯式增长
    },
}

for config_id, config_info in traffic_flow_configs.items():
    generate_route(
        sumo_net=sumo_net,
        interval=[2,2,2,2,2], # 共有 10 min
        edge_flow_per_minute=config_info,
        edge_turndef={},
        veh_type={
            'background': {'color':'220,220,220', 'length': 5, 'probability':1},
        },
        output_trip=current_file_path('./testflow.trip.xml'),
        output_turndef=current_file_path('./testflow.turndefs.xml'),
        output_route=current_file_path(f'./routes/{config_id}.rou.xml'),
        interpolate_flow=False,
        interpolate_turndef=False,
    )