# Pytorch笔记

<!-- TOC -->

- [Pytorch笔记](#pytorch%e7%ac%94%e8%ae%b0)
  - [入门](#%e5%85%a5%e9%97%a8)
  - [张量](#%e5%bc%a0%e9%87%8f)
  - [神经网络](#%e7%a5%9e%e7%bb%8f%e7%bd%91%e7%bb%9c)
    - [简单的前馈神经网络](#%e7%ae%80%e5%8d%95%e7%9a%84%e5%89%8d%e9%a6%88%e7%a5%9e%e7%bb%8f%e7%bd%91%e7%bb%9c)
      - [训练流程](#%e8%ae%ad%e7%bb%83%e6%b5%81%e7%a8%8b)
      - [损失函数](#%e6%8d%9f%e5%a4%b1%e5%87%bd%e6%95%b0)
- [fairseq](#fairseq)

<!-- /TOC -->
## 入门

PyTorch是一个Python包，提供两个高级功能：

- 具有强大的GPU加速的张量计算（如NumPy）

- 包含自动求导系统的的深度神经网络

## 张量

```python

# 创建张量
import torch
x = torch.empty(5,3)                   # 创建空的张量(未初始化)
x = torch.rand(5,3)                    # 创建随机张量(在[0,1)中完全随机)
x = torch.randn(5,3)                   # 创建随机张量(正态分布)
x = torch.zeros(5,3,dtype=torch.long)  # 创建全0的,元素类型为long的张量
x = torch.ones(5,3)                    # **创建全1的**
x = torch.tensor([5.5,3])              # 创建张量并初始化
x = x.new_ones(5, 3, dtype=torch.double)      # new_* 方法来创建对象
x = torch.randn_like(x, dtype=torch.float)    # 覆盖 dtype,生成的对象的大小和传入的相同,只是值和类型发生了变化
print(x.size())                        # torch.Size([5, 3])

# 张量操作
print(x + y)                           # 方法一: 直接进行加法
print(torch.add(x, y))                 # 方法二: 利用成员函数进行加法

result = torch.empty(5, 3)             # 方法三: 指定输出对象
torch.add(x, y, out=result)
print(result)

y.add_(x)                              # 方法四: 注意,这种方法(以下划线结尾的方法,会导致y本身值的改变)
print(y)

# 你可以使用与NumPy索引方式相同的操作来进行对张量的操作(还需深入学习)

# view的基本原理是把张量排成一行,然后再根据给的参数进行重新排列
x = torch.randn(4, 4)                  # 大小为4*4
y = x.view(16)                         # 大小为16*1
z = x.view(-1, 8)                      # 某一维的大小如果为-1,则从其他维度推断,最多只能有一个-1出现.故Z的大小是2*8.如果没有-1存在,则各维度的乘积必须等于原张量的元素个数


# 注: torch和numpy虽然可以互相转化,但是其本质上使用了相同的内存空间,所以下文的a和b会被同步修改

# torch -> numpy
a = torch.ones(5)
b = a.numpy()

# numpy -> torch
import numpy as np
a = np.ones(5)
b = torch.from_numpy(a)


# CUDA 张量
# is_available 函数判断是否有cuda可以使用
# ``torch.device``将张量移动到指定的设备中
if torch.cuda.is_available():
    device = torch.device("cuda")          # a CUDA 设备对象
    y = torch.ones_like(x, device=device)  # 直接从GPU创建张量
    x = x.to(device)                       # 或者直接使用``.to("cuda")``将张量移动到cuda中
    z = x + y
    print(z)
    print(z.to("cpu", torch.double))       # ``.to`` 也会对变量的类型做更改
```

## 神经网络

### 简单的前馈神经网络

#### 训练流程

1. 定义包含一些可学习的参数(或者叫权重)神经网络模型；
2. 在数据集上迭代；
3. 通过神经网络处理输入；
4. 计算损失(输出结果和正确值的差值大小)；
5. 将梯度反向传播回网络的参数；(这里主要用autograd自动求导的方式,它会自动生成backward函数)
6. 更新网络的参数，主要使用如下简单的更新原则： `weight = weight - learning_rate * gradient`

在自己写网络的时候,应该是初始化和forward必须自己写

#### 损失函数
#  fairseq
一个损失函数接受一对 (output, target) 作为输入，计算一个值来估计网络的输出和目标值相差多少。


r任务
具体做方法
计划

1. 从头开始 明确 任务目标 目的 数据集 合理性分析  解决方法 方法评估
2. 工作计划
3. 未来规划

ppt:
1. 主要工作进度收获
目的和作用
2. 我对任务的理解程度
3. 目的 意义 评价指标
