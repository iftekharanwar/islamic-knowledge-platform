import React from 'react';
import { Box, Container, Heading, Text } from '@chakra-ui/react';

const Header: React.FC = () => {
  return (
    <Box bg="blue.600" color="white" py={4}>
      <Container maxW="container.xl">
        <Heading size="lg">Islamic Knowledge Platform</Heading>
        <Text mt={1}>Access authentic Islamic knowledge through AI-powered guidance</Text>
      </Container>
    </Box>
  );
};

export default Header;
