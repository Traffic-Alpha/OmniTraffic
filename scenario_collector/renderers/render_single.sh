#!/bin/bash
###
 # @Author: WANG Maonan
 # @Date: 2025-08-11 17:19:12
 # @LastEditors: Please set LastEditors
 # @Description: 渲染单个场景
 # @Example 渲染单个时间步 ./renderers/render_single.sh --start 250 --end 251 --models high_poly --render_mask --render_depth
 # @LastEditTime: 2026-03-04 19:59:01
###

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 默认参数值
DEFAULT_START=400 # 初始时间
DEFAULT_END=405
DEFAULT_RESOLUTION=480
DEFAULT_MODELS="high_poly"
DEFAULT_BLEND="$PROJECT_ROOT/../traffic_scenarios/Hongkong_YMT/env.blend"
DEFAULT_SCENARIO="$PROJECT_ROOT/../scenario_dataset/Hongkong_YMT_normal_fluctuating_commuter_barrier/"
DEFAULT_TSHUB="$PROJECT_ROOT/../TransSimHub/"
DEFAULT_BLENDER_PATH="/home/wmn/blender-4.4.3-linux-x64/blender"
DEFAULT_RENDER_MASK=false
DEFAULT_RENDER_DEPTH=false

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
        --blender_path)
            BLENDER_PATH="$2"
            shift 2
            ;;
        --render_mask)
            RENDER_MASK=true
            shift 1
            ;;
        --render_depth)
            RENDER_DEPTH=true
            shift 1
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
BLENDER_PATH=${BLENDER_PATH:-$DEFAULT_BLENDER_PATH}
RENDER_MASK=${RENDER_MASK:-$DEFAULT_RENDER_MASK}
RENDER_DEPTH=${RENDER_DEPTH:-$DEFAULT_RENDER_DEPTH}

# 打印配置信息
echo "┌──────────────────────────────────────────────┐"
echo "│           Blender 渲染配置参数                 │"
echo "├──────────────────────────────────────────────┤"
echo "│ 起始时间步: $START"
echo "│ 结束时间步: $END"
echo "│ 输出图像分辨率: $RESOLUTION"
echo "│ 模型精度:   $MODELS"
echo "│ 渲染Mask:   $RENDER_MASK"
echo "│ 渲染Depth:  $RENDER_DEPTH"
echo "│ Blender路径: $BLENDER_PATH"
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

"$BLENDER_PATH" "$BLEND_FILE" --background --python "$SCRIPT_DIR/render_scene.py" -- \
    --tshub "$TSHUB_PATH" \
    --scenario "$SCENARIO_PATH" \
    --start "$START" \
    --end "$END" \
    --resolution "$RESOLUTION" \
    --models "$MODELS" \
    $(if [ "$RENDER_MASK" = true ]; then echo "--render_mask"; fi) \
    $(if [ "$RENDER_DEPTH" = true ]; then echo "--render_depth"; fi)

# 检查退出状态
if [ $? -eq 0 ]; then
    echo "✅ 渲染成功完成!"
else
    echo "❌ 渲染过程中出错!"
fi