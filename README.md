# CryptHelper
Protect files by layered encryption with multiple keys.


```
# python3 CryptHelper_Main.py -h

_---_--_----_--------__-_-____--_---__--_--_----__-_-_-----__-------
|     _       `  .  crypthelper  , .     do `  ~   magic  * ` .
|    (o)        *    	*  .    might   *   the   ~ *  . `
|   |[~]|
|    | |     *    `    .      ~  *     `     .
|    " "
_---_--_----_--------__-_-____--_---__--_--_----__-_-_-----__-------



usage: CryptHelper_Main.py [-h] [-k GET_KEY] [-e] [-d] file

crypthelper

positional arguments:
  file                  file to apply multiple encrypts/decrypts

options:
  -h, --help            show this help message and exit
  -k GET_KEY, --key GET_KEY
                        load an existing key
  -e, --encrypt         to set the flag for encryption (if option -k is not used a new key will be generated)
  -d, --decrypt         to set the flag for decryption
```
