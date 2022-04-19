# amazonRestockNotification
Amazonの在庫通知


### 2022/4/8 メモ
通信費用と商品数のコスパバランスが悪いため一度停止 費用はNATゲートウェイの使用による通信費  
再度起動する際は、EC2、botを起動しなおす  
```
docker-compose up -d
sh entrypoint.sh
```
