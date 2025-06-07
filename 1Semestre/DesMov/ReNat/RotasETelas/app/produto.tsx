import { Link } from "expo-router";
import { Text, View } from "react-native";

export default function Produto() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text>
        Produtos cadastrados
      </Text>

      <Link
        href={{
          pathname: '/detalhes/[id]',
          params: {id: '1'}
        }}>
          <Text>Ver produto 1</Text>
        </Link>
      <Link
        href={{
          pathname: '/detalhes/[id]',
          params: {id: '2'}
        }}>
          <Text>Ver produto 2</Text>
        </Link>
      <Link
        href={{
          pathname: '/detalhes/[id]',
          params: {id: '3'}
        }}>
          <Text>Ver produto 3</Text>
        </Link>
   

    </View>
  );
}
