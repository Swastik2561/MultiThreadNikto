#!/bin/python3
import sys
import os
import subprocess
import threading



G, B, R, W, M, C, end = '\033[92m', '\033[94m', '\033[91m', '\x1b[37m', '\x1b[35m', '\x1b[36m', '\033[0m'
info = end + W + "[-]" + W
good = end + G + "[+]" + C
bad = end + R + "[" + W + "!" + R + "]"


def nikto_ssl(host):
    print(good + "Running Nikto for the %s" % host)
    output = subprocess.run(["nikto", "-host", host, "-ssl"], capture_output=True, text=True)
    filename = str(threading.current_thread().getName()) + ".tmp.txt"
    f = open(filename, "w")
    f.write(str(output.stdout))

def nikto_nossl(host):
    print(good + "Running Nikto For the no ssl %s "% host)
    output = subprocess.run(["nikto", "-host", host, "-nossl"], capture_output=True, text=True)
    filename = str(threading.current_thread().getName()) + ".tmp.txt"
    f = open(filename, "w")
    f.write(str(output.stdout))



def main():
    print("This is MNikto\n")
    print("*"*30)

    if len(sys.argv) < 4:
        print(info + "Usage python3 <program_name>.py <host_file> < ssl/nossl > <outputfilename>")
        print(info + "Remember All the hosts will run with same configuration\n")
        exit(0)

    host_file = sys.argv[1]
    sslc = sys.argv[2]
    file = sys.argv[3]
    if sslc == "ssl" or sslc == "SSL":
        sslc = 1
        print(good + "Running with SSL\n")

    else:
        sslc = 0
        print(good + "Running without SSL\n")

    with open(host_file, "r") as f:
        hosts = f.read()
        hosts = hosts.split("\n")

    #Last null element removal
    i = len(hosts)
    while hosts[i-1] is "":
        hosts.pop()
        i = i - 1
    #End of null elements removal

    p = {}
    if sslc:
        i = 0
        for i in range(len(hosts)):
            p[i] = threading.Thread(target=nikto_ssl, args=(hosts[i],))
            print(p[i].getName())
            p[i].start()
    else:
        i = 0
        for i in range(len(hosts)):
            p[i] = threading.Thread(target=nikto_nossl, args=(hosts[i],))
            print(p[i].getName())
            p[i].start()


    for i in range(len(hosts)):
        p[i].join()

    print("Creating A Nice File for Analysis\n")
    fw = open(file, "w")

    for i in range(len(hosts)):
        thread_file = "Thread-%s.tmp.txt" % str(i+1)
        print("Thread file copying %s" % thread_file)
        with open(thread_file, "r") as fr:
            fw.write("Mnikto %s" % hosts[i])
            fw.write("\n")
            fw.write(fr.read())
            fw.write("\n")
    print(good + "Writing Complete!\n")
    print(info + "Removing The Temprory Files\n")
    os.system("rm -f Thread-*")
    print(good + "Program Ended")

if __name__ == '__main__':
    main()
