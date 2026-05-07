'''
Author: WANG Maonan
Date: 2025-08-04 16:09:06
LastEditors: WANG Maonan
Description: Beijing Beihuan
LastEditTime: 2025-08-04 17:39:24
'''
Beijing_Beihuan = {
    # ============================
    # Easy + With Special Events
    # ============================
    "Beijing_Beihuan_Event_easy_fluctuating_commuter": {
    "SPECIAL_VEHICLES": [
        #-----------------3
        {
            "id": "ambulance_03",
            "type": "emergency",
            "depart_time": 115,
            "route": ["252712271#0.589", "-157863208#1"],
        },
        {
            "id": "police_03",
            "type": "police",
            "depart_time": 110,
            "route": ["252712271#0.589","1106233488"],
        },
        #----------------4
        {
            "id": "police_04",
            "type": "police",
            "depart_time": 340,
            "route": ["-1106233488.150", "-252712271#1"],
        },
        #----------------5
        {
            "id": "ambulance_05",
            "type": "emergency",
            "depart_time": 385,
            "route": ["252712271#0.589", "-157863208#1"],
        },
        {
            "id": "fire_05",
            "type": "fire_engine",
            "depart_time": 378, 
            "route": ["-1106233488.150", "-157863208#1"],
        }
    ]},
    "Beijing_Beihuan_Event_easy_high_density": {
            "SCENARIO_NAME": "Beijing_Beihuan", 
            "SUMOCFG": "easy_high_density.sumocfg",
            "NETFILE": "./networks/easy.net.xml",
            "JUNCTION_NAME": "INT1",
            "NUM_SECONDS": 600,
            "PHASE_NUMBER": 3,
            "MOVEMENT_NUMBER": 6,
            "CENTER_COORDINATES": (835, 360, 50),
            "SENSOR_INDEX_2_PHASE_INDEX": {0:2, 1:1, 2:0},
            # ========================================
            "ACCIDENTS": [
            {
                "id": "accident_01",
                "depart_time": 93,
                "edge_id": "252712271#0.589",  
                "lane_index": 0,
                "position": 290,
                "duration": 117,
            },
        ],
        "SPECIAL_VEHICLES": [
            {
                "id": "police_01",
                "type": "police",
                "depart_time": 305,
                "route": ["157863208#0.1590","-252712271#1"],
            },
            #-----------------3
            {
                "id": "ambulance_01",
                "type": "emergency",
                "depart_time": 440,
                "route": ["157863208#0.1590","1106233488"],
            },
            {
                "id": "fire_01",
                "type": "fire_engine",
                "depart_time": 435,
                "route": ["157863208#0.1590","1106233488"],
            }
        ]
    },
    "Beijing_Beihuan_Event_easy_increasing_demand": {
            "SCENARIO_NAME": "Beijing_Beihuan", 
            "SUMOCFG": "easy_increasing_demand.sumocfg",
            "NETFILE": "./networks/easy.net.xml",
            "JUNCTION_NAME": "INT1",
            "NUM_SECONDS": 600,
            "PHASE_NUMBER": 3,
            "MOVEMENT_NUMBER": 6,
            "CENTER_COORDINATES": (835, 360, 50),
            "SENSOR_INDEX_2_PHASE_INDEX": {0:2, 1:1, 2:0},
            # ========================================
            "ACCIDENTS": [
            {
                "id": "accident_01",
                "depart_time": 31,
                "edge_id": "157863208#0.1590",  
                "lane_index": 1,
                "position": 218,
                "duration": 129,
            },
            {
                "id": "accident_02",
                "depart_time": 232,
                "edge_id": "-1106233488.150",  
                "lane_index": 0,
                "position": 197,
                "duration": 121,
            }
        ],
        "SPECIAL_VEHICLES": [
            {
                "id": "police_01",
                "type": "police",
                "depart_time": 45,
                "route": ["252712271#0.589","1106233488"],
            },
        ]
    },
    "Beijing_Beihuan_Event_easy_low_density": {
            "SCENARIO_NAME": "Beijing_Beihuan", 
            "SUMOCFG": "easy_low_density.sumocfg",
            "NETFILE": "./networks/easy.net.xml",
            "JUNCTION_NAME": "INT1",
            "NUM_SECONDS": 600,
            "PHASE_NUMBER": 3,
            "MOVEMENT_NUMBER": 6,
            "CENTER_COORDINATES": (835, 360, 50),
            "SENSOR_INDEX_2_PHASE_INDEX": {0:2, 1:1, 2:0},
            # ========================================
            "ACCIDENTS": [
            {
                "id": "accident_01",
                "depart_time": 36,
                "edge_id": "157863208#0.1590",  
                "lane_index": 1,
                "position": 218,
                "duration": 82,
            },
            {
                "id": "accident_02",
                "depart_time": 220,
                "edge_id": "252712271#0.589",  
                "lane_index": 0,
                "position": 290,
                "duration": 86,
            },
            {
                "id": "accident_03",
                "depart_time": 429,
                "edge_id": "-1106233488.150",  
                "lane_index": 0,
                "position": 197,
                "duration": 137,
            },
        ],
        "SPECIAL_VEHICLES": [
            {
                "id": "ambulance_03",
                "type": "emergency",
                "depart_time": 450,
                "route": ["157863208#0.1590","-252712271#1"],
            },
            {
                "id": "police_03",
                "type": "police",
                "depart_time": 445,
                "route": ["157863208#0.1590","-252712271#1"],
            },
            {
                "id": "fire_03",
                "type": "fire_engine",
                "depart_time": 440,
                "route": ["-1106233488.150","-252712271#1"],
            },
        ]
    },
    "Beijing_Beihuan_Event_easy_random_perturbation": {
            "SCENARIO_NAME": "Beijing_Beihuan", 
            "SUMOCFG": "easy_random_perturbation.sumocfg",
            "NETFILE": "./networks/easy.net.xml",
            "JUNCTION_NAME": "INT1",
            "NUM_SECONDS": 600,
            "PHASE_NUMBER": 3,
            "MOVEMENT_NUMBER": 6,
            "CENTER_COORDINATES": (835, 360, 50),
            "SENSOR_INDEX_2_PHASE_INDEX": {0:2, 1:1, 2:0},
            # ========================================
            "ACCIDENTS": [
            {
                "id": "accident_01",
                "depart_time": 113,
                "edge_id": "157863208#0.1590",  
                "lane_index": 1,
                "position": 218,
                "duration": 91,
            },
            {
                "id": "accident_02",
                "depart_time": 313,
                "edge_id": "-1106233488.150",  
                "lane_index": 1,
                "position": 197,
                "duration": 139,
            },
            {
                "id": "accident_03",
                "depart_time": 509,
                "edge_id": "252712271#0.589",  
                "lane_index": 1,
                "position": 290,
                "duration": 88,
            }
        ],
        "SPECIAL_VEHICLES": [
            {
                "id": "police_01",
                "type": "police",
                "depart_time": 128,
                "route": ["252712271#0.589","1106233488"],
            },
            {
                "id": "fire_01",
                "type": "fire_engine",
                "depart_time": 132, 
                "route": ["157863208#0.1590","1106233488"],
            },
            {
                "id": "police_02",
                "type": "police",
                "depart_time": 525,
                "route": ["-1106233488.150","-252712271#1"],
            },
            {
                "id": "ambulance_01",
                "type": "emergency",
                "depart_time": 530,
                "route": ["-1106233488.150","-252712271#1"],
            },
            {
                "id": "fire_02",
                "type": "fire_engine",
                "depart_time": 519,
                "route": ["157863208#0.1590","-252712271#1"],
            }
        ]
    },
    "Beijing_Beihuan_Event_normal_fluctuating_commuter": {
            "SCENARIO_NAME": "Beijing_Beihuan", 
            "SUMOCFG": "normal_fluctuating_commuter.sumocfg",
            "NETFILE": "./networks/normal.net.xml",
            "JUNCTION_NAME": "INT1",
            "NUM_SECONDS": 600,
            "PHASE_NUMBER": 3,
            "MOVEMENT_NUMBER": 6,
            "CENTER_COORDINATES": (835, 360, 50),
            "SENSOR_INDEX_2_PHASE_INDEX": {0:2, 1:1, 2:0},
            # ========================================
            "ACCIDENTS": [
            {
                "id": "accident_01",
                "depart_time": 33,
                "edge_id": "-1106233488.150",  
                "lane_index": 1,
                "position": 197,
                "duration": 125,
            },
            {
                "id": "accident_02",
                "depart_time": 242,
                "edge_id": "252712271#0.589",  
                "lane_index": 1,
                "position": 290,
                "duration": 103,
            },
            {
                "id": "accident_03",
                "depart_time": 500,
                "edge_id": "157863208#0.1590",  
                "lane_index": 1,
                "position": 218,
                "duration": 93,
            }
        ],
        "SPECIAL_VEHICLES": [
            {
                "id": "police_01",
                "type": "police",
                "depart_time": 255,
                "route": ["157863208#0.1590","1106233488"],
            },
            {
                "id": "fire_01",
                "type": "fire_engine",
                "depart_time": 248, 
                "route": ["157863208#0.1590","1106233488"],
            },
            {
                "id": "ambulance_01",
                "type": "emergency",
                "depart_time": 260,
                "route": ["157863208#0.1590","1106233488"],
            }
        ]
    },
    "Beijing_Beihuan_Event_normal_high_density": {
            "SCENARIO_NAME": "Beijing_Beihuan", 
            "SUMOCFG": "normal_high_density.sumocfg",
            "NETFILE": "./networks/normal.net.xml",
            "JUNCTION_NAME": "INT1",
            "NUM_SECONDS": 600,
            "PHASE_NUMBER": 3,
            "MOVEMENT_NUMBER": 6,
            "CENTER_COORDINATES": (835, 360, 50),
            "SENSOR_INDEX_2_PHASE_INDEX": {0:2, 1:1, 2:0},
            # ========================================
            "ACCIDENTS": [
            {
                "id": "accident_01",
                "depart_time": 36,
                "edge_id": "-1106233488.150",  
                "lane_index": 1,
                "position": 197,
                "duration": 84,
            },
            {
                "id": "accident_02",
                "depart_time": 238,
                "edge_id": "157863208#0.1590",  
                "lane_index": 1,
                "position": 218,
                "duration": 124,
            }
        ],
        "SPECIAL_VEHICLES": [
            {
                "id": "police_01",
                "type": "police",
                "depart_time": 355,
                "route": ["157863208#0.1590","1106233488"],
            },
            {
                "id": "ambulance_01",
                "type": "emergency",
                "depart_time": 357,
                "route": ["252712271#0.589","1106233488"],
            },
            {
                "id": "fire_01",
                "type": "fire_engine",
                "depart_time": 349,
                "route": ["157863208#0.1590","1106233488"],
            },
            {
                "id": "police_02",
                "type": "police",
                "depart_time": 500,
                "route": ["252712271#0.589","-157863208#1"],
            },
            {
                "id": "police_03",
                "type": "police",
                "depart_time": 529,
                "route": ["252712271#0.589","1106233488"],
            },
            {
                "id": "ambulance_02",
                "type": "emergency",
                "depart_time": 536,
                "route": ["252712271#0.589","1106233488"],
            },
            {
                "id": "fire_02",
                "type": "fire_engine",
                "depart_time": 527,
                "route": ["157863208#0.1590","1106233488"],
            }
        ]
    },
    "Beijing_Beihuan_Event_normal_increasing_demand": {
            "SCENARIO_NAME": "Beijing_Beihuan", 
            "SUMOCFG": "normal_increasing_demand.sumocfg",
            "NETFILE": "./networks/normal.net.xml",
            "JUNCTION_NAME": "INT1",
            "NUM_SECONDS": 600,
            "PHASE_NUMBER": 3,
            "MOVEMENT_NUMBER": 6,
            "CENTER_COORDINATES": (835, 360, 50),
            "SENSOR_INDEX_2_PHASE_INDEX": {0:2, 1:1, 2:0},
            # ========================================
            "ACCIDENTS": [
            {
                "id": "accident_01",
                "depart_time": 58,
                "edge_id": "157863208#0.1590",  
                "lane_index": 1,
                "position": 218,
                "duration": 77,
            },
            {
                "id": "accident_02",
                "depart_time": 342,
                "edge_id": "157863208#0.1590",  
                "lane_index": 1,
                "position": 218,
                "duration": 79,
            },
        ],
        "SPECIAL_VEHICLES": [
            {
                "id": "police_01",
                "type": "police",
                "depart_time": 74,
                "route": ["252712271#0.589","-157863208#1"],
            },
            {
                "id": "fire_01",
                "type": "fire_engine",
                "depart_time": 68,
                "route": ["252712271#0.589","-157863208#1"],
            },
            #-----------------2
            {
                "id": "police_02",
                "type": "police",
                "depart_time": 168,
                "route": ["252712271#0.589","-157863208#1"],
            },
            {
                "id": "ambulance_02",
                "type": "emergency",
                "depart_time": 170,
                "route": ["252712271#0.589","-157863208#1"],
            },
            {
                "id": "fire_02",
                "type": "fire_engine",
                "depart_time": 155,
                "route": ["-1106233488.150","-157863208#1"],
            },
            #-----------------3
            {
                "id": "police_03",
                "type": "police",
                "depart_time": 326,
                "route": ["252712271#0.589","-157863208#1"],
            },
            {
                "id": "ambulance_03",
                "type": "emergency",
                "depart_time": 328,
                "route": ["-1106233488.150","-157863208#1"],
            },
            {
                "id": "fire_03",
                "type": "fire_engine",
                "depart_time": 319,
                "route": ["-1106233488.150","-157863208#1"],
            },
            #----------------4
            {
                "id": "police_04",
                "type": "police",
                "depart_time": 440,
                "route": ["-1106233488.150","-252712271#1"],
            }
        ]
    },
    "Beijing_Beihuan_Event_normal_low_density": {
            "SCENARIO_NAME": "Beijing_Beihuan", 
            "SUMOCFG": "normal_low_density.sumocfg",
            "NETFILE": "./networks/normal.net.xml",
            "JUNCTION_NAME": "INT1",
            "NUM_SECONDS": 600,
            "PHASE_NUMBER": 3,
            "MOVEMENT_NUMBER": 6,
            "CENTER_COORDINATES": (835, 360, 50),
            "SENSOR_INDEX_2_PHASE_INDEX": {0:2, 1:1, 2:0},
            # ========================================
            "ACCIDENTS": [
            {
                "id": "accident_01",
                "depart_time": 59,
                "edge_id": "157863208#0.1590",  
                "lane_index": 1,
                "position": 217,
                "duration": 125,
            },
            {
                "id": "accident_02",
                "depart_time": 267,
                "edge_id": "252712271#0.589",  
                "lane_index": 1,
                "position": 290,
                "duration": 137,
            },
            {
                "id": "accident_03",
                "depart_time": 469,
                "edge_id": "252712271#0.589",  
                "lane_index": 1,
                "position":290,
                "duration": 110,
            }
        ],
        "SPECIAL_VEHICLES": [
            {
                "id": "police_01",
                "type": "police",
                "depart_time": 175,
                "route": ["-1106233488.150","-157863208#1"],
            },
            {
                "id": "ambulance_01",
                "type": "emergency",
                "depart_time": 178,
                "route": ["252712271#0.589","-157863208#1"],
            },
            {
                "id": "fire_01",
                "type": "fire_engine",
                "depart_time": 169,
                "route": ["252712271#0.589","-157863208#1"],
            },
        ]
    },
    "Beijing_Beihuan_Event_normal_random_perturbation": {
            "SCENARIO_NAME": "Beijing_Beihuan", 
            "SUMOCFG": "normal_random_perturbation.sumocfg",
            "NETFILE": "./networks/normal.net.xml",
            "JUNCTION_NAME": "INT1",
            "NUM_SECONDS": 600,
            "PHASE_NUMBER": 3,
            "MOVEMENT_NUMBER": 6,
            "CENTER_COORDINATES": (835, 360, 50),
            "SENSOR_INDEX_2_PHASE_INDEX": {0:2, 1:1, 2:0},
            # ========================================
            "ACCIDENTS": [
            {
                "id": "accident_01",
                "depart_time": 102,
                "edge_id": "-1106233488.150",  
                "lane_index": 1,
                "position": 197,
                "duration": 111,
            },
            {
                "id": "accident_02",
                "depart_time": 227,
                "edge_id": "252712271#0.589",  
                "lane_index": 1,
                "position": 290,
                "duration": 94,
            },
            {
                "id": "accident_03",
                "depart_time": 317,
                "edge_id": "157863208#0.1590",  
                "lane_index": 1,
                "position": 218,
                "duration": 109,
            },
        ],
        "SPECIAL_VEHICLES": [
            {
                "id": "police_01",
                "type": "police",
                "depart_time": 120,
                "route": ["252712271#0.589","1106233488"],
            },
            #-----------------2
            {
                "id": "ambulance_02",
                "type": "emergency",
                "depart_time": 251,
                "route": ["252712271#0.589","-157863208#1"],
            },
            {
                "id": "fire_02",
                "type": "fire_engine",
                "depart_time": 239,
                "route": ["-1106233488.150","-157863208#1"],
            },
            {
                "id": "police_04",
                "type": "police",
                "depart_time": 359,
                "route": ["252712271#0.589","-157863208#1"],
            },
            {
                "id": "ambulance_04",
                "type": "emergency",
                "depart_time": 367,
                "route": ["252712271#0.589","-157863208#1"],
            },
            {
                "id": "fire_04",
                "type": "fire_engine",
                "depart_time": 356,
                "route": ["-1106233488.150","-157863208#1"],
            }
        ]
    }
        # Normal + With Special Events
}