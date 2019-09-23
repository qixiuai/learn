
#include <iostream>
#include <vector>


int main() {
  std::vector<float> arr{0,1,2};
  std::vector<float> dest{-2,-1};
  
  dest.insert(dest.end(), arr.begin(), arr.end());
  
  for (auto v : dest)
    std::cout << v << '\n';

  return 0;
}

