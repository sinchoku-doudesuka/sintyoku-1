from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import requests
import webbrowser
import tkinter
import tkinter.filedialog
import sys

data = None

capture = cv2.VideoCapture(0)

while not data:

    ret, image = capture.read()

    image = cv2.flip(image,1)

    cv2.imshow('QRcodeReader', image)

    image = cv2.flip(image,1)

    if cv2.waitKey(1) >= 0:
        # GUIでファイル読み込み
        show = tkinter.Tk()
        show.withdraw()
        image = Image.open(tkinter.filedialog.askopenfilename(filetypes=[('image files','*.png')]))
        show.destroy()
        ret = True

    if ret == True:
        # QRコードの読取り
        data = decode(image)

capture.release()
cv2.destroyAllWindows()

#デバック用プリント            
print(data[0][0].decode('utf-8', 'ignore'))

URL=data[0][0].decode('utf-8', 'ignore')

if not  URL.count('http'):
    URL='http://'+URL
    print(URL)

payload={
	"browserHeight":"683",
	"browserWidth":"1138",
	"url":URL,
	"waitTime":"0"
}

r=requests.post('https://securl.nu/jx/get_page_jx.php',data=payload)

hash=r.json()

try:
        result=hash['viruses'][0]['type']

except KeyError:
        print("URL not found")
        sys.exit()

except IndexError:
        print("check marware")
        print("virus not included")

else:
        print("check marware")
        print("---warning---")
        print("This site includes marware!!")
        print(result)

print("check fishing")
try:
        result=hash['blackList'][0]['type']

except IndexError:
        print("safty site")
        webbrowser.open(URL)

else:
        print("---warning---")
        print("This site is fishing site!!")
        print(result)
