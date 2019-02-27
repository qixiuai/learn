
#include <cpprest/http_client.h>
#include <cpprest/filestream.h>
#include <cpprest/json.h>
#include <cpprest/http_listener.h>
#include <cpprest/uri.h>
#include <cpprest/asyncrt_utils.h>
#include <cpprest/filestream.h>
#include <cpprest/containerstream.h>
#include <cpprest/producerconsumerstream.h>

using namespace utility;
using namespace web;
using namespace web::http;
using namespace web::http::client;
using namespace concurrency::streams;


void ClientCall() {
  auto fileStream = std::make_shared<ostream>();

  pplx::task<void> requestTask = fstream::open_ostream(U("results.html")).then([=](ostream outFile)
    {
      *fileStream = outFile;

      http_client client(U("http://www.cn.bing.com/"));

      uri_builder builder(U("/search"));
      builder.append_query(U("q"), U("cpprestsdk github"));
      return client.request(methods::GET, builder.to_string());
    })
    .then([=](http_response response) {
	printf("Received response status code:%u\n", response.status_code());
	return response.body().read_to_end(fileStream->streambuf());
      })
    .then([=](size_t) {
	return fileStream->close();
      });
  try {
    requestTask.wait();
  }
  catch (const std::exception &e) {
    printf("Error exception:%s\n", e.what());
  }
}


int main() {
  ClientCall();
  
  return 0;
}




