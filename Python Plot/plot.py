import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re
from collections import deque
import time

class BPMPlotter:
    def __init__(self, com_port='COM5', baud_rate=115200):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.ser = None
        self.setup_serial()
        self.setup_plot()
        
    def setup_serial(self):
        """Kết nối serial đến STM32"""
        try:
            self.ser = serial.Serial(self.com_port, self.baud_rate, timeout=1)
            print(f"Đã kết nối đến {self.com_port}")
            # Xóa buffer serial
            self.ser.reset_input_buffer()
            time.sleep(2)
        except Exception as e:
            print(f"Lỗi kết nối đến {self.com_port}: {e}")
            exit()
    
    def setup_plot(self):
        """Thiết lập đồ thị"""
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.max_points = 120  # 120 giây dữ liệu
        self.times = deque(maxlen=self.max_points)
        self.bpm_values = deque(maxlen=self.max_points)
        
        # Cấu hình đồ thị
        self.ax.set_title('HEART RATE MONITOR - Real Time BPM', fontsize=16, fontweight='bold')
        self.ax.set_xlabel('Time (seconds)', fontsize=12)
        self.ax.set_ylabel('BPM', fontsize=12)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_ylim(40, 180)  # Phạm vi BPM bình thường
        
        # Vẽ đường BPM
        self.bpm_line, = self.ax.plot([], [], 'r-', linewidth=2, label='Heart Rate')
        
        # Hiển thị BPM hiện tại
        self.current_bpm_text = self.ax.text(0.02, 0.95, 'BPM: --', transform=self.ax.transAxes,
                                           fontsize=20, fontweight='bold', color='red',
                                           bbox=dict(facecolor='white', alpha=0.8))
        
        self.ax.legend(loc='upper right')
        plt.tight_layout()
    
    def parse_bpm(self, line):
        """Phân tích dữ liệu BPM từ STM32"""
        try:
            # Tìm pattern: "Heart rate: 72 bpm"
            match = re.search(r'Heart rate:\s*(\d+)\s*bpm', line)
            if match:
                return int(match.group(1))
        except (ValueError, AttributeError):
            pass
        return None
    
    def update_plot(self, frame):
        """Cập nhật đồ thị"""
        try:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                # print(f"Received: {line}")  # Debug
                
                bpm = self.parse_bpm(line)
                if bpm is not None and 40 <= bpm <= 180:
                    current_time = time.time()
                    
                    # Thêm dữ liệu mới
                    if not self.times:
                        self.start_time = current_time
                    
                    elapsed_time = current_time - self.start_time
                    self.times.append(elapsed_time)
                    self.bpm_values.append(bpm)
                    
                    # Cập nhật đồ thị
                    self.bpm_line.set_data(self.times, self.bpm_values)
                    
                    # Cập nhật text BPM hiện tại
                    self.current_bpm_text.set_text(f'BPM: {bpm}')
                    
                    # Tự động điều chỉnh trục X
                    if elapsed_time > 30:
                        self.ax.set_xlim(elapsed_time - 30, elapsed_time + 5)
                    else:
                        self.ax.set_xlim(0, 35)
                    
                    # Tự động điều chỉnh trục Y với biên độ nhỏ
                    if self.bpm_values:
                        current_bpm = self.bpm_values[-1]
                        y_min = max(40, current_bpm - 20)
                        y_max = min(180, current_bpm + 20)
                        self.ax.set_ylim(y_min, y_max)
        
        except Exception as e:
            print(f"Lỗi khi đọc dữ liệu: {e}")
        
        return self.bpm_line, self.current_bpm_text
    
    def run(self):
        """Chạy chương trình"""
        print("Đang đọc dữ liệu BPM từ STM32...")
        print("Nhấn Ctrl+C để dừng")
        print("Chờ dữ liệu...")
        
        try:
            # Animation
            ani = animation.FuncAnimation(self.fig, self.update_plot,
                                        interval=100, blit=True,
                                        cache_frame_data=False)
            plt.show()
            
        except KeyboardInterrupt:
            print("\nĐang dừng chương trình...")
        finally:
            if self.ser and self.ser.is_open:
                self.ser.close()
            print("Đã đóng kết nối serial")

# Code chính
if __name__ == "__main__":
    # Tự động tìm COM port nếu COM5 không hoạt động
    com_port = 'COM5'
    
    plotter = BPMPlotter(com_port=com_port)
    plotter.run()