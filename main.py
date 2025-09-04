import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图像处理工具")
        self.root.geometry("1920x1080")
        
        self.current_image = None
        self.processed_image = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(button_frame, text="选择图像", command=self.load_image).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="处理图像", command=self.process_image).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="保存结果", command=self.save_image).pack(side=tk.LEFT, padx=(0, 10))
        
        # 图像显示框架
        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 原图显示
        original_label = ttk.Label(image_frame, text="原始图像")
        original_label.grid(row=0, column=0, padx=(0, 10))
        
        self.original_canvas = tk.Canvas(image_frame, width=960, height=540, bg='white')
        self.original_canvas.grid(row=1, column=0, padx=(0, 10))
        
        # 处理后图像显示
        processed_label = ttk.Label(image_frame, text="处理后图像")
        processed_label.grid(row=0, column=1)
        
        self.processed_canvas = tk.Canvas(image_frame, width=960, height=540, bg='white')
        self.processed_canvas.grid(row=1, column=1)
        
        # 参数控制框架
        control_frame = ttk.LabelFrame(main_frame, text="处理参数", padding="10")
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 滑块控制
        ttk.Label(control_frame, text="亮度调节:").grid(row=0, column=0, sticky=tk.W)
        self.brightness_var = tk.DoubleVar(value=1.0)
        self.brightness_scale = ttk.Scale(control_frame, from_=0.5, to=2.0, 
                                        variable=self.brightness_var, orient=tk.HORIZONTAL)
        self.brightness_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        ttk.Label(control_frame, text="对比度调节:").grid(row=1, column=0, sticky=tk.W)
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.contrast_scale = ttk.Scale(control_frame, from_=0.5, to=3.0, 
                                      variable=self.contrast_var, orient=tk.HORIZONTAL)
        self.contrast_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # 结果显示
        result_frame = ttk.LabelFrame(main_frame, text="分析结果", padding="10")
        result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.result_text = tk.Text(result_frame, height=6, width=70)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # 配置权重
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        control_frame.columnconfigure(1, weight=1)
        result_frame.columnconfigure(0, weight=1)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="选择图像文件",
            filetypes=[
                ("图像文件", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                # 使用OpenCV读取图像
                self.current_image = cv2.imread(file_path)
                if self.current_image is None:
                    messagebox.showerror("错误", "无法读取图像文件")
                    return
                
                # 显示原始图像
                self.display_image(self.current_image, self.original_canvas)
                
                # 分析原始图像
                self.analyze_image(self.current_image)
                
            except Exception as e:
                messagebox.showerror("错误", f"加载图像失败: {str(e)}")
    
    def process_image(self):
        if self.current_image is None:
            messagebox.showwarning("警告", "请先选择图像")
            return
        
        try:
            # 获取参数
            brightness = self.brightness_var.get()
            contrast = self.contrast_var.get()
            
            # 图像处理
            processed = self.current_image.astype(np.float64)
            processed = processed * contrast + (brightness - 1) * 127
            processed = np.clip(processed, 0, 255).astype(np.uint8)
            
            # 应用其他处理（示例：高斯模糊）
            processed = cv2.GaussianBlur(processed, (5, 5), 0)
            
            self.processed_image = processed
            
            # 显示处理后图像
            self.display_image(self.processed_image, self.processed_canvas)
            
            # 分析处理后图像
            self.analyze_image(self.processed_image, prefix="处理后 - ")
            
        except Exception as e:
            messagebox.showerror("错误", f"图像处理失败: {str(e)}")
    
    def display_image(self, cv_image, canvas):
        # 转换颜色空间 (BGR -> RGB)
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        
        # 调整图像大小以适应画布
        height, width = rgb_image.shape[:2]
        canvas_width, canvas_height = 350, 250
        
        # 计算缩放比例
        scale = min(canvas_width/width, canvas_height/height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # 缩放图像
        resized_image = cv2.resize(rgb_image, (new_width, new_height))
        
        # 转换为PIL Image
        pil_image = Image.fromarray(resized_image)
        photo = ImageTk.PhotoImage(pil_image)
        
        # 显示在画布上
        canvas.delete("all")
        canvas.create_image(canvas_width//2, canvas_height//2, anchor=tk.CENTER, image=photo)
        
        # 保持引用，防止被垃圾回收
        canvas.image = photo
    
    def analyze_image(self, image, prefix=""):
        """分析图像并显示指标"""
        try:
            # 基本统计信息
            height, width, channels = image.shape
            mean_value = np.mean(image)
            std_value = np.std(image)
            
            # 颜色通道分析
            if channels == 3:
                b_mean, g_mean, r_mean = np.mean(image, axis=(0, 1))
                color_info = f"RGB均值: R={r_mean:.2f}, G={g_mean:.2f}, B={b_mean:.2f}"
            else:
                color_info = f"灰度均值: {mean_value:.2f}"
            
            # 直方图分析
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist_peak = np.argmax(hist.flatten())
            
            # 边缘检测
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if channels == 3 else image
            edges = cv2.Canny(gray, 50, 150)
            edge_pixels = np.sum(edges > 0)
            edge_density = edge_pixels / (width * height) * 100
            
            # 格式化结果
            result = f"""
                        {prefix}图像分析结果:
                        ================
                        尺寸: {width} × {height} 像素
                        通道数: {channels}
                        {color_info}
                        标准差: {std_value:.2f}
                        边缘密度: {edge_density:.2f}%
                        直方图峰值索引: {hist_peak}

                        统计指标:
                        - 最小值: {np.min(image):.2f}
                        - 最大值: {np.max(image):.2f}
                        - 中位数: {np.median(image):.2f}
                        """
            
            # 显示结果
            if prefix:
                self.result_text.insert(tk.END, result)
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, result)
            
            self.result_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("错误", f"图像分析失败: {str(e)}")
    
    def save_image(self):
        if self.processed_image is None:
            messagebox.showwarning("警告", "没有处理后的图像可保存")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存处理后的图像",
            defaultextension=".png",
            filetypes=[
                ("PNG文件", "*.png"),
                ("JPEG文件", "*.jpg"),
                ("BMP文件", "*.bmp"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                cv2.imwrite(file_path, self.processed_image)
                messagebox.showinfo("成功", f"图像已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")

def main():
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()