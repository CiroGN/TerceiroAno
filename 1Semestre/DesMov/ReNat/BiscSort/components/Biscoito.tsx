import React from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';

export default function Biscoito({ quebrado, frase }) {
  const imagem = quebrado
    ? require('../images/biscoitoAberto.png')
    : require('../images/biscoito.png');

  return (
    <View style={styles.container}>
      <Image source={imagem} style={styles.imagem} />
      {frase !== '' && <Text style={styles.frase}>"{frase}"</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
  },
  imagem: {
    width: 250,
    height: 250,
    resizeMode: 'contain',
  },
  frase: {
    marginTop: 20,
    fontStyle: 'italic',
    fontSize: 16,
    textAlign: 'center',
    paddingHorizontal: 20,
  },
});
