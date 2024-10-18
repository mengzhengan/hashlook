# hashlook
## 安装依赖

## 1.查看hash值类型和对应明文
下面展示一些 `内联代码片`。

```
python hashlook.py -L dc1fd00e3eeeb940ff46f457bf97d66ba7fcc36e0b20802383de142860e76ae6
```
        
        hash值类型: sm3
        明文: admin
## 2.查看明文的hash值
        python hashlook.py -M admin
        md5: 21232f297a57a5a743894a0e4a801fc3
        sha1: d033e22ae348aeb5660fc2140aec35850c4da997
        sm3: dc1fd00e3eeeb940ff46f457bf97d66ba7fcc36e0b20802383de142860e76ae6
        sha224: 58acb7acccce58ffa8b953b12b5a7702bd42dae441c1ad85057fa70b
        sha256: 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
        sha384: 9ca694a90285c034432c9550421b7b9dbd5c0f4b6673f05f6dbce58052ba20e4248041956ee8c9a2ec9f10290cdc0782
        sha512: c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec
        sha3_224: a53fff8dd075bed169e164743231ff533d8b9260b0b8073f0a4c1d20
        sha3_256: fb001dfcffd1c899f3297871406242f097aecf1a5342ccf3ebcd116146188e4b
        sha3_384: 9765a57f2010506383de91052915ce8bafbdb39f3e5a8c1a1693a0076365d37abbfd3305881ea3b5fa1426316afd7df3
        sha3_512: 5a38afb1a18d408e6cd367f9db91e2ab9bce834cdad3da24183cc174956c20ce35dd39c2bd36aae907111ae3d6ada353f7697a5f1a8fc567aae9e4ca41a9d19d
  ## 3.增加明文的hash值
        python hashlook.py  -I './test.txct'
        1234545已存在
        admin已存在
        1341qaeq已存在
        qer13214已存在
        插入完成
        原有7519条记录
        现有7520
        成功插入 1 条记录。
