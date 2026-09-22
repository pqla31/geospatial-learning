"""
环境自检脚本 —— 确认 conda 环境、Python 版本、常用包是否就绪。
跑法：conda activate geo && python week01-basics/00_env_check.py
"""
import platform
import sys

def check(name):
    try:
        mod = __import__(name)
        version = getattr(mod, "__version__", "已安装")
        return f"  [OK]   {name:<12} {version}"
    except ImportError:
        return f"  [未装] {name:<12} （用到时再装，现在不影响）"

print("=" * 50)
print("Python 版本:", sys.version.split()[0])
print("解释器路径:", sys.executable)
print("系统:", platform.platform())
print("=" * 50)
print("常用包状态：")
for pkg in ["numpy", "pandas", "matplotlib", "geopandas", "rasterio", "shapely"]:
    print(check(pkg))
print("=" * 50)
print("能打印出这行，说明环境跑通了。")
