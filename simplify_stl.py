# 简化STL文件面数：
# STL文件面数太多（超过MuJoCo默认200,000 面限制）
# 简化方法
# 用trimesh（Python 3D 网格处理库）+ fast-simplification（快速网格简化 C++ 扩展），基于二次边折叠（Quadric Edge Decimation）算法。
# 算法原理：每次折叠一条边（合并两个顶点为1个），选择对模型形状影响最小的边优先折叠，反复执行直到面数降到目标值。保留大尺度几何特征，减少小尺度三角面细节。
# 参数 aggression（0-10）可调节速度/质量权衡，默认 0 最慢但质量最好。


# 参数	              作用	                    建议值
# MAX_FACES	    面数红线，超过就简化	 180000（稳妥，留余量）
# face_count	目标面数，减到多少	     int(MAX_FACES * 0.9) 即 162K
# aggression	速度/质量权衡，0-10	    不填默认 0（质量最高）


# 如果需要更激进地简化，修改目标面数，比如想降到 10 万面：
# simplified = mesh.simplify_quadric_decimation(face_count=100000)


# 如果想一次批量处理整个文件夹，把脚本里 stl_file 单文件改成循环遍历：
# stl_dir = r"你的目录路径"
# for f in os.listdir(stl_dir):
#     if not f.endswith('.STL'):
#         continue
#     stl_file = os.path.join(stl_dir, f)
#     # ... 后面同样的简化逻辑


import trimesh
import os

# === 修改这里的路径为你自己的 STL 文件路径 ===
stl_file = r"D:/IsaacLab/source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/config/AnLi/unitree_rl_gym-main/resources/robots/Bennett_test2/meshes/base1.STL"

# MuJoCo 允许的最大面数
MAX_FACES = 180000

# 读取 STL 文件
mesh = trimesh.load(stl_file)
current_faces = len(mesh.faces)
print(f"当前面数: {current_faces}")

# 如果超出限制，简化
if current_faces > MAX_FACES:
    target = int(MAX_FACES * 0.9)  # 目标面数：162000
    print(f"超过 {MAX_FACES} 限制，简化到 {target} 面...")

    # 备份原始文件
    bak_file = stl_file + ".bak1"
    os.rename(stl_file, bak_file)
    print(f"原始文件备份到: {bak_file}")

    # 二次边折叠简化
    simplified = mesh.simplify_quadric_decimation(face_count=target)
    result_faces = len(simplified.faces)
    print(f"简化完成: {result_faces} 面")

    # 保存简化后的文件
    simplified.export(stl_file)
    print(f"简化后文件保存到: {stl_file}")
else:
    print(f"面数 {current_faces} 在限制 {MAX_FACES} 以内，无需简化")
