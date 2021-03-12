
//создание образа
docker build -t ocr-pak .

//запуск образа с пробросом сети
docker run -it --network host -v //l-pack/net/Сканер/1C/4825036196/10032021:/home/web ocr_pak 
docker run -it --network host -v D:\temp\scan:/home/web ocr-pak 



//10.0.75.1/D