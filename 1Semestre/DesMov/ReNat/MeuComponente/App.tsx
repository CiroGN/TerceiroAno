import { StyleSheet, Text, View } from 'react-native';
import CartaoDePrecos from './components/CartaoDePrecos';

export default function App() {
  return (
    <View style={styles.container}>
      <CartaoDePrecos/>
      <CartaoDePrecos/>
      <CartaoDePrecos/>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    margin:10,
  },
});
