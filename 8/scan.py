import os , ctypes
from time import sleep
from sys import argv
from mem_edit import Process



def cons(nober_serva,miner_nomb):
    with open(f'/root/{nober_serva}/{miner_nomb}/log/miner.log.log') as f:
       data_log = f.read()
    cons_p=data_log[data_log.rfind("scan consume="):data_log.rfind("scan consume=")+17]
    cons=cons_p[13:]
    return cons

def read_hex(nober_serva,miner_nomb):
    initial_value = int(cons(nober_serva,miner_nomb))
    print(initial_value)
    pid = Process.get_pid_by_name('miner' + str(miner_nomb))
    print(pid)
    with Process.open_process(pid) as p:
        addrs = p.search_all_memory(ctypes.c_int(initial_value))
        print(addrs)
        while initial_value == int(cons(nober_serva,miner_nomb)):
            sleep(2)
            final_value = int(cons(nober_serva,miner_nomb))
        print(final_value)
        filtered_addrs = p.search_addresses(addrs, ctypes.c_int(final_value))
        print('Found addresses:')
        for addr in filtered_addrs:
            addr=str(hex(addr))
            print(addr)
    return addr,pid


nober_serva = argv[1] 
miner_nomb = argv[2]

while '0 sc' == str(cons(nober_serva,miner_nomb)):
    print('ОЖИДАЮ НОНСУМЕ ОТЛИЧНОГО ОТ 0 ')
    sleep(2)


try:
    os.system('apt install scanmem')
    data_scanmem=read_hex(nober_serva,miner_nomb)
except:
    print('Ошибка в получении даныых для сканмема')
    input('Жду решения')





DIR = os.getcwd()
print(DIR)
print('СТАРТУЮ ЗАМОРОЗКУ СКАНТАЙМ')
sleep(2)

t=0
while True:
    t+=1
    if os.listdir(DIR):
       os.system(f"scanmem -p {data_scanmem[1]} -c 'write i32 {data_scanmem[0]} 3621;quit'")
       sleep(5)






       

