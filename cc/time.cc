
#include <string>
#include <iostream>
#include <cstdio>
#include <ctime>


class Timer {
public:
  Timer(std::string name) {
    start = std::clock();
    this->name = name;
  }
  
  void eplapsed() {
    double duration;
    duration = (std::clock() - start) / (double) CLOCKS_PER_SEC;
    std::cout << "[" << name << "] eplapsed: " << duration << "\n";
  }
  
  void reset() {
    start = std::clock();
  }
  
private:
  std::clock_t start;
  std::string name;
};

int main() {
  
  std::clock_t start;
  double duration;
  
  start = std::clock();
  int a = 1;
  a += 1;
  duration = (std::clock() - start) / (double) CLOCKS_PER_SEC;
  
  std::cout << duration << "\n";
  
  return 0;
}



