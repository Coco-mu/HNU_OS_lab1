# 作业2：UniProton build.py 构建系统分析

下面的分析以 openEuler/UniProton 的 `master` 分支 `build.py` 为例（官网给出的 `python build.py m4` 是课程所用版本的示例；不同版本的参数接口可能变化）。报告时应按老师要求使用指定分支，并核对平台名称。

## 调用链与代码位置

1. **读取命令行参数**：`build.py:252-260` 检查参数并填入默认值，将第一个位置参数转成小写 CPU 类型。
2. **展开平台配置**：`build.py:265-267` 根据 `globle.cpus_[cur_cpu_type]` 遍历该 CPU 类别下的平台，为每个平台创建 `Compile` 对象并调用 `UniProtonCompile()`。
3. **准备平台/工具链环境**：`Compile.get_config()`（约第25行）通过 `get_cpu_info()` 从 CPU 和平台配置中取得库类型、平台类型、交叉编译器目录、Kconfig 目录等；`SetCMakeEnviron()`（第44行起）写入 CMake 所需环境变量并把工具链目录加入 PATH。
4. **生成配置头文件**：`MakeBuildef()`（第240行起）调用 `make_buildef(..., "CREATE")` 生成配置头文件。
5. **创建独立构建目录**：`CMake()`（第126-145行）把构建目录设为 `output/tmp/<kconf_dir>`，创建目录并清理旧生成目录。
6. **生成 Makefile**：`CMake()`（第146-161行）根据构建选项拼接 CMake 命令，指定 `uniproton_tool_chain.cmake`、安装目录等参数，再由 `BuilderNolog.run()` 在构建目录中执行。
7. **编译与安装**：`make()`（第188-202行）执行 `make clean`、`make all`，成功后对 normal/coverity/single 模式执行 `make install`。
8. **整体控制**：`UniProtonCompile()`（第223-238行）按单平台或 ALL 逐个平台完成环境准备、生成配置、CMake 和 Make。

## 建议报告表述

`build.py` 是构建总入口。它先将 CPU/平台参数映射到工具链和 Kconfig 配置，再为每个平台建立独立的 `output/tmp/<kconf>` 构建目录；随后生成配置头文件、调用 CMake 生成 Makefile，最后运行 make 编译并安装产物。日志位于相应 `logs/<cpu_type>/` 下。课程网页的 `python build.py m4` 属于课程材料对应版本的调用示例；本次查看的上游 master 接受多个位置参数且首先按 `globle.cpus_` 查询目标，所以应以实际使用的仓库版本为准，不能直接把 `m4` 当作所有版本都支持的平台名。

## 本机复查命令

> 本机目前**没有** UniProton 源码，需要先自己 clone 一份（仓库地址见实验官网原文）。
> 下面第一行的路径换成你 clone 下来的位置，整块复制即可执行。

```sh
cd ~/uniproton
sed -n '1,280p' build.py
rg -n "def get_config|def CMake|def make\(|def UniProtonCompile|default_para|globle.cpus_|make all|make install" build.py
```

没装 `rg` 的话，最后一行可以换成 `grep -nE`：

```sh
cd ~/uniproton
grep -nE "def get_config|def CMake|def make\(|def UniProtonCompile|default_para|globle.cpus_|make all|make install" build.py
```

想确认这个版本的 `build.py` 到底接受哪些平台名（官网写的 `m4` 未必支持）：

```sh
cd ~/uniproton
python3 build.py -h
```

