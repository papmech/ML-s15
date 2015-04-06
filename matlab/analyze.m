clear; close all;
load('results.mat');

f = figure;
imagesc(avglrcmat);
colorbar;
title('Confusion matrix for Logistic Regression');

g = figure;
imagesc(avgnbcmat);
colorbar;
title('Confusion matrix for Naive Bayes');
saveas(f, 'confusionlr' ,'png');
saveas(g, 'confusionnb' ,'png');