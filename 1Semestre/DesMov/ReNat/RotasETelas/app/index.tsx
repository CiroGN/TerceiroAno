import { Link, router } from 'expo-router';
import { Text, TouchableOpacity, View } from "react-native";
import { styles } from './styles';

export default function Index() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text>Página inicial</Text>

      <Link style={styles.button} href="/(tabs)/cliente">
        <Text>Meu perfil</Text>
      </Link>

      <Link style={styles.button} href="/produto">
        <Text>Ir para produto</Text>
      </Link>

      <Link style={styles.button} href="/cliente">
        <Text>Ir para cliente</Text>
      </Link>
      
      <TouchableOpacity onPress={ ()=> router.push('/sobre')}>
        <Text style={styles.button}>Sobre nós!</Text>
      </TouchableOpacity>

    </View>
  );
}
