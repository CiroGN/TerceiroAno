import { Image, StyleSheet, Text, View } from 'react-native';
export default function CardPais(props: any) {
    return (
        <View style={styles.container}>
            <View>
                <Image style={styles.bandeira} source={{ uri: props.conteudo.bandeira }} />
            </View>
            <View style={styles.infoContainer}>
                <Text style={styles.title}>{props.conteudo.nome}</Text>
                <Text style={styles.info}>Capital: {props.conteudo.capital}</Text>
                <Text style={styles.info}>População: {props.conteudo.populacao} habitantes</Text>
                <Text style={styles.info}>Idioma: {props.conteudo.idioma}</Text>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        padding:10,
        marginBlock:10,
        flexDirection:'row',
        alignItems:"center",
    },
    title: {
        fontSize:30,
        fontWeight:'900',
    },
    info: {
    },
    bandeira: {
        height:100,
        width: 140,
        marginRight:10
    },
    infoContainer:{
        flex:1,
    }
});
