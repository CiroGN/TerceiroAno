import {Text, View, StyleSheet} from "react-native"

export default function Time(props:any){
    const styles = StyleSheet.create({
        container:{
            flexDirection:"row",
        },
        retangulo1:{backgroundColor: props.corDeFundo, height:40, width:20, borderWidth:3, borderRightWidth:0},
        retangulo2:{backgroundColor: props.corDeTexto, height:40, width:20, borderWidth:3, borderRightWidth:0},
        retangulo3:{height:40, width:100, borderWidth:3},
        time:{ alignItems:"center", alignSelf:"center", fontSize:25, fontWeight:"500"},
    });
    return(
        <View style={styles.container}>
            <View style={styles.retangulo1}>

            </View>
            <View style={styles.retangulo2}>

            </View>
            <View style={styles.retangulo3}>
                <Text style={styles.time}>{props.time}</Text>
            </View>
        </View>
            
    );
}