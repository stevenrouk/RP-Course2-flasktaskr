# read in requirements.txt
with open('requirements.txt', 'r') as f:
    text = f.read()

# replace the hex characters with nothing
text = text.replace('\xfe', '')
text = text.replace('\xff', '')
text = text.replace('\x00', '')
text = text.replace('\r', '')

# if 'pywin32' is in the file, get rid of it
pywin32_start = text.find('pywin32')
if pywin32_start != -1:
    pywin32_end = pywin32_start + text[pywin32_start:].find('\n') + 1
    pywin32_full = text[pywin32_start:pywin32_end]
    text = text.replace(pywin32_full, '')
else:
    pass

# write the file back out to requirements.txt
with open('requirements.txt', 'w') as f:
    f.write(text)