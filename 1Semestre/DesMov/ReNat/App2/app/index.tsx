import { Text, View } from "react-native";

export default function Index() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        margin: 5,
      }}
    >
      <Text style={{fontSize: 50}}>Título</Text>
      <h1 style={{fontSize: 30}}>Coisas legais</h1>
      <li>
        <p>Coisa</p>
        <p>Coisa</p>
        <p>Coisa</p>
        <p>Coisa</p>
      </li>
      <h2>Mais coisas legais</h2>
      <li>
        <Text>Coisa</Text>
        <Text>Coisa</Text>
        <Text>Coisa</Text>
        <Text>Coisa</Text>
      </li>

      <h3 style={{fontSize: 60}}>Estmaos aqui</h3>
      <Text>Contatos</Text>
      <li style={{alignItems: "center", justifyContent: "center", alignContent:"center", display: "contents"}}>
        <p>telefone</p>
        <p>celular</p>
        <p>email</p>
        <p>coisa</p>
      </li>
    </View>
  );
}
