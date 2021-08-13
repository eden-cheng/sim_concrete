### **2020.04.30变更（程伟）**

1. 表单原名为 CC 改为 sim_vtd
2. para_hv_init 中增加 lane 属性
3. para_hv_action1 中增加 direction 属性
4. hv和tv的action中均增加 trigger_event 属性，用来解决
   1. 主车参考自车换道时相对车道线的时机的做换道取消的case
   2. 目标车参考主车换道时相对车道线的时机的case
   3. 主车在跟加时或跟减时做换道的case



1. HIL 错写成了 HILL，已修改
2. tvNum 的tag转移到tag_fixed下面，并且更名为targetNum
3. 删除tag_auto的信息
4. CC_7_1的summary中的持续一段时间变量错误，已纠正，并且原参数库中缺少tv1_action2，已增加
5. CC_23_1中两两相距的变量名替换错误，修改为para_tv2_init_relativeTV1. 并且调整了TV1和TV2的前车与前前车的关系
6. CC_23_2中目标2相距目标1切出的距离纠正为para_tv1_action2_triggerRelativeTV2，. 并且调整了TV1和TV2的前车与前前车的关系
7. CC_8_1/2中目标相距主车变量替换为para_tv1_init_relativeHV
8. CC_10_1的cutin减速case，action3中增加trigger
9. 原来对triggerDelay的理解有误，本次新增triggerTime变量，将部分triggerDelay替换为triggerTime
10. 新增triggerCircle变量，搭配triggerRelativeHV/TV1/TV2使用，表示该动作为进圈还是出圈，本次修改主要涉及cutin和cutout的case