#!/usr/bin/python
# R-Finder ( File & Open Directory finder ) - R&D ICWR

print("""
 /$$$$$$$        /$$$$$$$$/$$               /$$                  
| $$__  $$      | $$_____|__/              | $$                  
| $$  \ $$      | $$      /$$/$$$$$$$  /$$$$$$$ /$$$$$$  /$$$$$$ 
| $$$$$$$//$$$$$| $$$$$  | $| $$__  $$/$$__  $$/$$__  $$/$$__  $$
| $$__  $|______| $$__/  | $| $$  \ $| $$  | $| $$$$$$$| $$  \__/
| $$  \ $$      | $$     | $| $$  | $| $$  | $| $$_____| $$      
| $$  | $$      | $$     | $| $$  | $|  $$$$$$|  $$$$$$| $$      
|__/  |__/      |__/     |__|__/  |__/\_______/\_______|__/      
=================================================================
[*] R-Finder V 2.0 ( File & Open Directory finder ) - R&D ICWR
=================================================================
""")

import ssl, random, socket, warnings
from sys import stdout
from argparse import ArgumentParser
from multiprocessing.pool import ThreadPool

warnings.filterwarnings("ignore")

class finder:

    def percentageProc(self):

        self.procDone += 1
        self.processCount = int(self.procDone / self.totalProc * 100)

    def useragent(self):

        arr = [

            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.0.12) Gecko/2009070611 Firefox/3.0.12 (.NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
            "Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/6.0.427.0 Safari/534.1"

        ]

        return arr[random.randint(0, len(arr) - 1)]

    def check(self, path):

        try:

            head = "GET /{} HTTP/1.1\r\n".format(path)
            head += "Host: {}\r\n".format(self.args.target.split("/")[2])
            head += "User-Agent: {}\r\n".format(self.useragent)
            head += "Connection: Keep-Alive\r\n"
            head += "Accept: */*\r\n\r\n"

            if self.args.target.split(":")[0] == "https":

                get_ssl = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                s = get_ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname = self.args.target.split("/")[2])
                port = 443

            elif self.args.target.split(":")[0] == "http":

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                port = 80

            s.settimeout(self.args.timeout)
            s.connect((self.args.target.split("/")[2], port))
            s.send(head.encode())
            response = s.recv(50).decode()
            s.close()

            if ("200" in response):

                self.result += "[+] {}/{}\n".format(self.args.target, path)

        except:

            pass

        self.percentageProc()

        stdout.write("\r[*] Process : {}%".format(self.processCount))
        stdout.flush()

    def __init__(self):

        print("[*] R-Finder Running")

        self.procDone = 0
        self.result = ""
        parser = ArgumentParser()
        parser.add_argument("-x", "--target", required = True)
        parser.add_argument("-l", "--list", required = True)
        parser.add_argument("-t", "--thread", required = True, type = int)
        parser.add_argument("-d", "--timeout", required = True, type = int)
        self.args = parser.parse_args()

        self.totalProc = len(open(self.args.list).read().splitlines())

        print("[*] Finding...")

        ThreadPool(self.args.thread).map(self.check, open(self.args.list).read().splitlines())

        print("\n")
        print("[*] Result:\n")

        if self.result != '':

            print(self.result)

        else:

            print("[-] No result")

finder() if __name__ == "__main__" else exit()
