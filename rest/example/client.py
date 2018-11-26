
import requests
import pdb

def main():
    with open('/home/guo/PSG/data/A2-PSG_1811142338.edf', 'rb') as file:
        data = file.read()
    url = "http://127.0.0.1:5000/"
#    print(data[:10])
#    data = {"hello":"value"}
    data_buffer = {"edf" : data[:100]}
    response = requests.post(url, data=data_buffer)#, headers={"Content-Type": "application/json"})

if __name__ == '__main__':
    main()

