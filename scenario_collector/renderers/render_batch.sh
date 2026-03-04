#!/bin/bash
###
 # @Author: WANG Maonan
 # @Date: 2025-08-14 16:59:25
 # @LastEditors: Please set LastEditors
 # @Description: 批量渲染多个场景
 # @Example: ./renderers/render_batch.sh --start 0 --end 600 --models high_poly --render_mask --render_depth
 # @LastEditTime: 2026-03-04 20:05:41
###
#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 默认参数值
DEFAULT_START=0
DEFAULT_END=600
DEFAULT_RESOLUTION=480
DEFAULT_MODELS="high_poly"
DEFAULT_BLEND="$PROJECT_ROOT/../exp_networks/Hongkong_YMT/env_new.blend"
DEFAULT_TSHUB="$PROJECT_ROOT/../"
DEFAULT_BLENDER_PATH="/home/tshub/blender/blender-4.5.2/blender"
DEFAULT_RENDER_MASK=false
DEFAULT_RENDER_DEPTH=false

# 定义场景路径数组（默认值）
DEFAULT_SCENARIOS=(
    "$PROJECT_ROOT/../exp_dataset/Hongkong_YMT_normal_fluctuating_commuter_barrier"
    "$PROJECT_ROOT/../exp_dataset/Hongkong_YMT_normal_fluctuating_commuter_none"
)

# 解析命令行参数
SCENARIOS=()
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
        --scenario)
            SCENARIOS+=("$2")
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            echo "用法: $0 [选项]"
            echo "选项:"
            echo "  --start <值>         起始时间步 (默认: $DEFAULT_START)"
            echo "  --end <值>           结束时间步 (默认: $DEFAULT_END)"
            echo "  --resolution <值>    输出图像分辨率 (默认: $DEFAULT_RESOLUTION)"
            echo "  --models <值>        模型精度 [high_poly|low_poly] (默认: $DEFAULT_MODELS)"
            echo "  --blend <路径>       Blend文件路径 (默认: 使用默认Hongkong_YMT)"
            echo "  --tshub <路径>       TransSimHub根目录 (默认: PROJECT_ROOT/..)"
            echo "  --blender_path <路径> Blender可执行文件路径 (默认: $DEFAULT_BLENDER_PATH)"
            echo "  --render_mask        启用mask渲染 (默认: 关闭)"
            echo "  --render_depth       启用depth渲染 (默认: 关闭)"
            echo "  --scenario <路径>    场景路径 (可多次指定，默认使用预设场景)"
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
TSHUB_PATH=${TSHUB_PATH:-$DEFAULT_TSHUB}
BLENDER_PATH=${BLENDER_PATH:-$DEFAULT_BLENDER_PATH}
RENDER_MASK=${RENDER_MASK:-$DEFAULT_RENDER_MASK}
RENDER_DEPTH=${RENDER_DEPTH:-$DEFAULT_RENDER_DEPTH}

# 如果用户未指定场景，使用默认场景列表
if [ ${#SCENARIOS[@]} -eq 0 ]; then
    SCENARIOS=("${DEFAULT_SCENARIOS[@]}")
fi

# 打印批量渲染配置信息
echo "┌────────────────────────────────────────────────────┐"
echo "│           Blender 批量渲染配置参数                    │"
echo "├────────────────────────────────────────────────────┤"
echo "│ 起始时间步:     $START"
echo "│ 结束时间步:     $END"
echo "│ 输出图像分辨率: $RESOLUTION"
echo "│ 模型精度:       $MODELS"
echo "│ 渲染Mask:       $RENDER_MASK"
echo "│ 渲染Depth:      $RENDER_DEPTH"
echo "│ Blender路径:    $BLENDER_PATH"
echo "│ Blend文件:      $BLEND_FILE"
echo "│ TransSimHub:    $TSHUB_PATH"
echo "│ 场景总数:       ${#SCENARIOS[@]}"
echo "└────────────────────────────────────────────────────┘"
echo ""

# 遍历所有场景并执行render_single.sh
scenario_count=0
for scenario in "${SCENARIOS[@]}"; do
    scenario_count=$((scenario_count + 1))
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "正在处理场景 [$scenario_count/${#SCENARIOS[@]}]: $scenario"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 构建参数
    CMD_ARGS=(
        --scenario "$scenario"
        --blend "$BLEND_FILE"
        --tshub "$TSHUB_PATH"
        --blender_path "$BLENDER_PATH"
        --start "$START"
        --end "$END"
        --resolution "$RESOLUTION"
        --models "$MODELS"
    )
    
    # 添加可选参数
    if [ "$RENDER_MASK" = true ]; then
        CMD_ARGS+=(--render_mask)
    fi
    
    if [ "$RENDER_DEPTH" = true ]; then
        CMD_ARGS+=(--render_depth)
    fi
    
    # 执行渲染命令
    "$SCRIPT_DIR/render_single.sh" "${CMD_ARGS[@]}"

    # 检查上一个命令的退出状态
    if [ $? -ne 0 ]; then
        echo "❌ 错误: 处理场景 $scenario 时失败"
        exit 1
    fi

    echo "✅ 场景 $scenario 处理完成"
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 所有 ${#SCENARIOS[@]} 个场景处理完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"