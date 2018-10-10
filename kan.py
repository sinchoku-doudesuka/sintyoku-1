from pyzbar.pyzbar import decode
import cv2
import requests

data = None

capture = cv2.VideoCapture(0)

while not data:

    ret, image = capture.read()

    if ret == True:
        # QRコードの読取り
        data = decode(image)

    image = cv2.flip(image,1)

    cv2.imshow('QRcodeReader', image)

    if cv2.waitKey(1) >= 0:
        break

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
	"waitTime":"1"
}

r=requests.post('https://securl.nu/jx/get_page_jx.php',data=payload)

hash=r.json()



try:
	result=hash['viruses'][0]['type']

except IndexError:
	print("safe")

except KeyError:
        print("site not found")
else:
	print("---warning---")
	print("This site include marware!!")
	print(result)
