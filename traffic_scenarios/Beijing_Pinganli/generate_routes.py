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
        '-156465481#3.628.100': [8, 6, 9, 5, 7],
        '169221931#0.91': [10, 12, 8, 9, 9],
        '156465483#0.660': [6, 8, 8, 7, 8],
        '33610069#0.1159': [10, 11, 9, 10, 10],
    },
    
    # 2. 波动通勤车流 (Fluctuating Commuter Flow)
    "fluctuating_commuter": {
        '-156465481#3.628.100': [5, 19, 4, 15, 3],  # 高峰低谷交替
        '169221931#0.91': [5, 22, 3, 18, 3],  # 强波动性
        '156465483#0.660': [7, 13, 6, 12, 4],   # 中等波动
        '33610069#0.1159': [10, 19, 8, 10, 15],  # 中等波动
    },
    
    # 3. 饱和高密度车流 (Saturated High-Density Flow)
    "high_density": {
        '-156465481#3.628.100': [18, 18, 18, 18, 18],  # 车道近饱和
        '169221931#0.91': [22, 22, 22, 22, 22],  # 稳定高负载
        '156465483#0.660': [15, 15, 15, 15, 15],   # 持续高压
        '33610069#0.1159': [23, 23, 23, 23, 23],   # 稳定高负载
    },
    
    # 4. 随机扰动车流 (Random Perturbation Flow)
    "random_perturbation": {
        '-156465481#3.628.100': [11, 3, 17, 5, 8], 
        '169221931#0.91': [18, 3, 30, 8, 12], 
        '156465483#0.660': [9, 8, 4, 15, 12],
        '33610069#0.1159': [10, 18, 15, 12, 10],
    },
    
    # 5. 递增需求车流 (Increasing Demand Flow)
    "increasing_demand": {
        '-156465481#3.628.100': [6, 9, 12, 15, 18],  # 线性增长
        '169221931#0.91': [11, 11, 18, 18, 25],  # 阶梯式增长
        '156465483#0.660': [8, 10, 14, 20, 20],  # 加速增长
        '33610069#0.1159': [8, 12, 16, 20, 24],   # 线性增长
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