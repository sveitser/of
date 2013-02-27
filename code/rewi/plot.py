# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

d = loadtxt('grid10.dat')
x = unique(d[:, 0])
y = unique(d[:, 1])
X, Y = meshgrid(x, y)
z = d[:,2] * (1 - d[:,0]) # rescale
#z = d[:, 2]

Z = reshape(z,(len(x), -1))
print(shape(X),shape(Y),shape(Z))
pcolor(X,Y,transpose(Z))
c = colorbar()
c.set_label("$t$")
xlabel("$\phi$")
ylabel("$\eta$")
savefig("test.pdf")

# <codecell>

help(pcolor)

# <codecell>


