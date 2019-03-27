#ifndef _TF_MODEL_
#define _TF_MODEL_

#include <cstring>
#include <iostream>
#include <vector>
#include <memory>

#include "tensorflow/c/c_api.h"


using Vec = std::vector<float>;
using Array = std::vector<Vec>;

class TFModel {
public:
  TFModel() = default;
  TFModel(const std::string export_dir);
  
  int predict(float* X, int nbytes);
  
private:
  void _load_exported_model(const std::string export_dir);
  
  std::string export_dir;
  
  TF_Graph* graph;
  //TF_Buffer* meta_graph;
  TF_Session* session;
};

#endif
