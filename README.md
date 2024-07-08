# VisionDataForge


#### Установка библиотек
```shell
python -m pip install -r requirements/requirements.txt 
```
на Linux torch CUDA установиться сам если есть CUDA драйвера


#### Установка CUDA для Windows
```shell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```


#### Генерация ключей для JWT
```bash
mkdir certs && cd certs && openssl genrsa -out jwt-private.pem 2048 && \
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```


#### Файл окружения `.env`
Создать файл `.env` по образцу `.env-example`


#### Запуск
```shell
uvicorn src.main:app --reload
```