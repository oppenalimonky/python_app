import subprocess
import sys
import os

def main():
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_file = os.path.join(current_dir, "main.py")
    
    # 启动Streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_file])

if __name__ == "__main__":
    main()