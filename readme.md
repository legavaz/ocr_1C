
//создание образа
docker build -t ocr-pak .

//запуск образа с пробросом сети
docker run -it --network host -v //l-pack/net/Сканер/1C/4825036196/10032021:/home/web ocr_pak 
docker run -it --network host -v D:\temp\scan:/home/web ocr-pak 


//описание проекта
https://docs.google.com/document/d/1pYPnBihBenWhnbUZpqSguGF-x2Z1U7baV8UnjuuEsnE/edit?usp=sharing

//19-03 - Необходимо подключить шару
https://pypi.org/project/pysmb/

(10:30:21) Сигунов Алексей: там над копать в сторону smbclient
(10:31:57) Сигунов Алексей: проверить можно если в командной строке запустить mount.cifs

mkdir /mnt/my_folder
#монтируем шару в папку
mount -t smbfs -o username=<LOGIN>,password=<PASSWORD> //file-server-1/bhs-exchange /mnt/my_folder
#размонтируем
umount /mnt/my_folder
(8:16:06) Балчугов Дмитрий: это команды OS, выполняются, скорее всего как-то так:
import os
os.system(my_command)