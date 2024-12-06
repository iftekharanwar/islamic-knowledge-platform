import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import './index.css';
import App from './App.tsx';
import { register } from './serviceWorkerRegistration';

const theme = extendTheme({
  breakpoints: {
    sm: '320px',
    md: '768px',
    lg: '960px',
    xl: '1200px',
  },
  config: {
    initialColorMode: 'light',
    useSystemColorMode: true,
  },
});

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ChakraProvider theme={theme}>
      <App />
    </ChakraProvider>
  </StrictMode>,
);

register({
  onSuccess: () => console.log('Service Worker registered successfully'),
  onUpdate: (registration) => {
    console.log('New content is available; please refresh.');
    if (registration && registration.waiting) {
      registration.waiting.postMessage({ type: 'SKIP_WAITING' });
    }
  },
});
