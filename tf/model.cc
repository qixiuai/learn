
#include "model.h"

#include <cstring>

#include <iostream>
#include <vector>
#include <memory>

#include "tensorflow/c/c_api.h"


TFModel::TFModel(const std::string export_dir) {
  _load_exported_model(export_dir);
}

void TFModel::_load_exported_model(const std::string export_dir) {
  const char* const tags = "serve";
  int tags_len = 1; // ???
  TF_SessionOptions* opt = TF_NewSessionOptions();
  TF_Buffer* run_options = TF_NewBufferFromString("", 0);
  TF_Buffer* meta_graph = TF_NewBuffer();
  TF_Status* status = TF_NewStatus();
  this->graph = TF_NewGraph();
  this->session = TF_LoadSessionFromSavedModel(opt, run_options,
					       export_dir.c_str(),
					       &tags, tags_len,
					       graph, meta_graph,
					       status);
}

/*
Vec TFModel::predict(float* X, int len) {
  // create feed info
  TF_Output feeds[]    = {{TF_GraphOperationByName(graph, "example"), 0}};
  float raw_values[]   = {1,2,3};
  const int64_t dims[] = {3};
  TF_Tensor* input_value = TF_AllocateTensor(TF_FLOAT, dims, 1, sizeof(float)*3);
  memcpy(TF_TensorData(input_value), raw_values, sizeof(float)*3);
  
  TF_NewTensor(TF_FLOAT, dims, 1,)
  
  TF_Tensor* feed_values[] = {input_value};
  TF_Output fetches[] = {{TF_GraphOperationByName(graph, "add"), 0}};
  TF_Tensor* fetch_values[] = {nullptr};
  int ninputs  = 1;
  int noutputs = 1;

  TF_Buffer* run_metadata = nullptr;
  const TF_Operation* const* target_opers = nullptr;
  int ntargets = 0;
  TF_Status* status = TF_NewStatus();
  TF_Buffer* run_options = TF_NewBufferFromString("", 0);
  TF_SessionRun(session, run_options,
		feeds,   feed_values,  ninputs,
		fetches, fetch_values, noutputs,
		target_opers, ntargets,
		run_metadata, status); 
  Vec y;
  return y;
  }
*/
int TFModel::predict(float* X, int len) {
  // create feed info
  TF_Output feeds[] = {{TF_GraphOperationByName(graph, "serving_default_input_1"), 0}};
  const int64_t dims[] = {1, 3000, 1};
  int num_dims = 3;
  int nbytes = sizeof(float) * len;
  TF_Tensor* input_values = TF_AllocateTensor(TF_FLOAT, dims, num_dims, nbytes);
  memcpy(TF_TensorData(input_values), X, nbytes);
  
  TF_Tensor* feed_values[] = {input_values};

  // create fetch info
  TF_Output fetches[] = {{TF_GraphOperationByName(graph, "StatefulPartitionedCall"), 0}};
  TF_Tensor* fetch_values[] = {nullptr};
  int ninputs = 1;
  int noutputs = 1;
  TF_Buffer* run_metadata = nullptr;
  const TF_Operation* const* target_opers = nullptr;
  int ntargets = 0;
  TF_Status* status = TF_NewStatus();
  TF_Buffer* run_options = TF_NewBufferFromString("", 0);
  TF_SessionRun(this->session, run_options,
		feeds, feed_values, ninputs,
		fetches, fetch_values, noutputs,
		target_opers, ntargets,
		run_metadata, status);
  auto ret = TF_TensorData(fetch_values[0]);
  auto prob = static_cast<float *>(ret);
  float max_prob = 0;
  int ind_max = -1;
  for (int i = 0; i < 5; i++) {
    float val = prob[i];
    if (val > max_prob) {
      ind_max = i;
      max_prob = val;
    }
  }
  return ind_max;
}

int main() {
  //std::string export_dir = "/home/guo/PSG/psg/stage/cc/saved_model/1541732153/";
  std::string export_dir = "/home/guo/Github/learn/tf/saved_models";
  TFModel model(export_dir);
  float* X = new float[3000];
  for (int i = 0; i < 3000; i++) {
    X[i] = 0;
  }
  auto label = model.predict(X, 3000);
  std::cerr << "predict label is :" << label << std::endl;
  return 0;
}
