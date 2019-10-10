import React from 'react';
import Webcam from "react-webcam";

const videoConstraints = {
    width: 600,
    height: 600,
    facingMode: "user"
};

const b64toBlob = (b64Data, contentType, sliceSize) => {
    contentType = contentType || '';
    sliceSize = sliceSize || 512;
  
    var byteCharacters = atob(b64Data);
    var byteArrays = [];
  
    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
      var slice = byteCharacters.slice(offset, offset + sliceSize);
  
      var byteNumbers = new Array(slice.length);
      for (var i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }
  
      var byteArray = new Uint8Array(byteNumbers);
  
      byteArrays.push(byteArray);
    }
  
    var blob = new Blob(byteArrays, {type: contentType});
    return blob;
}


export default function WebcamCapture() {

    const webcamRef = React.useRef(null);

    const capture = React.useCallback(() => {
        
            // debugger;
            const imageSrc = webcamRef.current.getScreenshot();
            const parts = imageSrc.split(','),
                  type = parts[0].split(';')[0].split(':')[1],
                  base64Data = parts[1];
            var formData = new FormData();
            var imageBlob = b64toBlob(base64Data, type);
            
            formData.append('data','yes');
            formData.append('image', imageBlob, 'image.jpg');

            fetch('http://localhost:5001/', {
                method: 'POST',
                body: formData 
            })
            .then(res => res.json())
            .then(body => console.log(body));
        },
        [webcamRef]
    );

    return (
        <div>
            <Webcam
                audio={false}
                height={720}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width={1280}
                videoConstraints={videoConstraints}
            />
            <button onClick={capture}>Capture photo</button>
        </div>
    )
}
