import { View, Text, StyleSheet, Image, TouchableOpacity } from "react-native";

export default function Produto(){
    return(
        <View style={styles.tudo}>
            <View>
                <Text style={styles.titulo}>Nome do Produto</Text>
            </View>
            <Image
                source={{uri:"https://www.google.com/imgres?q=imagem&imgurl=http%3A%2F%2Fwww.ccs.ufpb.br%2Flqf%2Fcontents%2Fimagens%2Ffoto-1.jpg%2F%40%40images%2Fimage.jpeg&imgrefurl=http%3A%2F%2Fwww.ccs.ufpb.br%2Flqf%2Fcontents%2Fimagens%2Ffoto-1.jpg%2Fimage_view_fullscreen&docid=gcRMP9NdejdlkM&tbnid=VfwOIrTFEwT9HM&vet=12ahUKEwjireenrdaMAxWPFLkGHShPPHIQM3oECG0QAA..i&w=670&h=440&hcb=2&ved=2ahUKEwjireenrdaMAxWPFLkGHShPPHIQM3oECG0QAA"}}
                style={styles.image}
            />
            <View>
                <Text style={styles.descricao}>Descrição do item a ser vendido, como a utilidade, confexção, cor, tamanho, etc...</Text>
                <Text style={styles.preco}>Preco de venda, exemplo R$ 1.500,00</Text>
                <TouchableOpacity style={styles.botao}><Text style={{fontSize:25, color:'white'}}>Comprar</Text></TouchableOpacity>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    tudo: {
        backgroundColor:"lightgrey",
        width:300,
        gap:10,
        margin:"auto",
        marginBlock:20,
        justifyContent:"center",
        alignItems:"center",
        alignContent:"center",
        alignSelf:"center",
        borderWidth: 0,
        padding:15 ,
        borderRadius:20},
    image:{width: 200, height:200, borderRadius:100},
    botao:{
        borderRadius:5,
        backgroundColor: 'grey', 
        paddingInline:8, 
        paddingBottom:3, 
        maxWidth:140,
        alignSelf:"center"
    },
    titulo:{fontSize:30, textDecorationLine:"underline"},
    descricao:{marginTop:10, marginInline:10, borderWidth:1, paddingInline:3},
    preco:{marginBlock:5, paddingHorizontal:10},
}) 