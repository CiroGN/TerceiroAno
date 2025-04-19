import Produto from "@/components/Produto";
import { Text, View, StyleSheet } from "react-native";
import { ScrollView } from "react-native-gesture-handler";

export default function Index() {
  return (
    <ScrollView>
      <Text style={styles.titulosite}>Loja Site Itens</Text>
      <View  
        style={{
          flexWrap:"wrap",
          flexDirection:"row",
        }}>
        <Produto/>
        <Produto/>
        <Produto/>
        <Produto/>
      </View>
      
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  titulosite:{fontSize:50, alignSelf:"center"}
})