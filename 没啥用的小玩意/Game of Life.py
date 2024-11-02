import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 设置生命游戏的规则
def update(frameNum, img, grid, N):
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):

            # 计算周围的活细胞数量
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)

            # 应用生命游戏的规则
            if grid[i, j]  == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON

    # 更新数据
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# 设置网格大小
N = 100
# 设置活细胞和死细胞的状态
ON = 255
OFF = 0
# 创建一个N*N的网格
grid = np.array([[OFF] * N for _ in range(N)])

# 随机挑选几个细胞作为起始的活细胞
for i in range(N):
    for j in range(N):
        if np.random.choice([True, False]):
            grid[i][j] = ON

# 设置动画
fig, ax = plt.subplots()
img = ax.imshow(grid, cmap='gray', interpolation='nearest')
ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N), frames = 10, interval=10, save_count=50)

# 不显示坐标
plt.axis('off')

# 显示动画
plt.show()
