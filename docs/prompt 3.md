# Prompt

None, amended code with single print statement

# Prompt Response

None

# Run

```Shell
(.venv) daveih@dih-m1-mini m11_specification % python main.py
{"message": "Starting template specification processing"}
COLOUR: (0, 0.2, 0.6), Official
COLOUR: (0, 0.2, 0.6), address
COLOUR: (0.427, 0.435, 0.443), Domenico
COLOUR: (0.427, 0.435, 0.443), Scarlattilaan
COLOUR: (0.427, 0.435, 0.443), 6
COLOUR: (0, 0.2, 0.6), ●
COLOUR: (0.427, 0.435, 0.443), 1083
COLOUR: (0.427, 0.435, 0.443), HS
COLOUR: (0.427, 0.435, 0.443), Amsterdam
COLOUR: (0, 0.2, 0.6), ●
COLOUR: (0.427, 0.435, 0.443), The
COLOUR: (0.427, 0.435, 0.443), Netherlands
COLOUR: (0.427, 0.435, 0.443), An
COLOUR: (0.427, 0.435, 0.443), agency
COLOUR: (0.427, 0.435, 0.443), of
COLOUR: (0.427, 0.435, 0.443), the
COLOUR: (0.427, 0.435, 0.443), European
COLOUR: (0.427, 0.435, 0.443), Union
COLOUR: (0, 0.2, 0.6), Address
COLOUR: (0, 0.2, 0.6), for
COLOUR: (0, 0.2, 0.6), visits
COLOUR: (0, 0.2, 0.6), and
COLOUR: (0, 0.2, 0.6), deliveries
COLOUR: (0.502,), Refer
COLOUR: (0.502,), to
COLOUR: (0.502,), www.ema.europa.eu/how-to-find-us
COLOUR: (0, 0.2, 0.6), Send
COLOUR: (0, 0.2, 0.6), us
COLOUR: (0, 0.2, 0.6), a
COLOUR: (0, 0.2, 0.6), question
COLOUR: (0.502,), Go
COLOUR: (0.502,), to
COLOUR: (0.502,), www.ema.europa.eu/contact
COLOUR: (0, 0.2, 0.6), Telephone
COLOUR: (0.427, 0.435, 0.443), +31
COLOUR: (0.427, 0.435, 0.443), (0)88
COLOUR: (0.427, 0.435, 0.443), 781
COLOUR: (0.427, 0.435, 0.443), 6000
COLOUR: (0.427, 0.435, 0.443), ©
COLOUR: (0.427, 0.435, 0.443), European
COLOUR: (0.427, 0.435, 0.443), Medicines
COLOUR: (0.427, 0.435, 0.443), Agency,
COLOUR: (0.427, 0.435, 0.443), 2022.
COLOUR: (0.427, 0.435, 0.443), Reproduction
COLOUR: (0.427, 0.435, 0.443), is
COLOUR: (0.427, 0.435, 0.443), authorised
COLOUR: (0.427, 0.435, 0.443), provided
COLOUR: (0.427, 0.435, 0.443), the
COLOUR: (0.427, 0.435, 0.443), source
COLOUR: (0.427, 0.435, 0.443), is
COLOUR: (0.427, 0.435, 0.443), acknowledged.
COLOUR: (0,), 26
Traceback (most recent call last):
  File "/Users/daveih/Documents/python/m11_specification/main.py", line 7, in <module>
    processor.save_to_json("data/output_data/m11.json")
  File "/Users/daveih/Documents/python/m11_specification/m11_specification/processor.py", line 167, in save_to_json
    result = self.process()
  File "/Users/daveih/Documents/python/m11_specification/m11_specification/processor.py", line 149, in process
    self.process_template_specification()
  File "/Users/daveih/Documents/python/m11_specification/m11_specification/processor.py", line 93, in process_template_specification
    color = self._extract_color_from_text(word)
  File "/Users/daveih/Documents/python/m11_specification/m11_specification/processor.py", line 51, in _extract_color_from_text
    elif (color[0] < 0.3 and color[1] < 0.3 and color[2] > 0.7):
IndexError: tuple index out of range
(.venv) daveih@dih-m1-mini m11_specification % 
```