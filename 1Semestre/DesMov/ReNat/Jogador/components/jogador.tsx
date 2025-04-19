import {Text, View, StyleSheet, Image} from "react-native";

export default function Jogador(props:any){
    const styles = StyleSheet.create({
        container:{
            backgroundColor: props.corDeFundo,
            borderRadius: 10,
            borderWidth:3,
            width:200,
            alignSelf:"center",
            alignItems:"center",
            margin:10,
            padding:15,
        },
        nome:{fontSize:20, color:props.corDeTexto},
        idade:{fontSize:15, color:props.corDeTexto},
        time:{fontSize:20,paddingTop:3, color:props.corDeTexto},
        foto:{width:100, height:100, backgroundColor:'white', borderRadius:100, marginBottom:10, borderWidth:5}
    });
    return (
        <View style={styles.container}>
            <Image
                style={styles.foto}
                source={{uri: props.foto}}
            />
            <Text style={styles.nome}>Nome: {props.nome}</Text>
            <Text style={styles.idade}>Idade: {props.idade} anos</Text>
            <Text style={styles.time}>Time: {props.time}</Text>
        </View>
        
    );
}
