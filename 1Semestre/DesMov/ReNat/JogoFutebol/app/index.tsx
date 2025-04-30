import { useState } from "react";
import { Text, View, StyleSheet, TouchableOpacity } from "react-native";
import Ionicons from '@expo/vector-icons/Ionicons';
import { useFonts } from 'expo-font';
import { BebasNeue_400Regular } from '@expo-google-fonts/bebas-neue'

export default function Index() {

  const [fontsLoaded] = useFonts({
    BebasNeue_400Regular,
  })
  const [contador, setContador] = useState(0);
  const [contador2, setContador2] = useState(0);

  function atualizarContagemCasa(){
    setContador(contador+1);
  }

  function resetarContagem(){
    setContador(0);
    setContador2(0);
  }
  function atualizarContagemVisitante(){
    setContador2(contador2+1);
  }


  const styles=StyleSheet.create({
    container:{flex:1, justifyContent:"center", alignItems:"center", gap:10},
    contador:{fontSize:30},
    botao:{padding:15, borderWidth:1, width:200, backgroundColor:'blue', borderRadius:14},
    botao2:{padding:15, borderWidth:1, width:200, backgroundColor:'blue', borderRadius:14},
    textoBotao:{color:'white', fontSize:30, textAlign:"center"},
    textoBotao2:{color:'white', fontSize:30, textAlign:"center"},
    titulo:{fontFamily:'BebasNeue_400Regular', fontSize:50}
  })
  return (
    <View style={styles.container}>
      <Text><Ionicons name="football" size={60} color="black" /></Text>
      <Text style={styles.titulo}>Placar Eletronico</Text>
      <Text style={styles.contador}>Time da Casa: {contador}</Text>
      <Text style={styles.contador}>Time Visitante: {contador2}</Text>
      <TouchableOpacity style={styles.botao} onPress={atualizarContagemCasa}>
        <Text style={styles.textoBotao}>Gol Time da Casa</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.botao2} onPress={atualizarContagemVisitante}>
        <Text style={styles.textoBotao2}>Gol Time Visitante</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.botao2} onPress={resetarContagem}>
        <Text style={styles.textoBotao2}>Reiniciar</Text>
      </TouchableOpacity>
    </View>
  );
}