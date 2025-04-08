import { Text, View } from "react-native";

export default function Index() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text style={{fontSize: 50, color: "#0", backgroundColor: "yellow"}}>Hello World</Text>
      <Text style={{fontSize: 35, color: "rgb(135, 16, 219)", backgroundColor:"#123456"}}>Eu sou um App</Text>
      <Text style={{fontSize: 20}}>Fui criado em React</Text>
    </View>
  );
}
