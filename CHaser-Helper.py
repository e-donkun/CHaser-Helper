import tkinter as tk
from tkinter import OptionMenu, StringVar, messagebox
import subprocess
import os
import glob
import random
import shutil

# マップファイルとClientファイルの取得
map_files = [f for f in os.listdir('./Server/Maps') if f.endswith('.map')]
client_files = [os.path.basename(f) for f in glob.glob('./Client/*.py') if os.path.basename(f) != 'CHaser.py']

# Client実行関数
def run_client(mode, filename):
    if filename:
        name_without_ext = os.path.splitext(filename)[0]
        arg1 = "2009" if mode == "COOL" else "2010"
        subprocess.Popen([
            "python", f"./Client/{filename}", arg1, name_without_ext, "127.0.0.1"
        ], shell=True)

# Server起動関数
def run_server():
    selected_map = map_var.get()
    if selected_map:
        subprocess.Popen([
            "AsahikawaProcon-Server.exe", f"Maps/{selected_map}"
        ], cwd="./Server", shell=True)

# BGM変更関数（init_server.py と同階層にある BGM/ からランダム選択し、Server/Music/bgm.mp3 として上書き）
def change_bgm():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bgm_dir = os.path.join(base_dir, 'BGM')
    dest_dir = os.path.join(base_dir, 'Server', 'Music')
    os.makedirs(dest_dir, exist_ok=True)

    mp3_files = glob.glob(os.path.join(bgm_dir, '*.mp3'))
    if not mp3_files:
        messagebox.showerror("BGM変更", "BGM フォルダに *.mp3 ファイルが見つかりません。\nBGM フォルダを確認してください。")
        return

    chosen = random.choice(mp3_files)
    dest_path = os.path.join(dest_dir, 'bgm.mp3')

    try:
        shutil.copy2(chosen, dest_path)  # 既存があれば上書き
        #messagebox.showinfo("BGM変更", f"選択された BGM: {os.path.basename(chosen)}\n'bgm.mp3' を更新しました。")
    except Exception as e:
        messagebox.showerror("BGM変更", f"コピーに失敗しました:\n{e}")

# COOLとHOTの入れ替え
def swap_clients():
    cool = cool_var.get()
    hot = hot_var.get()
    cool_var.set(hot)
    hot_var.set(cool)

# 最終ログ表示関数
def show_latest_log():
    log_dir = './Server/log'
    log_files = glob.glob(os.path.join(log_dir, '*.txt'))
    if not log_files:
        return

    latest_file = max(log_files, key=os.path.getmtime)

    with open(latest_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    last_lines = lines[-10:]

    log_window = tk.Toplevel()
    log_window.title("最終ログ表示")
    log_window.geometry("1000x500")

    text_frame = tk.Frame(log_window)
    text_frame.pack(expand=True, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Helvetica", 24), yscrollcommand=scrollbar.set)
    text_widget.pack(expand=True, fill=tk.BOTH)
    scrollbar.config(command=text_widget.yview)

    text_widget.insert(tk.END, f"{os.path.basename(latest_file)}\n\n")
    text_widget.insert(tk.END, ''.join(last_lines))
    text_widget.config(state=tk.DISABLED)

# GUI作成
root = tk.Tk()
root.title("U16プロコン大会Helper")
root.geometry("700x350")
font_large = ("Helvetica", 14)

# 上段：マップ選択とServer起動 + BGM変更ボタン
map_frame = tk.Frame(root)
map_frame.pack(pady=10)
map_var = StringVar(root)
map_var.set(map_files[0] if map_files else "")
tk.Label(map_frame, text="マップ選択：", font=font_large).pack(side=tk.LEFT, padx=5)
OptionMenu(map_frame, map_var, *map_files).pack(side=tk.LEFT, padx=5)
# Server起動ボタン
tk.Button(map_frame, text="Server起動", command=run_server, font=font_large, bg="#cce6ff", relief="raised", padx=10, pady=5).pack(side=tk.LEFT, padx=10)
# 追加: BGM変更ボタン（Server起動ボタンの横）
tk.Button(map_frame, text="BGM変更", command=change_bgm, font=font_large, bg="#ffe6cc", relief="raised", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

# 下段：COOL選択、入れ替え、HOT選択
client_frame = tk.Frame(root)
client_frame.pack(pady=10)
cool_var = StringVar(root)
cool_var.set(client_files[0] if client_files else "")
tk.Label(client_frame, text="COOL：", font=font_large).pack(side=tk.LEFT, padx=5)
OptionMenu(client_frame, cool_var, *client_files).pack(side=tk.LEFT, padx=5)
tk.Button(client_frame, text="入れ替え", command=swap_clients, font=font_large, relief="groove", padx=10, pady=5).pack(side=tk.LEFT, padx=10)
hot_var = StringVar(root)
hot_var.set(client_files[1] if len(client_files) > 1 else client_files[0] if client_files else "")
tk.Label(client_frame, text="HOT：", font=font_large).pack(side=tk.LEFT, padx=5)
OptionMenu(client_frame, hot_var, *client_files).pack(side=tk.LEFT, padx=5)

# 実行ボタン
exec_frame = tk.Frame(root)
exec_frame.pack(pady=10)
tk.Button(exec_frame, text="COOLとしてClient実行", command=lambda: run_client("COOL", cool_var.get()), font=font_large, bg="#ccffcc", relief="raised", padx=20, pady=10).pack(side=tk.LEFT, padx=50)
tk.Button(exec_frame, text="HOTとしてClient実行", command=lambda: run_client("HOT", hot_var.get()), font=font_large, bg="#ccffcc", relief="raised", padx=20, pady=10).pack(side=tk.LEFT, padx=50)

# 最終ログ表示ボタン
log_frame = tk.Frame(root)
log_frame.pack(pady=10)
tk.Button(log_frame, text="最終ログを表示", command=show_latest_log, font=font_large, bg="#f0f0f0", relief="raised", padx=10, pady=5).pack()

# GUI開始
root.mainloop()