# Install And Running The Code

```
Last login: Thu Jan  2 19:52:44 on console
daveih@dih-m1-mini ~ % cd Documents/python/m11_specification 
daveih@dih-m1-mini m11_specification % python3 -m venv .venv
daveih@dih-m1-mini m11_specification % source .venv/bin/activate
(.venv) daveih@dih-m1-mini m11_specification % pip install -r requirements.txt 
Collecting PyPDF2>=3.0.0
  Downloading pypdf2-3.0.1-py3-none-any.whl (232 kB)
     |████████████████████████████████| 232 kB 4.3 MB/s 
Collecting pdfplumber>=0.10.2
  Downloading pdfplumber-0.11.5-py3-none-any.whl (59 kB)
     |████████████████████████████████| 59 kB 10.2 MB/s 
Collecting python-json-logger>=2.0.7
  Downloading python_json_logger-3.2.1-py3-none-any.whl (14 kB)
Collecting pypdfium2>=4.18.0
  Downloading pypdfium2-4.30.1-py3-none-macosx_11_0_arm64.whl (2.8 MB)
     |████████████████████████████████| 2.8 MB 10.2 MB/s 
Collecting pdfminer.six==20231228
  Downloading pdfminer.six-20231228-py3-none-any.whl (5.6 MB)
     |████████████████████████████████| 5.6 MB 10.7 MB/s 
Collecting Pillow>=9.1
  Downloading pillow-11.1.0-cp310-cp310-macosx_11_0_arm64.whl (3.1 MB)
     |████████████████████████████████| 3.1 MB 10.1 MB/s 
Collecting charset-normalizer>=2.0.0
  Using cached charset_normalizer-3.4.1-cp310-cp310-macosx_10_9_universal2.whl (198 kB)
Collecting cryptography>=36.0.0
  Using cached cryptography-44.0.0-cp39-abi3-macosx_10_9_universal2.whl (6.5 MB)
Collecting cffi>=1.12
  Using cached cffi-1.17.1-cp310-cp310-macosx_11_0_arm64.whl (178 kB)
Collecting pycparser
  Using cached pycparser-2.22-py3-none-any.whl (117 kB)
Installing collected packages: pycparser, cffi, cryptography, charset-normalizer, pypdfium2, Pillow, pdfminer.six, python-json-logger, PyPDF2, pdfplumber
Successfully installed Pillow-11.1.0 PyPDF2-3.0.1 cffi-1.17.1 charset-normalizer-3.4.1 cryptography-44.0.0 pdfminer.six-20231228 pdfplumber-0.11.5 pycparser-2.22 pypdfium2-4.30.1 python-json-logger-3.2.1
WARNING: You are using pip version 21.2.4; however, version 24.3.1 is available.
You should consider upgrading via the '/Users/daveih/Documents/python/m11_specification/.venv/bin/python3 -m pip install --upgrade pip' command.
(.venv) daveih@dih-m1-mini m11_specification % python main.py
{"message": "Starting template specification processing"}
{"message": "Starting technical specification processing"}
{"message": "Results saved to data/input_data/m11.json"}
(.venv) daveih@dih-m1-mini m11_specification % 
```