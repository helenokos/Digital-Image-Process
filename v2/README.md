以下為由上而下的 button 介紹  
@ open : 開啟圖片  
@ save : 存取圖片  
(1) : gray level slicing -> 第一小題關閉  
>	  mode a             -> 保留範圍外原有的值  
>	  mode b             -> 將範圍外的值都變成黑色  
(2) : bit plane	-> 第二小題關閉  
>	  click     -> 切換 1 ~ 8 的 bit plane  
	  
(3) :   
>	  smooth-> 1 為原圖，數字越大，smooth程度越大(此 function 為我自己寫的函式，會跑得有點慢)  
>	  sharp -> 1 為原圖，數字越大，sharp程度越大  

(4) : log|F(u,v)|  
>	  將 fft 結果取 log 之後再將值重新分配至 0 ~ 255 之間  
 
(5) : amplitude / phase image  
>	  amplitude -> 利用 2d-fft 印出 amplitude image  
>	  phase		-> 利用 2d-fft 印出 phase image  
	  
接下來為由上而下的 scale 介紹  
(1)(2) : 前兩個 scale 皆為第一小題所使用。所選範圍為 0 ~ 255  
(3)    : 最底下的 scale 為第三小題使用。代表 smooth/sharp 程度  

注意事項：  
目前尚未支援各功能同時使用，請確實關閉每個功能再開啟下個功能。
