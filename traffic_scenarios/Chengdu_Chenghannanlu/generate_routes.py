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
        '458749037#0.1098': [6, 5, 8, 6, 6],
        '471999771#0.1574': [7, 5, 5, 7, 6],
        '845412822.360': [8, 6, 7, 6, 7],
    },
    
    # 2. 波动通勤车流 (Fluctuating Commuter Flow)
    "fluctuating_commuter": {
        '458749037#0.1098': [4, 17, 4, 15, 3],  # 高峰低谷交替
        '471999771#0.1574': [4, 15, 4, 12, 2],  # 强波动性
        '845412822.360': [6, 12, 5, 11, 6],   # 中等波动
    },
    
    # 3. 饱和高密度车流 (Saturated High-Density Flow)
    "high_density": {
        '458749037#0.1098': [13, 13, 13, 13, 13],  # 持续高压
        '471999771#0.1574': [15, 15, 15, 15, 15],  # 稳定高负载
        '845412822.360': [16, 16, 16, 16, 16],   # 车道近饱和
    },
    
    # 4. 随机扰动车流 (Random Perturbation Flow)
    "random_perturbation": {
        '458749037#0.1098': [11, 4, 12, 5, 6], 
        '471999771#0.1574': [13, 3, 19, 6, 8], 
        '845412822.360': [15, 13, 4, 13, 12],
    },
    
    # 5. 递增需求车流 (Increasing Demand Flow)
    "increasing_demand": {
        '458749037#0.1098': [7, 10, 16, 20, 24],  # 加速增长 
        '471999771#0.1574': [5, 5, 10, 15, 20],  # 阶梯式增长
        '845412822.360': [4, 7, 10, 13, 17],  # 线性增长
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