import subprocess
import sys

def uninstall_packages(file_path):
    try:
        with open(file_path, 'r') as file:
            packages = file.readlines()

        # 移除每个包字符串末尾的换行符
        packages = [pkg.strip() for pkg in packages]

        for package in packages:
            subprocess.run([sys.executable, '-m', 'pip', 'uninstall', package, '-y'], check=True)
            print(f"已卸载 {package}")

    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到。")
    except subprocess.CalledProcessError as e:
        print(f"卸载 {package} 时发生错误：{e}")
    except Exception as e:
        print(f"发生未知错误：{e}")

if __name__ == "__main__":
    requirements_file = 'requirements-noversion.txt'
    uninstall_packages(requirements_file)
