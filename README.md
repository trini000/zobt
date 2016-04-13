# zl.py

使用方法:
----

1. 下载Python 2.7: https://www.python.org/downloads/ （选择Download Python 2.7.xx)
1. 下载zl.py脚本（右键点击->另存为）
1. 在Windows上, 打开命令行(搜索`cmd`->运行)，然后运行

        C:\python27\python.exe C:\PATH_TO_SCRIPT\zl.py -n NUM_OF_BASKETS -s STEP -o C:\OUTPUT_FILE_NAME
        
以上命令中，替换：
* `PATH_TO_SCRIPT`为（第2步下载时的）脚本路径
* `NUM_OF_BASKETS`为将结果平均分到几列
* `STEP`为结果的最小步数。步数需要可以被1整除（例：0.1, 0.2, 0.25可以，0.37, 0.86不行）。建议不要选择太小，否则输出文件会很大。
* `OUTPUT_FILE_NAME`为输出文件名，文件会存为.csv格式.

使用Excel打开输出文件，编辑、排序后另存为xlsx格式。

运行zl.py参数不对，或不提供参数时，会打印出帮助命令。

建议先使用小数据集试用。如`C:\python27\python.exe C:\PATH_TO_SCRIPT\zl.py -n 3 -s 0.1 -o test`。结果会存在当前文件夹下，名为`test.csv`。
