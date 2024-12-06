import React from 'react';
import {
  Box,
  Heading,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  useToast,
  Spinner,
  Alert,
  AlertIcon,
} from '@chakra-ui/react';
import ScholarProfile from './ScholarProfile';
import ContributionForm from './ContributionForm';
import ReviewList from './ReviewList';
import { useScholar } from '../../hooks/useScholar';

const ScholarDashboard: React.FC = () => {
  const toast = useToast();
  const { scholar, loading, error } = useScholar();

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minH="200px">
        <Spinner size="xl" />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert status="error">
        <AlertIcon />
        Error loading scholar profile: {error.message}
      </Alert>
    );
  }

  if (!scholar) {
    return (
      <Alert status="warning">
        <AlertIcon />
        Scholar profile not found. Please register or verify your credentials.
      </Alert>
    );
  }

  return (
    <Box p={4}>
      <Heading mb={6}>Scholar Dashboard</Heading>
      <Tabs isLazy>
        <TabList>
          <Tab>Profile</Tab>
          <Tab>Submit Contribution</Tab>
          <Tab>Review Contributions</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <ScholarProfile scholar={scholar} />
          </TabPanel>
          <TabPanel>
            <ContributionForm
              onSuccess={() => {
                toast({
                  title: 'Contribution submitted',
                  description: 'Your contribution has been submitted for peer review.',
                  status: 'success',
                  duration: 5000,
                  isClosable: true,
                });
              }}
              scholarId={scholar.id}
            />
          </TabPanel>
          <TabPanel>
            <ReviewList scholarId={scholar.id} />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default ScholarDashboard;
