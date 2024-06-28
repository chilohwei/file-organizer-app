import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import shutil
import threading

class FileOrganizerApp:
    def __init__(self, master):
        self.master = master
        master.title("文件整理器")
        master.geometry("830x570")  # 默认尺寸
        master.minsize(830, 570)  # 最小尺寸，确保内容不被遮挡

        self.move_history = []  # 记录文件移动操作的历史
        self.created_folders = set()  # 记录创建的文件夹

        self.create_widgets()

    def create_widgets(self):
        # 顶部Logo和标题
        self.logo_text = tk.Label(self.master, text="📁", font=("Arial", 40))
        self.logo_text.pack(pady=10)
        tk.Label(self.master, text="文件整理器", font=("Arial", 18, "bold")).pack()

        # 选择文件夹按钮
        self.folder_frame = tk.Frame(self.master)
        self.folder_frame.pack(pady=20, padx=20, fill=tk.X)

        self.folder_path = tk.StringVar()
        self.folder_entry = tk.Entry(self.folder_frame, textvariable=self.folder_path, state='readonly', width=30)
        self.folder_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.folder_btn = ttk.Button(self.folder_frame, text="选择文件夹", command=self.select_folder)
        self.folder_btn.pack(side=tk.RIGHT)

        # 文件类型过滤选项
        self.filter_frame = tk.LabelFrame(self.master, text="文件类型过滤", padx=10, pady=10)
        self.filter_frame.pack(padx=20, pady=10, fill=tk.X)

        self.file_types = ["文档", "图片", "音频", "视频", "压缩文件", "其他"]
        self.file_type_vars = []

        for file_type in self.file_types:
            var = tk.BooleanVar(value=True)
            self.file_type_vars.append(var)
            ttk.Checkbutton(self.filter_frame, text=file_type, variable=var).pack(anchor=tk.W)

        # 开始整理按钮
        self.organize_btn = ttk.Button(self.master, text="开始整理", command=self.start_organize)
        self.organize_btn.pack(pady=20)

        # 撤销按钮
        self.undo_btn = ttk.Button(self.master, text="撤销", command=self.start_undo)
        self.undo_btn.pack(pady=5)

        # 进度条
        self.progress = ttk.Progressbar(self.master, length=300, mode='determinate')
        self.progress.pack(pady=10)

        # 状态标签
        self.status_label = tk.Label(self.master, text="", font=("Arial", 12), fg="blue")
        self.status_label.pack(pady=5)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def start_organize(self):
        folder = self.folder_path.get()
        if not folder:
            self.status_label.config(text="错误: 请先选择一个文件夹", fg="red")
            return

        self.organize_btn.config(state=tk.DISABLED)
        self.undo_btn.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.status_label.config(text="正在整理文件...", fg="blue")

        # 在新线程中运行文件整理，以避免UI卡顿
        threading.Thread(target=self.organize_files, args=(folder,), daemon=True).start()

    def organize_files(self, folder):
        try:
            file_types = {
                "文档": [".txt", ".doc", ".docx", ".pdf"],
                "图片": [".jpg", ".jpeg", ".png", ".gif"],
                "音频": [".mp3", ".wav", ".ogg"],
                "视频": [".mp4", ".avi", ".mov"],
                "压缩文件": [".zip", ".rar", ".7z"]
            }

            self.move_history.clear()  # 清空历史记录
            self.created_folders.clear()  # 清空创建的文件夹记录

            all_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            total_files = len(all_files)

            for i, file in enumerate(all_files):
                file_path = os.path.join(folder, file)
                file_ext = os.path.splitext(file)[1].lower()

                dest_folder = "其他"
                for type_name, extensions in file_types.items():
                    if file_ext in extensions:
                        dest_folder = type_name
                        break

                if self.file_type_vars[self.file_types.index(dest_folder)].get():
                    dest_path = os.path.join(folder, dest_folder)
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                        self.created_folders.add(dest_path)  # 记录创建的文件夹
                    new_path = os.path.join(dest_path, file)
                    shutil.move(file_path, new_path)
                    self.move_history.append((new_path, file_path))  # 记录移动操作

                self.progress['value'] = (i + 1) / total_files * 100
                self.status_label.config(text=f"正在处理: {file}", fg="blue")
                self.master.update_idletasks()

            self.status_label.config(text="文件整理完成！", fg="green")
        except Exception as e:
            self.status_label.config(text=f"整理过程中出现错误: {str(e)}", fg="red")
        finally:
            self.organize_btn.config(state=tk.NORMAL)
            self.undo_btn.config(state=tk.NORMAL)

    def start_undo(self):
        if not self.move_history and not self.created_folders:
            self.status_label.config(text="没有可撤销的操作", fg="blue")
            return

        self.organize_btn.config(state=tk.DISABLED)
        self.undo_btn.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.status_label.config(text="正在撤销操作...", fg="blue")

        # 在新线程中运行撤销操作，以避免UI卡顿
        threading.Thread(target=self.undo_all_actions, daemon=True).start()

    def undo_all_actions(self):
        try:
            total_moves = len(self.move_history)
            total_folders = len(self.created_folders)
            total_operations = total_moves + total_folders

            # 撤销所有文件移动操作
            for i, (src, dest) in enumerate(reversed(self.move_history)):
                shutil.move(src, dest)
                self.progress['value'] = (i + 1) / total_operations * 100
                self.status_label.config(text=f"正在撤销: {os.path.basename(src)}", fg="blue")
                self.master.update_idletasks()

            self.move_history.clear()

            # 删除创建的文件夹
            for i, folder in enumerate(sorted(self.created_folders, reverse=True), start=total_moves):
                if os.path.isdir(folder):
                    os.rmdir(folder)
                self.progress['value'] = (i + 1) / total_operations * 100
                self.status_label.config(text=f"正在删除文件夹: {os.path.basename(folder)}", fg="blue")
                self.master.update_idletasks()

            self.created_folders.clear()
            self.status_label.config(text="所有操作已撤销", fg="green")
        except Exception as e:
            self.status_label.config(text=f"撤销操作时发生错误: {str(e)}", fg="red")
        finally:
            self.organize_btn.config(state=tk.NORMAL)
            self.undo_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = FileOrganizerApp(root)
        root.mainloop()
    except Exception as e:
        import traceback
        with open("error_log.txt", "w") as f:
            f.write(f"An error occurred: {str(e)}")
            f.write(traceback.format_exc())