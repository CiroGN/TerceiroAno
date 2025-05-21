import Biscoito from '@/components/Biscoito';
import React, { useState } from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';

const frases = [
  'Não é que eu tenha medo de morrer. É que eu não quero estar lá na hora que isso acontecer.',
  'Era um menino tão mau que só se tornou radiologista para ver a caveira dos outros.',
  'O dinheiro não é tudo. Não se esqueça também do ouro, dos diamantes, da platina e das propriedades.',
  'Seja a pessoa que seu cachorro acredita que você é!',
  'Seja tão confiante a ponto de ter a certeza que o seu espelho está agradecido de te ver todas manhãs.'
];

export default function App() {
  const [frase, setFrase] = useState('');
  const [biscoitoQuebrado, setBiscoitoQuebrado] = useState(false);

  const quebrarBiscoito = () => {
    const indice = Math.floor(Math.random() * frases.length);
    setFrase(frases[indice]);
    setBiscoitoQuebrado(true);
  };

  const reiniciar = () => {
    setFrase('');
    setBiscoitoQuebrado(false);
  };

  return (
    <View style={styles.container}>
      <Biscoito
        quebrado={biscoitoQuebrado}
        frase={frase}
      />

      <TouchableOpacity style={styles.botao} onPress={quebrarBiscoito}>
        <Text style={styles.textoBotao}>Quebrar o Biscoito</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.botao} onPress={reiniciar}>
        <Text style={styles.textoBotao}>Recomeçar</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFF8DC',
    alignItems: 'center',
    justifyContent: 'center',
  },
  botao: {
    backgroundColor: '#DAA520',
    padding: 10,
    marginTop: 20,
    borderRadius: 10,
  },
  textoBotao: {
    color: '#fff',
    fontWeight: 'bold',
  },
});
