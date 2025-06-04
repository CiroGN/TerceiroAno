import { Link } from "expo-router";
import { Text, View } from "react-native";

export default function Sobre() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text>
        Página Sobre
      </Text>
      <Link href="/">
        <Text>Ir para Página Inicial</Text>
      </Link>
   
    </View>
  );
}
