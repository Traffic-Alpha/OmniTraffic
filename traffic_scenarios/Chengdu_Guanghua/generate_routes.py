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
        '-885943869#2.897': [8, 6, 8, 5, 7],
        '170446483#0.356': [8, 9, 6, 8, 7],
        '885943869#0.263': [9, 8, 8, 7, 8],
        '806740830#0.118': [8, 6, 8, 6, 8],
    },
    
    # 2. 波动通勤车流 (Fluctuating Commuter Flow)
    "fluctuating_commuter": {
        '-885943869#2.897': [6, 21, 5, 19, 4],  # 高峰低谷交替
        '806740830#0.118': [6, 15, 6, 12, 5],  # 强波动性
        '170446483#0.356': [5, 12, 5, 11, 6],   # 中等波动
        '885943869#0.263': [12, 17, 10, 9, 16], # 中等波动
        
    },
    
    # 3. 饱和高密度车流 (Saturated High-Density Flow)
    "high_density": {
        '-885943869#2.897': [19, 19, 19, 19, 19],  # 车道近饱和
        '806740830#0.118': [17, 17, 17, 17, 17],  # 稳定高负载
        '170446483#0.356': [15, 15, 15, 15, 15],   # 持续高压
        '885943869#0.263': [17, 17, 17, 17, 17], # 稳定高负载
    },
    
    # 4. 随机扰动车流 (Random Perturbation Flow)
    "random_perturbation": {
        '-885943869#2.897': [12, 3, 19, 15, 14], 
        '806740830#0.118': [14, 2, 15, 11, 9], 
        '170446483#0.356': [9, 8, 4, 15, 11],
        '885943869#0.263': [9, 8, 5, 12, 11],
    },
    
    # 5. 递增需求车流 (Increasing Demand Flow)
    "increasing_demand": {
        '-885943869#2.897': [3, 7, 11, 15, 19],  # 线性增长
        '806740830#0.118': [8, 8, 15, 15, 22],  # 阶梯式增长
        '170446483#0.356': [7, 9, 12, 15, 20],  # 加速增长
        '885943869#0.263': [6, 10, 14, 18, 22],  # 线性增长
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