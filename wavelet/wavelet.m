
%%

len = 2^11;
h = [4  -5  3  -4  5  -4.2   2.1   4.3  -3.1   5.1  -4.2];
t = [0.1  0.13  0.15  0.23  0.25  0.40  0.44  0.65  0.76  0.78  0.81];
h  = abs(h);
w  = 0.01*[0.5 0.5 0.6 1 1 3 1 1 0.5 0.8 0.5];
tt = linspace(0,1,len);
xref = zeros(1,len);
for j=1:11
    xref = xref+(h(j)./(1+((tt-t(j))/w(j)).^4));
end


%%
plot(tt, xref)

%%
rng default;
x = xref + 0.5*randn(size(xref));
plot(x)
set(gca,'xlim',[1 2048]);
%%
dwtmode('per');
[xd,cxd,lxd] = wden(x,'sqtwolog','s','sln',4,'sym4');
plot(xd)
set(gca,'xlim',[1 2048])
hold on
plot(xref,'r')
legend('Denoised','Reference')
%% 
glt = csvread("glt.txt");
%plot(glt(1:5000));
dwtmode('per');
[xd,cxd,lxd] = wden(glt,'sqtwolog','s','sln',4,'sym4');
plot(xd)
hold on;
plot(glt);

%%
load cuspamax;
dict = {{'wpsym4',1},{'db4',2},'dct','sin','RnIdent'};
mpdict = wmpdictionary(length(cuspamax),'lstcpt',dict);
[yfit,r,coeff,iopt,qual] = wmpalg('OMP',cuspamax,mpdict,'typeplot',...
    'movie','stepplot',5);