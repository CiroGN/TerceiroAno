import { Link } from "expo-router";
import { Text, View } from "react-native";

export default function Cliente() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text>
        Página Cliente
      </Text>

        <Link href="/produto">
          <Text>Ir para produto</Text>
        </Link>
        <Link href="/sobre">
          <Text>Ir para cliente</Text>
        </Link>
      
    </View>
  );
}
