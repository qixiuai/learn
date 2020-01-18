
#include <thread>
#include <iostream>

void foo() {
  std::cerr << "in foo...\n"; 
}

void bar(int x) {
  std::cerr << "in bar...\n";
}

int main() {
  std::thread first(foo);
  std::thread second(bar, 0);

  std::cout << "main, foo and bar now execute concurrently...\n";
  
  first.join();
  second.join();
  
  std::cout << "foo and bar completed.\n";
  return 0;
}



