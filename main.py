from flask import Flask
app = Flask(__name__)
# dictionary for unique function
flip = {'a':'ɐ',
'b':'q',
'c':'ɔ',
'd':'p',
'e':'ǝ',
'f':'ɟ',
'g':'ƃ',
'h':'ɥ',
'i':'ı',
'j':'ɾ',
'k':'ʞ',
'l':'ן',
'm':'ɯ',
'n':'u',
'o':'o',
'p':'d',
'q':'b',
'r':'ɹ',
's':'s',
't':'ʇ',
'u':'n',
'v':'ʌ',
'w':'ʍ',
'x':'x',
'y':'ʎ',
'z':'z',
'A':'∀',
'B':'𐐒',
'C':'Ɔ',
'D':'◖',
'E':'Ǝ',
'F':'Ⅎ',
'G':'⅁',
'H':'H',
'I':'I',
'J':'ſ',
'K':'⋊',
'L':'˥',
'M':'W',
'N':'N',
'O':'O',
'P':'Ԁ',
'Q':'Ό',
'R':'ᴚ',
'S':'S',
'T':'⊥',
'U':'∩',
'V':'Λ',
'W':'M',
'X':'X',
'Y':'⅄',
'Z':'Z',
'&':'⅋',
'.':'˙',
':':"'",
'[':']',
']':'[',
'(':')',
')':'(',
'{':'}',
'}':'{',
'?':'¿',
'!':'¡',
"'":":",
'"':'„',
'<':'>',
'>':'<',
'_':'‾',
'"':'„',
'\\':'/',
';':'؛',
'`':':',
'‿':'⁀',
'⁅':'⁆',
'∴':'∵',
'0':'0',
'1':'Ɩ',
'2':'ᄅ',
'3':'Ɛ',
'4':'ㄣ',
'5':'ϛ',
'6':'9',
'7':'ㄥ',
'8':'8',
'9':'6',
' ':' '}

@app.route("/")
def hello():
  return "Hello World!!!"

def ftoc(ftemp):
  return (ftemp - 32.0) * (5.0/9.0)

@app.route("/ftoc/<ftemp_str>")
def convert_ftoc(ftemp_str):
  ftemp = 0.0
  try:
    ftemp = float(ftemp_str)
    ctemp = ftoc(ftemp)
    return "In Fahrenheit: " + ftemp_str + "In Celsius :" + str(ctemp)
  except ValueError:
    return "Sorry.  Could not convert " + ftemp_str + " to a number."
    
def ctof(ctemp):
  return ctemp * (9.0/5.0) + 32

@app.route("/ctof/<ctemp_str>")
def convert_ctof(ctemp_str):
  ctemp = 0.0
  try:
    ctemp = float(ctemp_str)
    ftemp = ctof(ctemp)
    return "In Celsius: " + ctemp_str + " In Fahrenheit: " + str(ftemp)
  except ValueError:
    return "Sorry.  Could not convert" + ctemp_str + " to a number."

def milestokm(miles):
  return miles * 1.609344

@app.route("/milestokm/<miles_str>")
def convert_milestokm(miles_str):
  miles = 0.0
  try:
    miles = float(miles_str)
    if miles < 0:
      return "There is no negative distance!"
    km = milestokm(miles)
    return "In miles: " + miles_str + " In kilometers" + str(km)
  except ValueError:
    return "Sorry.  Could not convert" +  miles_str+ " to a number."
    
def flipText(input):
  listInput = []
  listInput[:0] = input
  output = ""
  for i in range(len(listInput)):
    if listInput[i] in flip:
      newChar = flip.get(listInput[i])
      output += newChar
  return output

@app.route("/flipText/<input_str>")
def convert_flipText(input_str):
  return flipText(input_str)

if __name__ == "__main__":
   app.run(host='0.0.0.0')
