
libserver.so: server.cc server.h
	g++ -fPIC -shared server.cc server.h -Wl,-soname,libserver.so -o libserver.so

test: test.c server.h
	gcc test.c server.h -L. -lserver -I.


clean:
	rm *.gch *.so
