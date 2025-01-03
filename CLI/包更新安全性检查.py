import json
from packaging.specifiers import SpecifierSet
from packaging.version import Version, InvalidVersion

# JSON数据
with open("dependencies.json", "r", encoding='utf-8') as f:
    data = json.load(f)

# 用户输入
package_name = input("请输入要升级的包名: ")
target_version = input("请输入目标版本: ")

found_package = False  # 标志变量，表示是否找到指定包
problems = []

for pkg in data:
    for dep in pkg["dependencies"]:
        if dep["package_name"] == package_name:
            found_package = True  # 找到指定包
            required_version = dep["required_version"]
            if required_version == "Any":
                continue  # 没有版本要求
            try:
                specifier = SpecifierSet(required_version)
                if not specifier.contains(target_version):
                    problems.append(f"{pkg['package']['package_name']} 需要 {required_version}")
            except InvalidVersion:
                problems.append(f"无法解析版本要求 {required_version} for {pkg['package']['package_name']}")

# 检查是否找到指定包
if not found_package:
    print(f"错误：未找到包 '{package_name}' 的依赖信息。")
elif problems:
    print("升级可能带来以下问题:")
    for problem in problems:
        print(f"- {problem}")
else:
    print("升级应该是安全的，没有发现版本冲突。")