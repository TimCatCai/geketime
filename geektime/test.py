import re
text = 'http://p3-tt.byteimg.com/list/568c0003cfccba420302'
pattern = r'list(/\d*x\d*)?'

print(re.sub(pattern, 'large', text))

print(text)
