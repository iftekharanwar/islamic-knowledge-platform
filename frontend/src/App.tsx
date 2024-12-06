import { ChakraProvider, Box, Container, extendTheme } from '@chakra-ui/react';
import Header from './components/layout/Header';
import ChatInterface from './components/ChatBot/ChatInterface';

const theme = extendTheme({
  styles: {
    global: {
      body: {
        bg: 'gray.50',
      },
    },
  },
  breakpoints: {
    sm: '320px',
    md: '768px',
    lg: '960px',
    xl: '1200px',
  },
  components: {
    Container: {
      baseStyle: {
        maxW: { base: '100%', md: 'container.xl' },
        px: { base: 4, md: 6 },
      },
    },
  },
});

function App() {
  return (
    <ChakraProvider theme={theme}>
      <Box minH="100vh" display="flex" flexDirection="column">
        <Header />
        <Container
          flex="1"
          py={{ base: 4, md: 8 }}
          px={{ base: 2, md: 4 }}
          maxW={{ base: '100%', md: 'container.xl' }}
        >
          <ChatInterface />
        </Container>
      </Box>
    </ChakraProvider>
  );
}

export default App;
