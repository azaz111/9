import os
from time import sleep, time
import conf_bf

def pap_mount(name_osnova,nomber_osnova):
   try:
      sleep(2)
      sum_plot=len(os.listdir(f'/{name_osnova}/{nomber_osnova}-1.d'))
      sleep(2)
   except:
      sum_plot=0
   return sum_plot
   


schet=0
x=conf_bf.start_json
while True:
   q=0
   os.system ('pkill rclone')


   while q!=10:
      q+=1
      if conf_bf.osn_lim == conf_bf.osn_serv :
         conf_bf.osn_serv=conf_bf.osn_serv-10
        
      conf_bf.osn_serv+=1     
      name_osnova='osnova'+str(conf_bf.osn_serv)
      os.system (f'rclone backend set {name_osnova}: -o service_account_file="/root/AutoRclone/accounts/{x+1}.json"')
      os.system (f'screen -dmS "{name_osnova}" rclone mount {name_osnova}: /{name_osnova} --allow-non-empty --daemon --multi-thread-streams 30 --low-level-retries 2 --retries 2 --vfs-read-chunk-size 128K --drive-chunk-size 1M --buffer-size off --max-backlog 20000 --contimeout 9s --no-traverse --no-modtime --read-only --log-level INFO --stats 1m')

      x += 1

      if pap_mount(name_osnova,conf_bf.osn_serv) >= 1 :
         print(f'Диск {name_osnova} смонтирован ')
      else:
         print(f'Нет плотов {name_osnova} - , косяк')
         while True:
            schet=schet+1
            sleep(6)
            os.system (f'fusermount -uz /{name_osnova}')
            os.system (f'screen -dmS "{name_osnova}" rclone mount {name_osnova}: /{name_osnova} --allow-non-empty --daemon --multi-thread-streams 30 --low-level-retries 2 --retries 2 --vfs-read-chunk-size 128K --drive-chunk-size 1M --buffer-size off --max-backlog 20000 --contimeout 9s --no-traverse --no-modtime --read-only --log-level INFO --stats 1m')
            print( 'Пытаюсь повторно размонтировать')
            if pap_mount(name_osnova,conf_bf.osn_serv) >= 1 :
               print(' Повторно прокатило')
               schet=0
               break
            if schet == 4:
               schet=0
               break  


      #except:
      #   print('НЕТ ТАКОЙ ПАПКИ')

   sleep(2880)
   x += 10
   
   if x==conf_bf.lim_json:
      x=0
