
#include <iostream>
#include <vector>
#include <string>

class Base {
public:
  virtual void print(std::string c) = 0;
  void print_no() {
    print("ageege");
  }
};

class Child : public Base {
public:
  Child() {}
  void print(std::string c) override {
    std::cerr << "child\n";
  }
};


int main() {
  Child child;
  child.print_no();
  return 0;
}
