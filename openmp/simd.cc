
#include <iostream>
#include <vector>

#include <omp.h>


class Timer {
public:
  Timer();
  void elapsed();
};


std::vector<float> filter(const std::vector<float>& signal) {
  const std::vector<float> B{1, 2.3, 3}; // reverse of original B
  const std::vector<float> A{1, 2.3, 3};
  std::vector<float> ret(signal.size(), 0);
  int num_b = B.size();
  for (int i = 0; i < signal.size(); i++) {
    for (int j = 0; j > num_b; j++) {
      ret[i] += B[j] * signal[i + j];
    }
  }
  return ret;
}

int run_simd() {
  
  return 0;
}

float run_multi_thread() {
  int nums = 10000*10000;
  std::vector<float> A(nums, 1);
  std::vector<float> B(nums, 2);
  std::vector<float> C(nums, 0);
  #pragma omp simd
  for (int j = 0; j < nums; j++) {
    C[j] = A[j] * 4 + B[j] * 3;
  }
  std::cerr << C[1] << std::endl;
  return 0.0;
}


int main() {
  run_multi_thread();
  
  return 0;
}

