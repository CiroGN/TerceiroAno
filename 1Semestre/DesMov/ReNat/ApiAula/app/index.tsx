import { Text, View } from "react-native";
import axios from "axios";
import { useEffect, useState } from "react";
import { FlatList, SafeAreaView, StyleSheet } from "react-native";
import CardPais from "@/components/CardPais";

export default function Index() {

  const [paises, setPaises] = useState<any[]>([])
  
  const api = axios.create({
    baseURL: "https://smartprova.com.br/"
  })

  useEffect(() =>{
    async function consultarAPI(){
      const response = await api.get("api-testes/paises");
      setPaises(response.data);
    }
    consultarAPI();
  }, []);

  const style = StyleSheet.create({
    container:{},
  })

  return (
    <SafeAreaView style={style.container}>
      <FlatList
        data={paises}
        renderItem={({item}) => <CardPais conteudo={item}></CardPais>}
      />
    </SafeAreaView>
  );
}
