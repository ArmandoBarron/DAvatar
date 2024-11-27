import psutil
import time

def cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

def mem_usage():
    mem_usage = psutil.swap_memory()
    return mem_usage.percent

def net_usage():
    net_stat = psutil.net_io_counters(pernic=False)
    net_res_1 = net_stat.bytes_recv + net_stat.bytes_sent
    time.sleep(1)
    net_stat = psutil.net_io_counters(pernic=False)
    net_res_2 = net_stat.bytes_recv + net_stat.bytes_sent
    net_res = round((net_res_2 - net_res_1) / 1024 / 1024, 3)
    return net_res
    #print("NET usage: "+str(net_res))

def disk_usage():
    disk_usage = psutil.disk_usage('/')
    return disk_usage.percent

cpu = cpu_usage()
mem = mem_usage()
net = net_usage()
disk = disk_usage()

print("CPU USAGE: "+str(cpu))
print("MEM USAGE: "+str(mem.percent))
print("NET USAGE: "+str(net))
print("DISK USAGE: "+str(disk.percent))