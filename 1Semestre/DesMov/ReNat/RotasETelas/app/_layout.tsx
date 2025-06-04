import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen 
        name="(tabs)" options={{
        title: 'Área do Cliente'
        }}
      />

      <Stack.Screen 
        name="detalhes/[id]" options={{
        title: 'Detalhes'
        }}
      />  

      <Stack.Screen 
        name="index"
        options={{ title: 'Home', headerShown: false }}
      />
      <Stack.Screen 
        name="produto" 
        options={{ 
          title: 'Página de Produtos',
          headerStyle:{
            backgroundColor: '#000'
          },
          headerTintColor: '#fff'
        }}
      />
      <Stack.Screen 
        name="cliente" 
        options={{ title: 'Página de Clientes',
        headerStyle: {
          backgroundColor: 'blue'
        },
        headerTintColor: '#fff'  
        }}
      />
      <Stack.Screen name="sobre" options={{ title: 'Página Sobre' }}/>
    </Stack>
  )
}
