# VisionDataForge


### Установка библиотек
```shell
python -m pip install -r requirements/requirementsCPU.txt 

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

```bash
mkdir certs && cd certs && openssl genrsa -out jwt-private.pem 2048 && openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

### Запуск
```shell
uvicorn src.main:app --reload
```