'''
Author: WANG Maonan
Date: 2025-07-17 13:01:58
LastEditors: WANG Maonan
Description: 车辆 Route 生成
LastEditTime: 2025-08-21 16:00:50
'''
from tshub.utils.init_log import set_logger
from tshub.utils.get_abs_path import get_abs_path
from tshub.sumo_tools.generate_routes import generate_route

# 初始化日志
current_file_path = get_abs_path(__file__)
set_logger(current_file_path('./'), file_log_level='WARNING', terminal_log_level='INFO')

# 开启仿真 --> 指定 net 文件
sumo_net = current_file_path("./networks/easy.net.xml")

traffic_flow_configs = {
    # 1. 稳定低密度车流 (Stable Low-Density Flow)
    "low_density": {
        '989312046#0': [11, 11, 11, 11, 11],
        '315156946#0': [13, 13, 13, 13, 13],
        '525074961#6': [14, 14, 14, 14, 14], 
        'E1': [10, 10, 10, 10, 10],
    },
    
    # 2. 波动通勤车流 (Fluctuating Commuter Flow)
    "fluctuating_commuter": {
        '989312046#0': [5, 20, 5, 20, 6],  # 高峰低谷交替
        '315156946#0': [10, 22, 28, 22, 10],  # 强波动性
        '525074961#6': [13, 18, 11, 21, 14],   # 中等波动
        'E1': [14, 22, 34, 22, 15], # 中等波动
    },
    
    # 3. 饱和高密度车流 (Saturated High-Density Flow)
    "high_density": {
        '989312046#0': [24, 24, 24, 24, 24],  # 车道近饱和
        '315156946#0': [30, 30, 30, 30, 30],  # 稳定高负载
        '525074961#6': [18, 18, 18, 18, 18],   # 持续高压
        'E1': [17, 17, 17, 17, 17], # 稳定高负载
    },
    
    # 4. 随机扰动车流 (Random Perturbation Flow)
    "random_perturbation": {
        '989312046#0': [25, 5, 20, 7, 15], 
        '315156946#0': [26, 5, 40, 16, 25], 
        '525074961#6': [25, 20, 10, 20, 20],
        'E1': [30, 27, 10, 18, 22],
    },
    
    # 5. 递增需求车流 (Increasing Demand Flow)
    "increasing_demand": {
        '989312046#0': [5, 10, 15, 10, 10],  # 线性增长
        '315156946#0': [10, 30, 40, 20, 20],  # 阶梯式增长
        '525074961#6': [5, 10, 16, 10, 8],  # 加速增长
        'E1': [10, 20, 32, 32, 20], # 阶梯式增长
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