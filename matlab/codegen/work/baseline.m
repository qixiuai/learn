%%
close all;
b = [1, -1];
a = [1, -0.99];
%data = ones(100,1) + randn(100,1);
data = zeros(100,1);
data(50:70) = 1;
signal = filter(b, a, data);

plot(data);
hold on;
plot(signal)