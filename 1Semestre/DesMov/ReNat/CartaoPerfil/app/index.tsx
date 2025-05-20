import { Text, View, StyleSheet, Image, ScrollView } from "react-native";

export default function Index() {
  return (
    <ScrollView>
      <View style={styles.tudo}>
        <View style={styles.card}>
          <Image
            source={{uri:'https://thispersondoesnotexist.com'}}
            style={styles.imagem}
          />
          <Text style={styles.nome}>Ciro Guilherme Nass</Text>
          <Text style={styles.email}>ciroguilhermenass@gmail.com</Text>
          <Text style={styles.descricao}>Estudante de BCC, do IFPR campus pinhais!</Text>
        </View>
        <View style={styles.card}>
          <Image
            source={{uri:'https://thispersondoesnotexist.com'}}
            style={styles.imagem}
          />
          <Text style={styles.nome}>Ciro Guilherme Nass</Text>
          <Text style={styles.email}>ciroguilhermenass@gmail.com</Text>
          <Text style={styles.descricao}>Estudante de BCC, do IFPR campus pinhais!</Text>
        </View>
        <View style={styles.card}>
          <Image
            source={{uri:'https://thispersondoesnotexist.com'}}
            style={styles.imagem}
          />
          <Text style={styles.nome}>Ciro Guilherme Nass</Text>
          <Text style={styles.email}>ciroguilhermenass@gmail.com</Text>
          <Text style={styles.descricao}>Estudante de BCC, do IFPR campus pinhais!</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  tudo:{
    flex:1,
    flexWrap:"wrap",
    flexDirection:"row",
  },
  card:{
    backgroundColor:"lightgrey",
    width:300,
    marginInline:"auto",
    marginBlock:10,
    gap:10,
    borderWidth: 2,
    padding:15 ,
    borderRadius:20
    },
  imagem:{width:200, height:200, borderRadius:50, alignSelf:"center"},
  nome:{ fontSize: 30, fontWeight: "bold" },
  email: { fontWeight:"100"},
  descricao: {fontStyle:"italic"}
});