% Автоматическая обработка папок rect_afc*.out и сохранение Magnitude/Frequency графика
clear; clc; close all;

% Параметры сигнала
f0 = 6.0e9;           % центральная частота, Гц
Fs = f0 * 8;          % частота дискретизации, Гц

% Получаем список папок
dirs = dir('rect_afc*.out');

for i = 1:length(dirs)
    folder = dirs(i).name;
    filepath = fullfile(folder, 'table.txt');

    if isfile(filepath)
        fprintf('Обрабатываю %s...\n', filepath);
        
        % Загружаем таблицу
        data = readtable(filepath);

        % Проверяем количество столбцов
        if width(data) < 6
            warning('Файл %s имеет меньше 6 столбцов, пропускаю.\n', filepath);
            continue;
        end

        % Извлекаем 5-й и 6-й столбцы как сигналы
        col5 = table2array(data(:,5));
        col6 = table2array(data(:,6));

        signals = {col5, col6};
        labels = {'Column 5', 'Column 6'};

        % Создаем фигуру без отображения
        figure('Visible', 'off');
        hold on;

        for k = 1:2
            x = signals{k};
            N = length(x);

            % Применяем окно (для сглаживания спектра)
            w = hann(N);
            xw = x .* w;

            % БПФ
            X = fft(xw);

            % Частотная ось в Гц
            f = linspace(0, Fs/2, floor(N/2));

            % Амплитуда в дБ
            mag = 20*log10(abs(X(1:floor(N/2))));

            % Построение
            plot(f/1e9, mag, 'LineWidth', 1.4, 'DisplayName', labels{k});
        end

        xlabel('Частота, ГГц');
        ylabel('Амплитуда, дБ');
        title(sprintf('АЧХ (Magnitude/Frequency) для %s', folder), 'Interpreter', 'none');
        legend('show', 'Location', 'best');
        grid on;
        hold off;

        % Сохраняем график
        outname = fullfile(folder, 'AFC_freq.png');
        saveas(gcf, outname);
        fprintf('→ Сохранено: %s\n', outname);
        close(gcf);
    else
        warning('В папке %s нет table.txt\n', folder);
    end
end

fprintf('\n✅ Обработка завершена.\n');
