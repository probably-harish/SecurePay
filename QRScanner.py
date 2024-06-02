import cv2
from pyzbar import pyzbar

def scan_qr_code():
    camera = cv2.VideoCapture(0)
    
    while True:
        _, frame = camera.read()
        decoded_objects = pyzbar.decode(frame)
        
        for obj in decoded_objects:
            print('Data:', obj.data.decode())
        
        cv2.imshow("QR Code Scanner", frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    camera.release()
    cv2.destroyAllWindows()

scan_qr_code()
