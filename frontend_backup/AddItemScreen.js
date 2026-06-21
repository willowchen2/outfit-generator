import { View, Text, StyleSheet} from 'react-native'
import Webcam from 'react-webcam';
import React, {useRef, useState, useCallBack} from 'react';


/***export default function AddItemScreen() {
    return (
        <View style = {styles.container}>
            <Text>Camera</Text>
        </View>
    )
}***/

const [capturedPhoto,setCapturedPhoto] = useState(null);
const [isCameraOpen, setIsCameraOpen] = useState(false);

webcamRef=useRef(null)
//setup camera stream and lsiten to it
//when user presses camera button, capture the photo
//close buttonQA
export default function CameraPopUp(){
    <div>
        <Webcam
            audio={false}
            ref={webcamRef} //????
            screenshotFormat="image/jpeg" //save as a  jpeg image
            width="100%"
        />
        <button> //click
            onclick={capturePhoto} //what do these curly braces mean
        </button>
        <button> //exit
            onclick={setIsCameraOpen(false)}
        </button>
    </div>


}


capturePhoto=useCallBack(()=>{
   const photo=webcamRef.current.getScreenShot(); //what si webcamref and what is .current?
    setCapturedPhoto(photo);
    setIsCameraOpen(false);
    uploadImage();
}, )


const uploadImage=async ()=>{
    await fetch(
        "http://127.0.0.1:5000/wardrobe/", {
            method:"POST",
            body: binaryData,
            headers: {
                'Content-Type': capturedPhoto,
            },
        }
    );
};


const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems:'center',
        justifyContent: 'center',
    },
})










//Info
//callbac fucntion: does not rerun evevry time react reloads
//useState:  triggers rerender
