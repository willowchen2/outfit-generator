import { View, Text, StyleSheet } from 'react-native'
import React, {useRef, useState, useCallBack} from 'react';


const [selectedWeather, setSelectedWeather]=useRef(null);
const [selectedOccasion, setSelectedOccasion]=useRef(null);
const [selectedColor, setSelectedColor]=useRef(null);

const [weatherReady, setWeatherReadyToSelect]=useRef(false);
const [occasionReady, setOccasionReadyToSelect]=useRef(false);
const [colorReady, setColorReadyToSelect]=useRef(false);

export default function OutfitScreen() {
    return(
        <View style = {styles.container}>
            <div>
                <button onClick={()=>setWeatherReadyToSelect(true)}>Weather ▾</button>
                {weatherReady && (
                    <ul className="dropdown">
                        <li onClick={()=>setSelectedWeather("sunny")}>Sunny</li>
                        <li onClick={()=>setSelectedWeather("cold")}>Cold</li>
                        <li onClick={()=>setSelectedWeather("warm")}>Warm</li>
                        <li onClick={()=>setSelectedWeather("windy")}>Windy</li>
                        <li onClick={()=>setSelectedWeather("rainy")}>Rainy</li>
                        <li onClick={()=>setSelectedWeather("humid")}>Humid</li>
                    </ul>
                )}
            </div>
            <div>
                <button onClick={()=>setOccasionReadyToSelect(true)}>Occasion ▾</button>
                {occasionReady && (
                    <ul className="dropdown">
                        <li onClick={()=>setSelectedOccasion("casual")}>casual</li>
                        <li onClick={()=>setSelectedOccasion("outdoors")}>outdoors</li>
                        <li onClick={()=>setSelectedOccasion("street-fashion")}>street-fashion</li>
                        <li onClick={()=>setSelectedOccasion("black-tie")}>black-tie</li>
                        <li onClick={()=>setSelectedOccasion("cocktail")}>cocktail</li>
                        <li onClick={()=>setSelectedOccasion("minimalist")}>minimalist</li>
                        <li onClick={()=>setSelectedOccasion("vintage")}>vintage</li>
                    </ul>
                )}
            </div>
            <div>
                <button onClick={()=>setColorReadyToSelect(true)}>Color ▾</button>
                {colorReady && (
                    <ul className="dropdown">
                        <li onClick={()=>setSelectedColor("red")}>red</li>
                        <li onClick={()=>setSelectedColor("orange")}>orange</li>
                        <li onClick={()=>setSelectedColor("yellow")}>yellow</li>
                        <li onClick={()=>setSelectedColor("green")}>green</li>
                        <li onClick={()=>setSelectedColor("violet")}>violet</li>
                        <li onClick={()=>setSelectedColor("blue")}>blue</li>
                    </ul>
                )}
            </div>

            <button onClick={generateOutfit}>Generate Outfit</button>
            <button onClick={makeOutfit}>Make Your Own</button>
        </View>
    )
}

const aiOutfits=async ()=>{
    await fetch(
        "http://127.0.0.1:5000/wardrobe/outfit/", {
            method:"GET",
            body: {
                "weather": selectedWeather,
                "occasion": selectedOccasion,
                "color": selectedColor //another comma?
            },
        }
    );
};

const pieceByID=async (id)=>{
    await fetch(
        "http://127.0.0.1:5000/wardrobe/"+id, {
            method:"GET",
        }
    );
};

function generateOutfit(){
    const outfits=aiOutfits;
    outfits.forEach(outfit=> {
        <div>
            <image src={pieceByID(outfit["items"][0]).image}/>;
            <image src={pieceByID(outfit["items"][1]).image}/>;
            <Text>{outfit["desciption"]}</Text>;
        </div>
    });
}


const [selectedTop, setSelectedTop]=useRef(null);
const [selectedBottom, setSelectedBottom]=useRef(null);

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
function makeOutfit(){
    return (
        <View style = {styles.container}>
            <Text>Tops:</Text>
                <div>
                    {tops.map((item)=>(
                        <button onClick={afterSelectingTop(item)}>
                            <image src={item.image} style={{ border: '5px solid white' }}/>
                        </button>
                    ))};
                </div>
        </View>
    )
}

function afterSelectingTop(top){ //dispaly selecetd image with red border
    setSelectedTop(top);
    return (
        <View>
            <Text>Pants:</Text>
                    <div>
                        {bottoms.map((item)=>(
                            <button onclick={afterSelectingBottom(item)}>
                                <image src={item.image} style={{ border: '5px solid white' }}/>
                            </button>
                        ))};
                    </div>
        </View>
    )
}

function afterSelectingBottom(bottom){
    setSelectedBottom(bottom);
    return (
        <div>
            <image src={selectedTop.image}/>
            <image src={selectedBottom.image}/>
        </div>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
})
