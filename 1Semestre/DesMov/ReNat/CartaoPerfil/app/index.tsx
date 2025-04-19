import { Text, View, StyleSheet, Image } from "react-native";

export default function Index() {
  return (
    <View>
      <View style={styles.tudo}>
        <Image
          source={{uri:'https://thispersondoesnotexist.com'}}
          style={styles.imagem}
        />
        <Text style={styles.nome}>Ciro Guilherme Nass</Text>
        <Text style={styles.email}>ciroguilhermenass@gmail.com</Text>
        <Text style={styles.descricao}>Estudante de BCC, do IFPR campus pinhais!</Text>
      </View>
      <View style={styles.tudo}>
        <Image
          source={{uri:'https://thispersondoesnotexist.com'}}
          style={styles.imagem}
        />
        <Text style={styles.nome}>Ciro Guilherme Nass</Text>
        <Text style={styles.email}>ciroguilhermenass@gmail.com</Text>
        <Text style={styles.descricao}>Estudante de BCC, do IFPR campus pinhais!</Text>
      </View>
      <View style={styles.tudo}>
        <Image
          source={{uri:'https://thispersondoesnotexist.com'}}
          style={styles.imagem}
        />
        <Text style={styles.nome}>Ciro Guilherme Nass</Text>
        <Text style={styles.email}>ciroguilhermenass@gmail.com</Text>
        <Text style={styles.descricao}>Estudante de BCC, do IFPR campus pinhais!</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  tudo:{
    backgroundColor:"lightgrey",
    width:"auto",
    marginInline:50,
    marginBlock:20,
    gap:10,
    justifyContent:"flex-start",
    alignItems:"flex-start",
    borderWidth: 2,
    padding:15 ,
    borderRadius:20
    },
  imagem:{width:200, height:200, borderRadius:50},
  nome:{ fontSize: 30, fontWeight: "bold" },
  email: { fontWeight:"100"},
  descricao: {fontStyle:"italic"}
});