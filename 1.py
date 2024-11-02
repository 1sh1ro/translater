import keyboard
import pyperclip
import win32gui
import win32con
import tkinter as tk
from tkinter import ttk
from deep_translator import GoogleTranslator
import threading

def get_selected_text():
    # 模拟Ctrl+C复制选中文本
    keyboard.send('ctrl+c')
    # 获取剪贴板内容
    return pyperclip.paste()

def translate_text(text):
    # 使用 deep_translator 进行翻译，目标语言设置为中文
    translator = GoogleTranslator(source='auto', target='zh-CN')
    translated = translator.translate(text)
    return translated

class TranslateWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("翻译助手")  # 设置窗口标题
        self.root.overrideredirect(True)  # 无边框
        self.root.attributes('-topmost', True)  # 窗口置顶
        self.initial_position_set = False  # 添加标志
        self.fixed_position = None  # 添加固定位置属性
        
        # 设置窗口样式
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#f0f0f0')  # 更改背景颜色
        style.configure('Custom.TButton', font=('Arial', 12), padding=5)  # 更改按钮样式
        
        self.frame = ttk.Frame(self.root, style='Custom.TFrame', padding=10)
        self.frame.pack(fill='both', expand=True)
        
        
        # 关闭钮
        self.close_btn = ttk.Button(self.frame, text='×', width=2, command=self.root.destroy, style='Custom.TButton')
        self.close_btn.pack(anchor='ne')
        
        # 翻译文本显示
        self.text = tk.Text(self.frame, wrap='word', height=5, width=40, font=('Arial', 12), bg='#ffffff', fg='#333333', bd=1, relief='solid')
        self.text.pack(pady=5)
        
        # 绑定鼠标事件实现窗口拖动
        self.frame.bind('<Button-1>', self.start_move)
        self.frame.bind('<B1-Motion>', self.on_move)
        
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        
    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    def show_translation(self, text):
        self.text.config(state=tk.NORMAL)  # 允许编辑
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, text)
        
        # 计算文本高度并调整窗口大小
        line_count = self.text.count('1.0', 'end', 'displaylines')[0]  # 获取行数
        text_height = self.text.winfo_height() + line_count * 20  # 估算每行高度
        t_height=text_height+10
        # 设置文本框的高度
        if line_count <=3:   
            # height=line_count*10
            self.text.config(height=line_count)  # 根据行数设置文本框高度
        else:
            self.text.config(height=line_count)  # 根据行数设置文本框高度
        
        self.root.geometry(f"400x{max(150, t_height)}")  # 设置宽度为400，高度根据文本调整，最小为100
        
        if not self.initial_position_set:
            # 仅在首次显示时设置窗口位置在鼠标附近
            x = self.root.winfo_pointerx()
            y = self.root.winfo_pointery()
            self.fixed_position = (x + 10, y + 10)
            self.root.geometry(f"+{self.fixed_position[0]}+{self.fixed_position[1]}")
            self.initial_position_set = True

        self.text.config(state=tk.DISABLED)  # 禁止编辑
        self.root.deiconify()
        self.text.update_idletasks()  # 更新布局

def main():
    translate_window = TranslateWindow()
    
    def check_selection():
        text = get_selected_text()
        if text:
            # 使用线程来处理翻译任务
            threading.Thread(target=translate_and_show, args=(text,)).start()
        # 增加延迟时间，例如每 2000 毫秒（2 秒）检查一次
        translate_window.root.after(2000, check_selection)  # 减少延迟以提高响应速度
    
    def translate_and_show(text):
        translated = translate_text(text)
        if translated:
            translate_window.show_translation(translated)
    
    check_selection()
    translate_window.root.withdraw()  # 初始隐藏窗口
    translate_window.root.mainloop()

if __name__ == '__main__':
    main()
