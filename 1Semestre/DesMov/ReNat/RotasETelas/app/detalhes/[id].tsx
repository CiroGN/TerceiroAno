import { View, Text, StyleSheet } from "react-native";
import { useLocalSearchParams } from "expo-router";

export default function DetalhesProduto(){

    const {id} = useLocalSearchParams();

    const styles=StyleSheet.create({
        container: {
          flex: 1, marginTop: 20,
          alignItems: 'center', 
        },
        titulo: {fontSize: 35, fontWeight: 'bold'},
        texto: {fontSize: 25},
    })

    return(
        <View style={styles.container}>
            <Text style={styles.titulo}>
                Visualuzando produto {id}
            </Text>
        </View>
    );
}
