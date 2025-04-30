import { useState } from "react";
import { Text, View, StyleSheet, TouchableOpacity } from "react-native";
import { useFonts } from "expo-font"
import { Bangers_400Regular } from '@expo-google-fonts/bangers';
import AntDesign from '@expo/vector-icons/AntDesign';

export default function Index() {

  const [fontsLoaded] = useFonts({Bangers_400Regular})
  const [contador, setContador] = useState(0);

  function atualizarContagem(){
    setContador(contador+1);
  }
  if(contador >= 10 || contador < 0){
    resetarContagem();
    alert("limite alcancado");
  }
  function resetarContagem(){
    setContador(0);
  }
  function diminuirContagem(){
    setContador(contador - 1);
  }


  const styles=StyleSheet.create({
    container:{flex:1, justifyContent:"center", alignItems:"center", gap:10},
    contador:{fontSize:100},
    botao:{padding:15, borderWidth:1, width:200, backgroundColor:'blue', borderRadius:14},
    botao2:{padding:15, borderWidth:1, width:200, backgroundColor:'blue', borderRadius:14},
    textoBotao:{color:'white', fontSize:30, textAlign:"center", fontFamily:"Bangers_400Regular"},
    textoBotao2:{color:'white', fontSize:30, textAlign:"center", fontFamily:"Bangers_400Regular"},
  })
  return (
    <View style={styles.container}>
      <Text style={styles.contador}>{contador}</Text>
      <TouchableOpacity style={styles.botao} onPress={atualizarContagem}>
        <Text style={styles.textoBotao}>Contar <AntDesign name="plus" size={24} color="white" /></Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.botao2} onPress={diminuirContagem}>
        <Text style={styles.textoBotao2}>Descontar <AntDesign name="minus" size={24} color="white" /></Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.botao2} onPress={resetarContagem}>
        <Text style={styles.textoBotao2}>Reiniciar</Text>
      </TouchableOpacity>
    </View>
  );
}
