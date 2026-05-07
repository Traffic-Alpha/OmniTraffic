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
        '84355055#1': [6, 6, 8, 5, 6],
        '741602126#2.93': [8, 8, 6, 8, 7],
        '739536522.212': [7, 8, 8, 6, 8],
        '387284606#0.817': [6, 9, 6, 8, 8],
    },
    
    # 2. 波动通勤车流 (Fluctuating Commuter Flow)
    "fluctuating_commuter": {
        '84355055#1': [5, 18, 4, 14, 5],  # 高峰低谷交替
        '741602126#2.93': [4, 18, 4, 15, 3],  # 强波动性
        '739536522.212': [5, 13, 5, 11, 5],   # 中等波动
        '387284606#0.817': [6, 14, 6, 15, 7], # 中等波动
    },
    
    # 3. 饱和高密度车流 (Saturated High-Density Flow)
    "high_density": {
        '84355055#1': [18, 18, 18, 18, 18],  # 车道近饱和
        '741602126#2.93': [17, 17, 17, 17, 17],  # 稳定高负载
        '739536522.212': [15, 15, 15, 15, 15],   # 持续高压
        '387284606#0.817': [16, 16, 16, 16, 16], # 稳定高负载
    },
    
    # 4. 随机扰动车流 (Random Perturbation Flow)
    "random_perturbation": {
        '84355055#1': [12, 3, 18, 4, 8], 
        '741602126#2.93': [18, 2, 30, 8, 12], 
        '739536522.212': [9, 8, 4, 15, 11],
        '387284606#0.817': [9, 17, 9, 11, 15],
    },
    
    # 5. 递增需求车流 (Increasing Demand Flow)
    "increasing_demand": {
        '84355055#1': [4, 8, 11, 15, 18],  # 线性增长
        '741602126#2.93': [6, 6, 14, 14, 20],  # 阶梯式增长
        '739536522.212': [4, 6, 12, 18, 22],  # 加速增长
        '387284606#0.817': [10, 10, 15, 15, 22], # 阶梯式增长
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