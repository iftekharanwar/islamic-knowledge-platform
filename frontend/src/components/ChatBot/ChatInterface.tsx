import React, { useState } from 'react';
import {
  Box,
  Input,
  Button,
  Stack,
  Text,
  Container,
  useToast as chakraUseToast,
  Divider as ChakraDivider,
} from '@chakra-ui/react';
import { queryKnowledgeBase } from '../../services/api';
import LanguageSelector from '../accessibility/LanguageSelector';
import DifficultyLevel from '../accessibility/DifficultyLevel';

interface Message {
  text: string;
  isUser: boolean;
  confidence?: number;
  references?: {
    type: string;
    source: string;
    reference: string;
    scholar?: string;
  }[];
}

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState('en');
  const [difficulty, setDifficulty] = useState('intermediate');
  const toast = chakraUseToast();

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    try {
      setIsLoading(true);
      // Add user message
      const userMessage = { text: input, isUser: true };
      setMessages(prev => [...prev, userMessage]);

      // Call AI service using the API service with preferences
      const data = await queryKnowledgeBase(input, {
        language,
        difficultyLevel: difficulty
      });

      // Add AI response
      const aiResponse = {
        text: data.text,
        isUser: false,
        confidence: data.confidence,
        references: data.references,
      };
      setMessages(prev => [...prev, aiResponse]);

      setInput('');
    } catch (error) {
      console.error('Error querying knowledge base:', error);
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to get response. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.md" py={8}>
      <Stack spacing={4} width="100%">
        <Box mb={4}>
          <LanguageSelector
            currentLanguage={language}
            onLanguageChange={setLanguage}
          />
          <DifficultyLevel
            currentDifficulty={difficulty}
            onDifficultyChange={setDifficulty}
          />
        </Box>
        <Box flex={1} overflowY="auto" minH="400px" p={4} borderWidth={1} borderRadius="md" width="100%">
          {messages.map((message, index) => (
            <Box
              key={index}
              bg={message.isUser ? 'blue.50' : 'green.50'}
              p={3}
              borderRadius="md"
              mb={4}
              maxW="80%"
              ml={message.isUser ? 'auto' : 0}
            >
              <Text fontWeight={message.isUser ? 'normal' : 'medium'}>{message.text}</Text>
              {!message.isUser && message.confidence && (
                <>
                  <ChakraDivider my={2} />
                  <Text fontSize="sm" color="gray.600">
                    Confidence: {(message.confidence * 100).toFixed(1)}%
                  </Text>
                  {message.references && message.references.length > 0 && (
                    <Box mt={2}>
                      <Text fontSize="sm" fontWeight="bold">References:</Text>
                      {message.references.map((ref, idx) => (
                        <Text key={idx} fontSize="sm" color="gray.600">
                          {ref.source} - {ref.reference}
                          {ref.scholar && ` (${ref.scholar})`}
                        </Text>
                      ))}
                    </Box>
                  )}
                </>
              )}
            </Box>
          ))}
        </Box>
        <Box width="100%">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about Islam..."
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            disabled={isLoading}
          />
          <Button
            mt={2}
            colorScheme="blue"
            onClick={handleSendMessage}
            isLoading={isLoading}
            loadingText="Sending..."
            width="100%"
          >
            Send
          </Button>
        </Box>
      </Stack>
    </Container>
  );
};

export default ChatInterface;
