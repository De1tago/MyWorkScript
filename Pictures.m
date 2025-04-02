% run_b_mag_simple_in_folders.m
% из скрипта и_ьфп_ышьзду удали строчку clear all
% в начало файла добавить currentDir_bak = pwd; % Резервное копирование директории
% в конец cd(currentDir_bak); % Возврат
clear all;
currentDir = pwd; % Сохраняем абсолютный путь исходной директории

% Генерируем значения от 5.100 до 5.775 с шагом 0.025
values = 5.303:0.010:5.9;

for i = 1:length(values)
    folderName = sprintf('T_gap30_square500x500_b_mag_f_%.3f.out', values(i)); 
    
    if exist(folderName, 'dir')
        % Переходим в папку через абсолютный путь
        targetDir = fullfile(currentDir, folderName);
        cd(targetDir);
        disp(['Запуск b_mag_simple.m в папке: ', folderName]);
        
        % Запускаем скрипт в изолированном окружении
        run('b_mag_simple.m'); % Используем run() вместо прямого вызова
        
        % Сохраняем все открытые графики
        figHandles = findall(groot, 'Type', 'figure');
        for figNum = 1:length(figHandles)
            figure(figHandles(figNum));
            saveas(gcf, sprintf('figure_%d.png', figNum)); 
        end
        
        close all; 
        cd(currentDir); % Возврат через абсолютный путь
    else
        warning('Папка "%s" не найдена. Пропуск.', folderName);
    end
end

disp('Выполнение завершено.');