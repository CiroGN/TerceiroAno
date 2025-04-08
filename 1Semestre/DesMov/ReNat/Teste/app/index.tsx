import { Text, View, Image, StyleSheet } from "react-native";

export default function Index(){
  return(
    <View>
      <Image
        source={{ uri: "https://reactnative.dev/img/tiny_logo.png"}}
        style={estilo.imagem}
      />
      {/* Primeira View Interna*/}
      <View>
        <Text style={estilo.titulo}>Título</Text>
        <Text style={estilo.subtitulo}>Subtítulo</Text>
      </View>
    {/* Segunda View Interna*/}
      <View>
        <Text style={estilo.textos}>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Impedit nostrum modi molestiae tenetur odio, nobis maxime qui vitae in nesciunt minus velit dolores illo et architecto atque asperiores voluptatem commodi?</Text>
        <Text style={estilo.textos}>Lorem ipsum dolor sit amet consectetur adipisicing elit. Molestias accusantium animi sed nemo dolor obcaecati exercitationem cum mollitia reiciendis debitis, provident quas blanditiis ducimus, incidunt ipsum, beatae dolores repellendus excepturi.</Text>
      </View>
    </View>
  );
}

const estilo = StyleSheet.create({
  imagem: {width:100, height:100, borderRadius: 100, alignSelf: "center"},
  titulo: {margin: 10, color: "red", fontSize:40, alignSelf: "flex-start"},
  subtitulo: {margin:10, marginTop:10, paddingBottom:10, fontSize: 30, alignSelf: "auto"},
  textos: {fontSize: 20, textAlign: "justify", padding:10, borderWidth:3, borderRadius:10, marginBottom:10, backgroundColor:"lightgray"},

})