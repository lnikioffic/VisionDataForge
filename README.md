# VisionDataForge


### Установка библиотек
```
python -m pip install -r requirements/requirementsCPU.txt 

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Запуск
```
uvicorn src.main:app --reload
```