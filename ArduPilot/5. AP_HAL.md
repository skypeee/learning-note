



UART_test 以及 AP_HAL/examples 目录下的所有示例，在 ArduPilot 整个项目中的用途是：HAL 接口的最小测试和文档。

./waf --targets examples/UART_test

如果不加 --targets examples/UART_test，Waf 默认会尝试编译所有的飞控固件（Copter, Plane, Rover 等），那会花费很长时间。所以，--targets 是我们做 HAL 学习和开发时，快速验证某个功能模块的必备指令。

每当 ArduPilot 想要移植到一个新的飞控板（比如 F4/F7/H7 系列）时，这些例子就是第一个测试套件。如果 UART_test 运行不起来，说明最基本的串口驱动和 HAL 初始化就有问题，移植工作就无法进行。

在 libraries/AP_HAL_SITL/SITL_Main.cpp (或者类似的入口文件) 中，SITL 后端定义了真正的系统级 main() 函数：

C++

// 简化的示意代码
int main(int argc, char *argv[]) {
    // 1. 初始化操作系统相关的资源
    // 2. 调用那个宏生成的 AP_MAIN
    AP_MAIN(argc, argv); 
}
总结： hal.run 在 AP_HAL_SITL 中被具体实现。它会拿着你的 callbacks（里面装着你的 setup 和 loop），先执行一次 setup，然后在一个死循环里不断调用 loop，同时处理串口输入、网络数据等后台任务。

