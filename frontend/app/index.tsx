import { Text, View } from "react-native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import CameraPopUp from "./screens/AddItemScreen.js"
import OutfitScreen from "./screens/OutfitScreen.js"
import WardrobeScreen from "./screens/WardrobeScreen.js"


const Tab=createBottomTabNavigator();
const BottomTab=()=>{
  return (
    <Tab.Navigator>
      <Tab.Screen name="Add" component= {CameraPopUp}/>
      <Tab.Screen name="Wardrobe" component= {OutfitScreen}/>
      <Tab.Screen name="Outfit" component= {WardrobeScreen}/>
    </Tab.Navigator>
  );
};

export default BottomTab;

//create pages and below bar

