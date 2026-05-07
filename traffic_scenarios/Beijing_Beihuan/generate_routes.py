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
        '157863208#0.1590': [6, 6, 6, 6, 6],  # 稳定6辆/分钟
        '252712271#0.589': [4, 4, 4, 4, 4],  # 稳定4辆/分钟
        '-1106233488.150': [5, 5, 5, 5, 5]   # 稳定5辆/分钟
    },
    
    # 2. 波动通勤车流 (Fluctuating Commuter Flow)
    "fluctuating_commuter": {
        '157863208#0.1590': [4, 16, 3, 12, 3],  # 高峰低谷交替
        '252712271#0.589': [3, 14, 4, 11, 2],  # 强波动性
        '-1106233488.150': [5, 12, 3, 10, 4]   # 中等波动
    },
    
    # 3. 饱和高密度车流 (Saturated High-Density Flow)
    "high_density": {
        '157863208#0.1590': [17, 17, 17, 17, 17],  # 车道近饱和
        '252712271#0.589': [15, 15, 15, 15, 15],  # 稳定高负载
        '-1106233488.150': [13, 13, 13, 13, 13]   # 持续高压
    },
    
    # 4. 随机扰动车流 (Random Perturbation Flow)
    "random_perturbation": {
        '157863208#0.1590': [10, 2, 16, 3, 6], 
        '252712271#0.589': [12, 1, 20, 5, 8], 
        '-1106233488.150': [8, 6, 3, 14, 10]
    },
    
    # 5. 递增需求车流 (Increasing Demand Flow)
    "increasing_demand": {
        '157863208#0.1590': [3, 6, 10, 13, 17],  # 线性增长
        '252712271#0.589': [5, 5, 10, 15, 20],  # 阶梯式增长
        '-1106233488.150': [7, 10, 14, 19, 20]  # 加速增长
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