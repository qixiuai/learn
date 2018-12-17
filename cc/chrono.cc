#include <iostream>
#include <chrono>
#include <thread>

int main() {
  using namespace std::chrono;
  system_clock::time_point start = system_clock::now();
  std::this_thread::sleep_for(1s);
  system_clock::time_point end = system_clock::now();
  
  auto m = duration_cast<milliseconds>(end-start).count();
  std::cout << static_cast<int>(m) << std::endl;
  return 0;
}
