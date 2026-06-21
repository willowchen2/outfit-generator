import { View, Text, StyleSheet} from 'react-native'

//retreiev edtata using fetch
const wardrobeData=await fetch(
    "http://127.0.0.1:5000/wardrobe/", {
        method:"GET"
    }
);
wardrobeData=wardrobeData.json();
const tops = wardrobeData["wardrobe"].filter(item=>isTop(item)); //list of dictioanries
const bottoms=wardrobeData["wardrobe"].filter(item=>isBott(item));
const isTop= (item)=>{
    return item.label.toLowerCase().includes("blouse") ||item.label.toLowerCase().includes("hoodie") || item.label.toLowerCase().includes("cardigan") || item.label.toLowerCase().includes("shirt") || item.label.toLowerCase().includes("sleeve");
}
const isBott=(item)=>{
    return item.label.toLowerCase().includes("skirt") || item.label.toLowerCase().includes("pant") || item.label.toLowerCase().includes("slacks") || item.label.toLowerCase().includes("shorts");
}

export default function WardrobeScreen(){
    return (
        <View style = {styles.container}>
            <Text>Tops:</Text> //how does .map ensure orderly?
                <div> //why do I need this?
                    {tops.map((item)=>(
                        <div>
                            <image src={item.image}/>
                        </div>
                    ))};
                </div>
            <Text>Pants:</Text>
                <div>
                    {bottoms.map((item)=>(
                        <div>
                            <image src={item.image}/>
                        </div>
                    ))};
                </div>
        </View>
    )
}


const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
})

