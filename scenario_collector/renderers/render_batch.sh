###
 # @Author: WANG Maonan
 # @Date: 2025-08-14 16:59:25
 # @LastEditors: WANG Maonan
 # @Description: 批量渲染多个场景
 # @LastEditTime: 2025-11-20 18:59:55
###
#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 定义场景路径数组
SCENARIOS=(
    "$PROJECT_ROOT/../exp_dataset/Hongkong_YMT_normal_fluctuating_commuter_barrier"
    "$PROJECT_ROOT/../exp_dataset/Hongkong_YMT_normal_fluctuating_commuter_none"
)

blender="$PROJECT_ROOT/../exp_networks/Hongkong_YMT/env_new.blend"

# 遍历所有场景并执行render_single.sh
for scenario in "${SCENARIOS[@]}"; do
    echo "正在处理场景: $scenario"
    "$SCRIPT_DIR/render_single.sh" --scenario "$scenario" --blend "$blender"

    # 检查上一个命令的退出状态
    if [ $? -ne 0 ]; then
        echo "错误: 处理场景 $scenario 时失败"
        exit 1
    fi

    echo "场景 $scenario 处理完成"
    echo "----------------------------------------"
done

echo "所有场景处理完成！"