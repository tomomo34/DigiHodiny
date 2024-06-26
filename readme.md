
# DigiHodiny

Program pro nahravani casu do digitronovych hodin.


## Instalace

Stahnout ardcom.exe z releases
```bash
https://github.com/tomomo34/DigiHodiny/releases/latest
```
Zapnout a program by se sam mel pripojit k arduinu pokud je zapojene nebo vyhodi jeden z moznych erroru.

1. `arduino nenalezeno`: Tento log se zaznamená, když není nalezeno Arduino se zadaným sériovým číslem. To se stane, pokud Arduino není připojeno nebo pokud je zadané špatné sériové číslo.

2. `{string2} found in {string1}`: Tento log se zaznamená, když je řetězec `string2` nalezen v `string1` v rámci funkce `compare_strings`. Pokud je tato funkce volána a `string2` je podřetězec `string1`, pak se zaznamená tento log.

3. `{string2}' not found in '{string1}`: Tento log se zaznamená, když řetězec `string2` není nalezen v `string1` v rámci funkce `compare_strings`. Pokud je tato funkce volána a `string2` není podřetězec `string1`, pak se zaznamená tento log.

4. `logging.info(result)`: Tento log se zaznamená, když je volána funkce `get_formatted_datetime` a vrátí formátovaný časový řetězec.

5. `logging.info(value)`: Tento log se zaznamená, když je volána funkce `write_read` a vrátí data z Arduina.

6. `logging.info(data)`: Tento log se zaznamená, když je přečtena data z Arduina.

7. `datum nahrano`: Tento log se zaznamená, když je úspěšně porovnána hodnota z Arduina s očekávaným výsledkem.

8. `datum nebylo uspesne nahrano`: Tento log se zaznamená, když není úspěšně porovnána hodnota z Arduina s očekávaným výsledkem po určitém počtu pokusů.

9. `logging.critical(e)`: Tento log se zaznamená, když dojde k výjimce během provádění kódu.

## Princip fungovani

Kod navaze komunikaci s arduinem arduino je hleddany podle jeho serioveho cisla.
Po navazanin komunikace si python pres datetime stahne aktualni datum ve formatu %Y%m%d%H%M%S a odesia kod jako utf-8 bytes do arduina. 
Arduino zjisti ze je mu posilano datum a zacne poslouchat na COM portu.
Finalne probehne kontrola kdy arduino odesle zpet data co prijalo a python porovna ocekavanou a prijatou hodnotu. Pokud se data shoduji bylo datum uspesne nahrano pokud ne probiha druhy pokus.
Z nejakeho duvodu se vetsinou datum odesle na nekolikaty pokus obcas je potreba i manualni restart COM (vypojeni a zapojeni arduina)
Kod ma padesat pokusu nez vyhodi err.

## Jak posavit kod se zmenami
```bash
pip install pyinstaller
```
```bash
cd #do mista ulozeni#
```
```bash
pyinstaller --onefile --clean ardcom.py
```

## Princip fungovani

Kod ktery vygeneruje cas a odesle
```python
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.02)
    data = arduino.readline()
    return data
def get_formatted_datetime():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y%m%d%H%M%S')
    return formatted_datetime
def compare_strings(string1, string2):
    pattern = re.compile(string2)
    match = re.search(pattern, string1)
```

Kod ktery na arduinu prijma cas
```C#
  if (Serial.available() > 0) {
    x = Serial.readString();
    Serial.println("Received String: " + x);
    
    // Check if the received string is long enough
    if (x.length() >= 14) {
      processReceivedData(x);
      wholereset();
      first = true;
    } else {
      Serial.println("Invalid input length");
    }
  }
```