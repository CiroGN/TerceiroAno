import { linkTo } from "expo-router/build/global-state/routing";
import { useState } from "react";
import { View } from "react-native";
import { Text, TextInput, Button, Snackbar } from 'react-native-paper';

export default function Index() {
  const [nomeusuario, setNomeUsuario] = useState("");
  const [senha, setSenha] = useState("");

  const [visible, setVisible] = useState(false);
  const onToggleSnackBar = () => setVisible(!visible);
  const onDismissSnackBar = () => setVisible(false);
  
  return (
    <View style={{flex: 1, gap: 25, marginLeft: 50, marginRight: 50, marginTop: 20}}>   
        <Text style={{textAlign: "center"}} variant="displayMedium">Login</Text>
        <TextInput
          label="Usuário"
          value={nomeusuario}
          onChangeText={texto => setNomeUsuario(texto)}
        />
        <TextInput
          label="Senha"
          value={senha}
          onChangeText={text => setSenha(text)}
          secureTextEntry={true}
        />
        <Button icon="lock" mode="contained" onPress={onToggleSnackBar}>
          Acessar
        </Button>

        <Snackbar
          visible={visible}
          onDismiss={onDismissSnackBar}
          action={{
            label: 'Fechar',
            onPress: () => {
              onToggleSnackBar
            },
          }}>
          Aguarde. Processando login...
        </Snackbar>

        <Button onPress={()=>{linkTo:"/card"}}>
          Card
        </Button>

    </View>
  );
}
