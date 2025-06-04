import { Tabs } from 'expo-router';
import { Feather } from '@expo/vector-icons';

export default function TabsLayout(){
    return(
        <Tabs>
            <Tabs.Screen 
                name="cliente" 
                options={{title: 'Perfil',
                    tabBarIcon: ({color, size}) => {
                        return(
                            <Feather
                                name="user"
                                size={size}
                                color={color}
                            />
                        );
                    }
                }}
            />
            <Tabs.Screen 
                name="endereco" 
                options={{title: 'Endereços',
                    tabBarIcon: ({color, size}) => {
                            return(
                                <Feather
                                    name="map-pin"
                                    size={size}
                                    color={color}
                                />
                            );
                        }
                }}
            />
            <Tabs.Screen 
                name="compras" 
                options={{title: 'Minhas compras',
                    tabBarIcon: ({color, size}) => {
                            return(
                                <Feather
                                    name="shopping-cart"
                                    size={size}
                                    color={color}
                                />
                            );
                        }
                }}
            />
        </Tabs>
    );
} 