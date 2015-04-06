clear; close all;

data = csvread('pixels.data');
fileID = fopen('labels.data', 'r');
labels = fscanf(fileID, '%c\n');
labels = double(labels') - 96;
% labels = labels';
nchars = numel(unique(labels));

[nobs, nfeats] = size(data);
nfolds = 10;

%% Naive Bayes
indices = crossvalind('Kfold', nobs, nfolds);
nbcmat = [];
nberr = [];
for i=1:nfolds
    i
    test = (indices==i); train = ~test;
    trainData = data(train, :);
    trainLabels = labels(train);
    testData = data(test, :);
    testLabels = labels(test);
    NB = fitNaiveBayes(trainData, trainLabels, 'Distribution', 'mvmn');
    predicted = NB.predict(testData);
    nbcmat = [nbcmat confusionmat(testLabels, predicted)];
    nberr = [nberr sum(predicted~=testLabels)/numel(testLabels)];
end
avgerrnb = mean(nberr);

%% Logistic Regr
nfolds = 3;
setsize = 2000;
setindices = randsample(nobs, setsize);
data = data(setindices, :);
data = compute_mapping(data, 'PCA', 30);
[nobs, nfeats] = size(data);
indices = crossvalind('Kfold', nobs, nfolds);
lrerr = [];
lcrmat = [];
for i=1:nfolds
    i
    test = (indices==i); train = ~test;
    trainData = data(train, :);
    trainLabels = labels(train);
    testData = data(test, :);
    testLabels = labels(test);
    [B, dev, stats] = mnrfit(trainData, trainLabels);
    probs = mnrval(B, testData);
    [~, ind] = sort(probs, 2);
    predicted = ind(:, end);
    lrcmat = [lcrmat confusionmat(testLabels, predicted)];
    lrerr = [lrerr sum(predicted~=testLabels)/numel(testLabels)];
end
avglrerr = mean(lrerr);

save('results.mat', 'nberr', 'nbcmat', 'lrerr', 'lrcmat');
