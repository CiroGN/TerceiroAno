import { Stack } from "expo-router";
import { PaperProvider } from "react-native-paper";
import CustomLightTheme from './theme'

export default function RootLayout() {
  return (
    <PaperProvider theme={CustomLightTheme}>
      <Stack>
        <Stack.Screen name='index' options={{title:'Paper'}}/>
      </Stack>
    </PaperProvider>
  );
}
