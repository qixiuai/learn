
#include <zmq.hpp>
#include <string>
#include <iostream>
#include <sstream>

int main() {
  zmq::context_t context(1);
  zmq::socket_t  socket(context, ZMQ_SUB);
  //  socket.connect("tcp://localhost:5555");
  socket.connect("ipc://5555");
  const char* filter = "10001";
  socket.setsockopt(ZMQ_SUBSCRIBE, filter, strlen(filter));
  std::cout << "Connecting to hello world server…" << std::endl;
  for (int request_nbr = 0; request_nbr != 1000; request_nbr++) {
    zmq::message_t update;
    socket.recv(&update);    
    int zipcode, temperature, relhumidity;
    std::istringstream iss(static_cast<char*>(update.data()));
    iss >> zipcode >> temperature >> relhumidity;
    std::cout << zipcode << ','
	      << temperature << ','
	      << relhumidity
	      << std::endl;
  }
  
  return 0;
}
