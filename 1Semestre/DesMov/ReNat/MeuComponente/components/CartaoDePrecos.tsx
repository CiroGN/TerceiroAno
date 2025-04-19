import { View, Text, StyleSheet, Image, TouchableOpacity } from "react-native";

export default function CartaoDePrecos(){
    return(
        <View style={styles.tudo}>
            <Image
                source={{uri:'https://i.pravatar.cc/200'}}
                style={styles.imagem}
            />
            <Text style={styles.nome}>Ciro Guilherme Nass</Text>
            <Text style={styles.email}>ciroguilhermenass@gmail.com</Text>
            <Text style={styles.descricao}>Estudante de BCC, do IFPR campus pinhais!</Text>
            <TouchableOpacity style={styles.botao}><Text style={{fontSize:25, color:'white'}}>Saiba Mais</Text></TouchableOpacity> 
      </View>
    );
}

const styles = StyleSheet.create({
    tudo:{
      backgroundColor:"lightgrey",
      width:"auto",
      marginInline:20,
      marginBlock:5,
      gap:10,
      justifyContent:"flex-start",
      alignItems:"center",
      borderWidth: 0,
      padding:15 ,
      borderRadius:20
      },
    botao:{borderRadius:5, backgroundColor: 'grey', paddingInline:8},
    imagem:{width:200, height:200, borderRadius:100},
    nome:{ fontSize: 30, fontWeight: "bold" },
    email: { fontWeight:"100"},
    descricao: {fontStyle:"italic"}
  });