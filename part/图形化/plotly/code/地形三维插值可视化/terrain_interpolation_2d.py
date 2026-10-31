"""
二维插值算法示例：地形数据的三次插值与3D可视化
基于离散的地形高程数据，使用二维三次插值生成平滑的地形表面
"""

import os
import numpy as np
import pandas as pd
from scipy.interpolate import RectBivariateSpline
import plotly.graph_objects as go

# 创建输出目录
os.makedirs('outputs', exist_ok=True)


# ============== 1. 加载地形数据 ==============
# 读取CSV文件中的地形高程数据（7行×8列的矩阵）
temp = pd.read_csv('terrain.csv')
print("原始地形数据:")
print(temp)

# 定义X轴坐标（8个点，范围1200-4000）
x = np.array([1200, 1600, 2000, 2400, 2800, 3200, 3600, 4000])

# 定义Y轴坐标（7个点，范围1200-3600，需要递增排序）
y = np.array([1200, 1600, 2000, 2400, 2800, 3200, 3600])

# 定义Z轴数据（高程），需要反转行顺序以匹配递增的y坐标
z = np.array(temp)[::-1]  # 反转行顺序


# ============== 2. 二维三次插值 ==============
# 二维三次插值是对二维数据进行插值的方法，通过三次多项式拟合
# 可以将稀疏的网格数据插值成高密度的平滑曲面
# 使用RectBivariateSpline替代已弃用的interp2d

# 构造二维三次样条插值器（kx=3, ky=3表示三次插值）
interpreter = RectBivariateSpline(y, x, z, kx=3, ky=3)

# 生成插值后的高密度网格
# X方向：从1200到4000均匀分布120个点
X = np.linspace(1200, 4000, num=120, endpoint=True)

# Y方向：从1200到3600均匀分布100个点
Y = np.linspace(1200, 3600, num=100, endpoint=True)

# 计算插值结果，得到100×120的高程矩阵
Z = interpreter(Y, X)

print(f"\n插值前网格: {z.shape[0]}×{z.shape[1]} = {z.shape[0]*z.shape[1]}个点")
print(f"插值后网格: {Z.shape[0]}×{Z.shape[1]} = {Z.shape[0]*Z.shape[1]}个点")


# ============== 3. 创建3D地形可视化 ==============
# 使用Plotly创建交互式三维曲面图

# 创建网格坐标
X_grid, Y_grid = np.meshgrid(X, Y)

# 创建3D曲面图
fig = go.Figure(data=[go.Surface(
    x=X_grid,
    y=Y_grid,
    z=Z,
    colorscale=[
        [0.0, '#313695'],   # 深蓝
        [0.1, '#4575b4'],
        [0.2, '#74add1'],
        [0.3, '#abd9e9'],
        [0.4, '#e0f3f8'],
        [0.5, '#ffffbf'],   # 黄色
        [0.6, '#fee090'],
        [0.7, '#fdae61'],
        [0.8, '#f46d43'],
        [0.9, '#d73027'],
        [1.0, '#a50026'],   # 深红
    ],
    colorbar=dict(
        title=dict(
            text="高程 (m)",
            side="right"
        )
    ),
    name='地形高程'
)])

# 设置布局
fig.update_layout(
    title='地形三维插值可视化',
    scene=dict(
        xaxis_title='X坐标',
        yaxis_title='Y坐标',
        zaxis_title='高程 (m)',
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.3)  # 设置初始视角
        )
    ),
    width=1000,
    height=800,
)

# 保存为HTML文件
output_file = 'outputs/terrain_3d_interpolation.html'
fig.write_html(output_file)
print(f"\n已保存3D可视化: {output_file}")
print("请在浏览器中打开HTML文件查看交互式3D地形图")
print("提示: 可以用鼠标拖拽旋转、滚轮缩放、右键平移")

print("\n二维插值计算完成！")
