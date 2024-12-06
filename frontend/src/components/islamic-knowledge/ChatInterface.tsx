import { useState } from 'react';
import {
  Box,
  VStack,
  HStack,
  Input,
  Button,
  Text,
  useToast,
  Container,
  Divider,
  Badge,
} from '@chakra-ui/react';
import axios from 'axios';

interface Message {
  text: string;
  isUser: boolean;
  references?: Array<{
    type: string;
    source: string;
    reference: string;
  }>;
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      text: input,
      isUser: true,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.get('/api/v1/knowledge/search', {
        params: { query: input }
      });

      const aiMessage: Message = {
        text: response.data.response,
        isUser: false,
        references: response.data.references,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to get response. Please try again.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.md" py={8}>
      <VStack spacing={4} align="stretch" h="600px">
        <Box flex="1" overflowY="auto" p={4} borderWidth={1} borderRadius="md">
          {messages.map((message, index) => (
            <Box
              key={index}
              bg={message.isUser ? 'blue.50' : 'green.50'}
              p={3}
              borderRadius="md"
              mb={2}
              maxW="80%"
              ml={message.isUser ? 'auto' : 0}
            >
              <Text>{message.text}</Text>
              {message.references && (
                <VStack align="start" mt={2} spacing={1}>
                  {message.references.map((ref, idx) => (
                    <HStack key={idx} spacing={2}>
                      <Badge colorScheme="purple">{ref.type}</Badge>
                      <Text fontSize="sm">{ref.source}: {ref.reference}</Text>
                    </HStack>
                  ))}
                </VStack>
              )}
            </Box>
          ))}
        </Box>
        <Divider />
        <HStack>
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about Islam..."
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <Button
            colorScheme="teal"
            onClick={handleSendMessage}
            isLoading={isLoading}
          >
            Send
          </Button>
        </HStack>
      </VStack>
    </Container>
  );
};

export default ChatInterface;
