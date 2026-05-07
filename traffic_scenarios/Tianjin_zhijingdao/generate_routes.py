'''
Author: WANG Maonan
Date: 2025-07-17 13:01:58
LastEditors: WANG Maonan
Description: 车辆 Route 生成
LastEditTime: 2025-07-17 15:32:43
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
        '417937574#1.74': [12, 10, 11, 9, 8],
        '417937497#0.2105': [10, 12, 9, 10, 9],
        '339537541#3': [8, 10, 10, 10, 10],
        '339537367#2.7': [10, 9, 10, 9, 10],
    },
    
    # 2. 波动通勤车流 (Fluctuating Commuter Flow)
    "fluctuating_commuter": {
        '339537541#3': [5, 18, 5, 15, 4],  # 高峰低谷交替
        '339537367#2.7': [4, 18, 6, 12, 3],  # 强波动性
        '417937574#1.74': [7, 14, 5, 11, 6],   # 中等波动
        '417937497#0.2105': [10, 21, 8, 20, 9],  # 强波动性
    },
    
    # 3. 饱和高密度车流 (Saturated High-Density Flow)
    "high_density": {
        '339537541#3': [19, 19, 19, 19, 19],  # 车道近饱和
        '339537367#2.7': [17, 17, 17, 17, 17],  # 稳定高负载
        '417937574#1.74': [15, 15, 15, 15, 15],   # 持续高压
        '417937497#0.2105': [18, 18, 18, 18, 18],  # 车道近饱和
    },
    
    # 4. 随机扰动车流 (Random Perturbation Flow)
    "random_perturbation": {
        '339537541#3': [15, 13, 20, 5, 10], 
        '339537367#2.7': [18, 12, 22, 8, 12], 
        '417937574#1.74': [12, 10, 5, 20, 15],
        '417937497#0.2105': [16, 15, 8, 17, 16],
    },
    
    # 5. 递增需求车流 (Increasing Demand Flow)
    "increasing_demand": {
        '339537541#3': [4, 8, 12, 16, 20],  # 线性增长
        '339537367#2.7': [8, 8, 15, 22, 22],  # 阶梯式增长
        '417937574#1.74': [6, 8, 11, 15, 20],  # 加速增长
        '417937497#0.2105': [4, 6, 10, 14, 20],  # 线性增长
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