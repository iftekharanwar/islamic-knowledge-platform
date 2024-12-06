import React from 'react';
import {
  Box,
  VStack,
  Heading,
  Text,
  Badge,
  Button,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  Textarea,
  FormControl,
  FormLabel,
  Select,
  useToast,
  FormErrorMessage,
} from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import { getContributionsForReview, submitReview } from '../../services/api';
import { ScholarContribution } from '../../types/scholar';

interface Props {
  scholarId: string;
}

interface ReviewFormData {
  status: 'approved' | 'needs_revision' | 'rejected';
  comment: string;
}

const ReviewList: React.FC<Props> = ({ scholarId }) => {
  const [contributions, setContributions] = React.useState<ScholarContribution[]>([]);
  const [selectedContribution, setSelectedContribution] = React.useState<ScholarContribution | null>(null);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting }
  } = useForm<ReviewFormData>();
  const toast = useToast();

  React.useEffect(() => {
    loadContributions();
  }, [scholarId]);

  const loadContributions = async () => {
    try {
      const data = await getContributionsForReview();
      setContributions(data);
    } catch (error) {
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to load contributions for review',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleReview = (contribution: ScholarContribution) => {
    setSelectedContribution(contribution);
    onOpen();
  };

  const onSubmitReview = async (data: ReviewFormData) => {
    if (!selectedContribution) return;

    try {
      await submitReview({
        contributionId: selectedContribution.id,
        reviewerId: scholarId,
        status: data.status,
        comment: data.comment,
      });
      toast({
        title: 'Success',
        description: 'Review submitted successfully.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      onClose();
      reset();
      loadContributions();
    } catch (error) {
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to submit review',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box>
      <Heading size="md" mb={4}>Contributions for Review</Heading>
      <VStack spacing={4} align="stretch">
        {contributions.map((contribution) => (
          <Box
            key={contribution.id}
            p={4}
            borderWidth={1}
            borderRadius="md"
            shadow="sm"
          >
            <Text fontSize="sm" color="gray.500">
              Submitted by: {contribution.scholar_name}
            </Text>
            <Text mt={2}>{contribution.content}</Text>
            <Badge mt={2} colorScheme="blue">
              {contribution.contribution_type}
            </Badge>
            <Button
              mt={3}
              size="sm"
              colorScheme="blue"
              onClick={() => handleReview(contribution)}
            >
              Review
            </Button>
          </Box>
        ))}
      </VStack>

      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Submit Review</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Box as="form" onSubmit={handleSubmit(onSubmitReview)} pb={6}>
              <VStack spacing={4}>
                <FormControl isRequired isInvalid={!!errors.status}>
                  <FormLabel>Review Status</FormLabel>
                  <Select {...register('status', { required: 'Status is required' })}>
                    <option value="approved">Approve</option>
                    <option value="needs_revision">Needs Revision</option>
                    <option value="rejected">Reject</option>
                  </Select>
                  <FormErrorMessage>
                    {errors.status && errors.status.message}
                  </FormErrorMessage>
                </FormControl>

                <FormControl isRequired isInvalid={!!errors.comment}>
                  <FormLabel>Comments</FormLabel>
                  <Textarea
                    {...register('comment', {
                      required: 'Comments are required',
                      minLength: { value: 20, message: 'Comments must be at least 20 characters' }
                    })}
                    placeholder="Enter your review comments..."
                    minH="200px"
                  />
                  <FormErrorMessage>
                    {errors.comment && errors.comment.message}
                  </FormErrorMessage>
                </FormControl>

                <Button
                  type="submit"
                  colorScheme="blue"
                  isLoading={isSubmitting}
                  loadingText="Submitting..."
                >
                  Submit Review
                </Button>
              </VStack>
            </Box>
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default ReviewList;
