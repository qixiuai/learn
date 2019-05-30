FLAGS = -fPIC

# the python interface through swig
PYTHONI = -I/home/guo/anaconda3/include/python3.6m/
PYTHONL = -Xlinker -export-dynamic

# default super-target
all: 
	g++ -fPIC -c kitty.cc -o kitty.o
	swig -c++ -python -o kitty_wrap.cxx kitty.i 
	g++ $(FLAGS) $(PYTHONI) -c kitty_wrap.cxx -o kitty_wrap.o
	g++ $(PYTHONL) $(LIBFLAGS) -shared kitty.o kitty_wrap.o -o _kitty.so
