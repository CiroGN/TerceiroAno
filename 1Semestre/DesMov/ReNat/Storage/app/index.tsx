import AsyncStorage from '@react-native-async-storage/async-storage'
import { useEffect, useState } from "react";
import { StyleSheet, Text, TextInput, View } from "react-native";

export default function Index() {

  const styles = StyleSheet.create({
    container: {
    flexDirection: 'column',
    padding: 10,
    gap: 10
  },
  input: {
    borderStyle: 'solid',
    borderWidth: 2,
    fontSize: 20
  },
  texto: {
    fontSize: 18
  }
  })

  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [telefone, setTelefone] = useState("");

  function atualizarConteudoNome(nome:string){
    setNome(nome);
    storeDataNome(nome);
  } 
  function atualizarConteudoEmail(email:string){
    setEmail(email);
    storeDataEmail(email);
  } 
  function atualizarConteudoTelefone(telefone:string){
    setTelefone(telefone);
    storeDataTelefone(telefone);
  } 

  const getData = async () => {
    getDataNome();
    getDataEmail();
    getDataTelefone();
  }

  const getDataNome = async () => {
    
    try{
      const jsonValueNome = await AsyncStorage.getItem('my-key-nome');

      if(jsonValueNome != null){
        setNome(JSON.parse(jsonValueNome));
      }
    } catch (e){
    console.log(e);
    } 
  }
  const getDataEmail = async () => {
    
    try{
      const jsonValueEmail = await AsyncStorage.getItem('my-key-email');

      if (jsonValueEmail != null){
        setEmail(JSON.parse(jsonValueEmail));
      }
    } catch (e){
    console.log(e);
    } 
  }
  const getDataTelefone = async () => {
    
    try{
      const jsonValueTelefone = await AsyncStorage.getItem('my-key-telefone');

      if (jsonValueTelefone != null){
        setTelefone(JSON.parse(jsonValueTelefone));
      }
    } catch (e){
    console.log(e);
    } 
  }

  const storeDataNome = async (nome:any) => {
    try {
      const jsonValueNome = JSON.stringify(nome);
      await AsyncStorage.setItem('my-key-nome', jsonValueNome)
    } catch (e) {
      console.log(e);
    }
  };

  const storeDataEmail = async (email:any) => {
    try {
      const jsonValueEmail = JSON.stringify(email);
      await AsyncStorage.setItem('my-key-email', jsonValueEmail)
    } catch (e) {
      console.log(e);
    }
  };

  const storeDataTelefone = async (telefone:any) => {
    try {
      const jsonValueTelefone = JSON.stringify(telefone);
      await AsyncStorage.setItem('my-key-telefone', jsonValueTelefone)
    } catch (e) {
      console.log(e);
    }
  };
  useEffect(() => {
    getData();
  }, []);
  return (
    <View
      style={styles.container}
    >
      <TextInput
        style={styles.input}
        onChangeText={(nome) => atualizarConteudoNome(nome)}
        value={nome}
        placeholder="Digite seu nome aqui"
      />
      <TextInput
        style={styles.input}
        onChangeText={(email) => atualizarConteudoEmail(email)}
        value={email}
        placeholder="Digite seu email aqui"
      />
      <TextInput
        style={styles.input}
        onChangeText={(telefone) => atualizarConteudoTelefone(telefone)}
        value={telefone}
        placeholder="Digite seu telefone aqui"
      />
      <Text>O que está salvo no dispositivo?.</Text>
      <Text style={styles.texto}>{nome}</Text>
      <Text style={styles.texto}>{email}</Text>
      <Text style={styles.texto}>{telefone}</Text>
    </View>
  );
}

