% Задаем параметры
fs = 30e9;  % Частота дискретизации (30 ГГц)
columns = {'m_z_xrange800', 'm_z_xrange900', 'm_z_xrange1000', ...
           'm_z_xrange1100', 'm_z_xrange1200'};  % Список нужных столбцов

% Получаем количество строк в данных
n_points = height(table1);

% Вычисляем частотный вектор один раз
[~, f] = periodogram(table1.(columns{1}), [], n_points, fs, 'power');

% Подготавливаем массив для хранения результатов
all_power_data = [];

% Цикл по всем указанным столбцам
figure;
hold on;

for i = 1:length(columns)
    colName = columns{i};
    aa = table1.(colName);  % Извлекаем данные из текущего столбца
    
    % Вычисляем периодограмму
    [Pxx, ~] = periodogram(aa, [], n_points, fs, 'power');
    
    % Переводим в логарифмический масштаб с произвольным сдвигом
    power_dB = 100 + 10*log10(Pxx);
    
    % Сохраняем в структуру или матрицу
    all_power_data(:, i) = power_dB;
    
    % Строим график
    plot(f, power_dB, 'DisplayName', colName);
end

% Оформление графика
xlabel('Частота (Гц)');
ylabel('Мощность (дБ)');
title('АЧХ для разных столбцов таблицы');
legend show;
grid on;
hold off;

% Если нужно объединить частоты и все спектры в одну таблицу/матрицу:
dataToSave = [f, all_power_data];

%%%

writematrix(dataToSave, 'ACH_results.csv');