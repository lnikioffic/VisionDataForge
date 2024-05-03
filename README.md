# VisionDataForge


### Установка библиотек
```
python -m pip install -r requirements/requirementsCPU.txt 

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Запуск
```
uvicorn src.main:app --reload
```