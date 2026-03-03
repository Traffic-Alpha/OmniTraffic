###
 # @Author: WANG Maonan
 # @Date: 2025-08-11 17:19:12
 # @LastEditors: WANG Maonan
 # @Description: 渲染单个场景
 # @Example 渲染单个时间步 ./renderers/render_single.sh --start 250 --end 251 --models high_poly
 # @LastEditTime: 2025-11-20 19:00:56
###
#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 默认参数值
DEFAULT_START=0 # 初始没有车辆
DEFAULT_END=600
DEFAULT_RESOLUTION=480
DEFAULT_MODELS="high_poly"
DEFAULT_BLEND="$PROJECT_ROOT/../exp_networks/France_Massy/env_buildings.blend"
DEFAULT_SCENARIO="$PROJECT_ROOT/../exp_dataset/France_Massy_easy_random_perturbation_crashed/"
DEFAULT_TSHUB="$PROJECT_ROOT/../"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        --start)
            START="$2"
            shift 2
            ;;
        --end)
            END="$2"
            shift 2
            ;;
        --resolution)
            RESOLUTION="$2"
            shift 2
            ;;
        --models)
            MODELS="$2"
            shift 2
            ;;
        --blend)
            BLEND_FILE="$2"
            shift 2
            ;;
        --scenario)
            SCENARIO_PATH="$2"
            shift 2
            ;;
        --tshub)
            TSHUB_PATH="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 设置默认值（如果用户未提供）
START=${START:-$DEFAULT_START}
END=${END:-$DEFAULT_END}
RESOLUTION=${RESOLUTION:-$DEFAULT_RESOLUTION}
MODELS=${MODELS:-$DEFAULT_MODELS}
BLEND_FILE=${BLEND_FILE:-$DEFAULT_BLEND}
SCENARIO_PATH=${SCENARIO_PATH:-$DEFAULT_SCENARIO}
TSHUB_PATH=${TSHUB_PATH:-$DEFAULT_TSHUB}

# 打印配置信息
echo "┌──────────────────────────────────────────────┐"
echo "│           Blender 渲染配置参数                 │"
echo "├──────────────────────────────────────────────┤"
echo "│ 起始时间步: $START"
echo "│ 结束时间步: $END"
echo "│ 输出图像分辨率: $RESOLUTION"
echo "│ 模型精度:   $MODELS"
echo "│ Blend文件:  $BLEND_FILE"
echo "│ 场景路径:   $SCENARIO_PATH"
echo "│ TransSimHub: $TSHUB_PATH"
echo "└──────────────────────────────────────────────┘"

# 启动Blender渲染
# blender "$BLEND_FILE" --background --python render_scene.py -- \
#     --tshub "$TSHUB_PATH" \
#     --scenario "$SCENARIO_PATH" \
#     --start "$START" \
#     --end "$END" \
#     --resolution "$RESOLUTION" \
#     --models "$MODELS"

/home/tshub/blender/blender-4.5.2/blender "$BLEND_FILE" --background --python "$SCRIPT_DIR/render_scene.py" -- \
    --tshub "$TSHUB_PATH" \
    --scenario "$SCENARIO_PATH" \
    --start "$START" \
    --end "$END" \
    --resolution "$RESOLUTION" \
    --models "$MODELS"

# 检查退出状态
if [ $? -eq 0 ]; then
    echo "✅ 渲染成功完成!"
else
    echo "❌ 渲染过程中出错!"
fi