import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Функция для генерации гармонического сигнала
def generate_harmonic_signal(frequency, amplitude, phase, time):
    return amplitude * np.sin(2 * np.pi * frequency * time + phase)

# Функция для добавления случайного шума
def add_noise(signal, noise_level):
    noise = np.random.normal(0, noise_level, signal.shape)
    return signal + noise

# Функция для вычисления числовых характеристик сигнала
def calculate_characteristics(signal):
    mean = np.mean(signal)  # Среднее значение
    variance = np.var(signal)  # Дисперсия
    return mean, variance

# Класс для создания графиков
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)

    def plot(self, time, harmonic_signal, noisy_signal):
        self.ax.clear()
        self.ax.plot(time, harmonic_signal, label="Гармонический сигнал", color="blue")
        self.ax.plot(time, noisy_signal, label="Случайный сигнал", color="red")
        self.ax.set_title("Гармонический и случайный сигналы")
        self.ax.set_xlabel("Время (с)")
        self.ax.set_ylabel("Амплитуда")
        self.ax.legend()
        self.draw()

# Основное окно приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Моделирование сигналов")
        self.setGeometry(100, 100, 800, 600)

        # Создание виджетов
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Поля для ввода параметров
        self.label_frequency = QLabel("Частота (Гц):")
        self.layout.addWidget(self.label_frequency)
        self.entry_frequency = QLineEdit()
        self.layout.addWidget(self.entry_frequency)

        self.label_amplitude = QLabel("Амплитуда:")
        self.layout.addWidget(self.label_amplitude)
        self.entry_amplitude = QLineEdit()
        self.layout.addWidget(self.entry_amplitude)

        self.label_phase = QLabel("Фаза (рад):")
        self.layout.addWidget(self.label_phase)
        self.entry_phase = QLineEdit()
        self.layout.addWidget(self.entry_phase)

        self.label_noise = QLabel("Уровень шума:")
        self.layout.addWidget(self.label_noise)
        self.entry_noise = QLineEdit()
        self.layout.addWidget(self.entry_noise)

        self.label_time = QLabel("Длительность (с):")
        self.layout.addWidget(self.label_time)
        self.entry_time = QLineEdit()
        self.layout.addWidget(self.entry_time)

        self.label_sampling = QLabel("Частота дискретизации (Гц):")
        self.layout.addWidget(self.label_sampling)
        self.entry_sampling = QLineEdit()
        self.layout.addWidget(self.entry_sampling)

        # Кнопка для запуска расчетов
        self.button = QPushButton("Рассчитать и построить графики")
        self.button.clicked.connect(self.process_input)
        self.layout.addWidget(self.button)

        # Холст для отображения графиков
        self.canvas = PlotCanvas(self, width=6, height=4)
        self.layout.addWidget(self.canvas)

    # Функция для обработки ввода и отображения результатов
    def process_input(self):
        try:
            frequency = float(self.entry_frequency.text())
            amplitude = float(self.entry_amplitude.text())
            phase = float(self.entry_phase.text())
            noise_level = float(self.entry_noise.text())
            time_duration = float(self.entry_time.text())
            sampling_rate = float(self.entry_sampling.text())

            time = np.arange(0, time_duration, 1 / sampling_rate)
            harmonic_signal = generate_harmonic_signal(frequency, amplitude, phase, time)
            noisy_signal = add_noise(harmonic_signal, noise_level)

            mean_harmonic, var_harmonic = calculate_characteristics(harmonic_signal)
            mean_noisy, var_noisy = calculate_characteristics(noisy_signal)

            result_text = (
                f"Характеристики гармонического сигнала:\n"
                f"Среднее: {mean_harmonic:.4f}, Дисперсия: {var_harmonic:.4f}\n\n"
                f"Характеристики случайного сигнала:\n"
                f"Среднее: {mean_noisy:.4f}, Дисперсия: {var_noisy:.4f}"
            )
            QMessageBox.information(self, "Результаты", result_text)

            self.canvas.plot(time, harmonic_signal, noisy_signal)

        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, введите корректные числовые значения.")

# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
