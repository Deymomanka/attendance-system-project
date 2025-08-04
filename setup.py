import os

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"作成: {path}")
    else:
        print(f"既に存在: {path}")

def create_file(path, content=""):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"作成: {path}")
    else:
        print(f"既に存在: {path}")

def main():
    # フォルダー作成
    create_folder("images")
    create_folder("logs")
    create_folder("credentials")

    # 空のDBファイル（SQLite用）を作成
    create_file("logs/attendance.db")

    # requirements.txt
    requirements_content = """opencv-python
face_recognition
numpy
gspread
oauth2client
"""
    create_file("requirements.txt", requirements_content)

    # .gitignore
    gitignore_content = """__pycache__/
*.pyc
*.pyo
*.pyd
env/
.venv/
venv/
.idea/
.vscode/
logs/*.db
credentials/*.json
"""
    create_file(".gitignore", gitignore_content)

    # 空のutils.py
    create_file("utils.py", "# ここにDBやGoogle Sheetsの関数を書きます\n")

    # 空のmain.py
    create_file("main.py", "# ここにメインスクリプトを書きます\n")

if __name__ == "__main__":
    main()
