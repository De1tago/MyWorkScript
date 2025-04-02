import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def comma_converter(value: str) -> float:
    return float(value.replace(',', '.'))

# Загрузка и обработка данных
data = []
with open('data.txt', 'r') as file:
    for line in file:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            freq = int(parts[0])
            amp = comma_converter(parts[1])
            data.append([freq, amp])

data = np.array(data)
all_frequencies = data[:, 0]
all_amplitudes = data[:, 1]

# Запрос диапазона анализа
print("\nВыберите диапазон анализа:")
f_min = 0.51e10
f_max = 0.56e10

# Фильтрация данных
mask = (all_frequencies >= f_min) & (all_frequencies <= f_max)
frequencies = all_frequencies[mask]
amplitudes = all_amplitudes[mask]

if len(frequencies) == 0:
    print("Ошибка: нет данных в выбранном диапазоне!")
    exit()

# Параметры поиска пиков (теперь ищем максимумы!)
peak_params = {'height': -70, 'distance': 3, 'prominence': 1.0}
peaks, properties = find_peaks(amplitudes, **peak_params)  # Убрали минус перед amplitudes!
prominences = properties['prominences']

def find_left_crossing(freq, amp, peak_idx, cutoff):
    for i in range(peak_idx - 1, -1, -1):
        if amp[i] <= cutoff:  # Теперь ищем пересечение вниз (для пиков)
            x1, y1 = freq[i], amp[i]
            x2, y2 = freq[i+1], amp[i+1]
            if y1 == y2:
                return x1
            x = x1 + (cutoff - y1) * (x2 - x1) / (y2 - y1)
            return x
    return None

def find_right_crossing(freq, amp, peak_idx, cutoff):
    for i in range(peak_idx + 1, len(amp)):
        if amp[i] <= cutoff:  # Теперь ищем пересечение вниз (для пиков)
            x1, y1 = freq[i-1], amp[i-1]
            x2, y2 = freq[i], amp[i]
            if y1 == y2:
                return x1
            x = x1 + (cutoff - y1) * (x2 - x1) / (y2 - y1)
            return x
    return None

# Расчет добротности
q_values = []
delta_fs = []
cutoffs = []
for idx in peaks:
    f0 = frequencies[idx]
    amp_val = amplitudes[idx]
    cutoff = amp_val - 15.0  # Уровень -3 dB для пиков (а не провалов)
    cutoffs.append(cutoff)
    
    f_left = find_left_crossing(frequencies, amplitudes, idx, cutoff)
    f_right = find_right_crossing(frequencies, amplitudes, idx, cutoff)
    
    if f_left and f_right:
        delta_f = f_right - f_left
        q = f0 / delta_f
    else:
        delta_f = q = None
    delta_fs.append(delta_f)
    q_values.append(q)

# Вывод информации о пиках
print("\nИнформация о пиках:")
print(f"{'Частота (Гц)':<15} {'Амплитуда (dB)':<15} {'Ширина (Гц)':<15} {'Добротность':<15} {'Высота (dB)':<15}")
for i, idx in enumerate(peaks):
    f0 = frequencies[idx]
    amp = amplitudes[idx]
    delta_f = delta_fs[i]
    q = q_values[i]
    prom = prominences[i]
    if delta_f and q:
        print(f"{f0:<15} {amp:<15.2f} {delta_f:<15.2f} {q:<15.2f} {prom:<15.2f}")
    else:
        print(f"{f0:<15} {amp:<15.2f} {'N/A':<15} {'N/A':<15} {prom:<15.2f}")

# Отрисовка графика
plt.figure(figsize=(14, 7))
plt.plot(all_frequencies, all_amplitudes, 'grey', alpha=0.3, label='Вся АЧХ')
plt.plot(frequencies, amplitudes, 'b', label='Выбранный диапазон')

if len(peaks) > 0:
    peak_freqs = frequencies[peaks]
    peak_amps = amplitudes[peaks]
    plt.plot(peak_freqs, peak_amps, 'xr', markersize=10, label='Пики')
    
    # Добавление линий уровня -3 dB и ширины пиков
    for i, idx in enumerate(peaks):
        f0 = peak_freqs[i]
        amp = peak_amps[i]
        cutoff = cutoffs[i]
        delta_f = delta_fs[i]
        if delta_f:
            f_left = peak_freqs[i] - delta_f / 2
            f_right = peak_freqs[i] + delta_f / 2
            plt.hlines(cutoff, f_left, f_right, colors='green', linestyles='dashed', linewidth=1)
            plt.vlines([f_left, f_right], cutoff, amp, colors='green', linestyles='dashed', linewidth=1)
            plt.text(f0, amp, f'Q={q_values[i]:.2f}', fontsize=8, ha='left')

plt.axvspan(f_min, f_max, color='yellow', alpha=0.2, label='Зона анализа')
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда, dB')
plt.title(f'Анализ АЧХ в диапазоне {f_min/1e6:.2f}-{f_max/1e6:.2f} МГц')
plt.legend()
plt.grid(True)
plt.show()