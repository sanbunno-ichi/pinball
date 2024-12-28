# pyxelとpymunkでpinball
pymunkのexsampleのflipper.pyをpyxelで動くようにしました。  

pymunkのexampleのflipper.pyを動かすとこんな画面  
![SS](pymunk_flipper.png)

これをpyxelで動くようにしたものが  
![SS](pyxel_flipper.png)

## Web化チャレンジ２（pymunk installで404エラーになってる）
- [this Web](https://sanbunno-ichi.github.io/pinball/)

> 動作ログ  
> Launch Pyxel  
> pyxel.js:45 Object  
> NoSleep.min.js:2 Wake Lock active.  
> pyodide.asm.js:10 Loading pyxel  
> pyodide.asm.js:10 Loaded pyxel  
> pyodide.asm.js:10 Loading micropip, packaging  
> pyodide.asm.js:10 Loaded micropip, packaging  
> pyxel.js:209 Copied './pyxel_flipper_web.pyxapp' to '/pyxel_working_directory/pyxel_flipper_web.pyxapp'  
> pyodide.asm.js:10 Installing Pymunk...  
> pyodide.asm.js:10   
>           
> GET https://sanbunno-ichi.github.io/pinball/pymunk-6.10.0-cp312-cp312-pyodide_2024_0_wasm32.whl 404 (Not Found)  
  
さすがにここには無いので404エラーにはなるけど、なぜここを見る？  
micropipの挙動がおかしい？  
  
## Web化（FC2ではエラーになって起動できず）
- [FC2 WEB](https://sanbunnoichi1962.web.fc2.com/pyxel/pyxel_flipper.html)
  
エラーメッセージを翻訳すると  
> CORS ポリシーによってブロックされました: 要求されたリソースに「Access-Control-Allow-Origin」ヘッダーが存在しません。不透明な応答がニーズを満たす場合は、リクエストのモードを「no-cors」に設定して、CORS を無効にしてリソースをフェッチします。
  
## 更新履歴
2024.12.28 pyxel_pinball公開

