
### data architecture
├── data
│   ├── hefei_data_list_20190904.txt
│   ├── heifei_round1_ansA_20191008.txt
│   ├── hf_round1_arrythmia.txt
│   ├── hf_round1_label.txt
│   ├── hf_round1_subA.txt
│   ├── hf_round1_subB_noDup_rename.txt
│   ├── hf_round1_testA
│   ├── hf_round1_testB_noDup_rename
│   └── hf_round1_train

### 依赖
Ubuntu 18.04 LTS
CUDA 10.0, CUDNN 7
Anconda3
其它python 库： tensorflow 2.0.0， plotly
具体安装过程可以参考 code/install.sh


### 运行方法
进入code, 执行 bash main.sh


### 解决方案及算法介绍

我们只使用了单个模型，最后使用了最后的66checkpoints ensemble才预测最后的结果。
我们队伍的最佳结果是0.8309，因为之前是手动调参训练忘记了。本次代码复现出来的是0.8305，
时间不够，如果训练更长时间，或许会更好。

- 基础模型
	模型我们是基于 https://stanfordmlgroup.github.io/projects/ecg2/ 图中的模型来开发的，
	我们只参考了这个网络结构图片，没有找到源代码。
- 改进之处： 
	1、我们使用stride=2来降采样而不是maxpooling。 
	2、 我们采用两个这样的网络结构，最后concatenate一起，来希望能抓取不同尺度的信息。
	3、因为类别不均匀，我们在最后一层，以log(pos/neg)对bias进行了初始化。
	4、以1/log(某类样本数) 做为class_weights，label_smoothing=0.1 的binary cross entropy
	做为loss函数。
	

### 联系方式
如有意外，请联系 郭兰停 13136165880 谢谢。
