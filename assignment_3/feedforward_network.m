% Redundant input such that there is some data for the test and validation
% data sets:
inputs  = [1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8];
outputs = [1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8];

net = feedforwardnet(1);
net = configure(net, inputs, outputs);

net.layers{1}.transferFcn = 'tansig';
net.divideParam.trainRatio = 0.7;
net.divideParam.valRatio   = 0.15;
net.divideParam.testRatio  = 0.15;
net.trainParam.showWindow  = 0;

net = train(net, inputs, outputs);

result = net(inputs);
plot(inputs,outputs,'o',inputs,result,'*')