# generate-wg-configs
## Скрипт для генерации клиентских конфигов для WireGuard
Выполняться скрипт должен на сервере\
В коде необходимо заменить плейсхолдеры на соответствующие значения 
* your_server_public_key - публичный ключ сервера
* your_server_ip - IP-адрес сервера
* your_server_port - порт сервера

Далее запускаем скрипт, он запросит имя клиента, вводим его, и после этого будет сгенерирован конфиг

```python3 wg-clients.py```

После того, как все конфиги сгенерированы нужно перезапустить WireGuard

```wg-quick down "your_server_config_name"```\
```wg-quick up "your_server_config_name"```
