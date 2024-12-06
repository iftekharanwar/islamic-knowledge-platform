import React from 'react';
import {
  Box,
  VStack,
  Text,
  Badge,
  Heading,
  List,
  ListItem,
} from '@chakra-ui/react';
import { ScholarProfile as ScholarProfileType } from '../../types/scholar';

interface Props {
  scholar: ScholarProfileType;
}

const ScholarProfile: React.FC<Props> = ({ scholar }) => {
  return (
    <Box>
      <VStack align="start" spacing={4}>
        <Heading size="md">{scholar.name}</Heading>
        <Badge colorScheme={
          scholar.verification_status === 'verified' ? 'green' :
          scholar.verification_status === 'pending' ? 'yellow' :
          'red'
        }>
          {scholar.verification_status.toUpperCase()}
        </Badge>
        <Text><strong>Email:</strong> {scholar.email}</Text>
        <Text><strong>Institution:</strong> {scholar.institution || 'Not specified'}</Text>
        <Box>
          <Text fontWeight="bold" mb={2}>Specializations:</Text>
          <List spacing={2}>
            {scholar.specializations.map((spec, index) => (
              <ListItem key={index}>
                <Badge colorScheme="blue">{spec}</Badge>
              </ListItem>
            ))}
          </List>
        </Box>
        <Text><strong>Contributions:</strong> {scholar.contributions_count}</Text>
        {scholar.verification_date && (
          <Text>
            <strong>Verified on:</strong>{' '}
            {new Date(scholar.verification_date).toLocaleDateString()}
          </Text>
        )}
      </VStack>
    </Box>
  );
};

export default ScholarProfile;
