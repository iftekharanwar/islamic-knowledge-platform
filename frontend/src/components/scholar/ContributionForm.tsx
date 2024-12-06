import React from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Select,
  Textarea,
  VStack,
  useToast,
  FormErrorMessage,
} from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import { submitContribution } from '../../services/api';

interface ContributionFormData {
  type: string;
  content: string;
  references: string;
}

interface Props {
  onSuccess: () => void;
  scholarId: string;
}

const ContributionForm: React.FC<Props> = ({ onSuccess, scholarId }) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting }
  } = useForm<ContributionFormData>();
  const toast = useToast();

  const onSubmit = async (data: ContributionFormData) => {
    try {
      await submitContribution({
        ...data,
        scholarId,
      });
      reset();
      onSuccess();
    } catch (error) {
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to submit contribution',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box as="form" onSubmit={handleSubmit(onSubmit)}>
      <VStack spacing={4} align="stretch">
        <FormControl isRequired isInvalid={!!errors.type}>
          <FormLabel>Contribution Type</FormLabel>
          <Select {...register('type', { required: 'Type is required' })}>
            <option value="verification">Content Verification</option>
            <option value="knowledge">Specialized Knowledge</option>
            <option value="correction">Content Correction</option>
          </Select>
          <FormErrorMessage>
            {errors.type && errors.type.message}
          </FormErrorMessage>
        </FormControl>

        <FormControl isRequired isInvalid={!!errors.content}>
          <FormLabel>Content</FormLabel>
          <Textarea
            {...register('content', {
              required: 'Content is required',
              minLength: { value: 50, message: 'Content must be at least 50 characters' }
            })}
            placeholder="Enter your contribution here..."
            minH="200px"
          />
          <FormErrorMessage>
            {errors.content && errors.content.message}
          </FormErrorMessage>
        </FormControl>

        <FormControl isRequired isInvalid={!!errors.references}>
          <FormLabel>References</FormLabel>
          <Textarea
            {...register('references', {
              required: 'References are required'
            })}
            placeholder="Enter references to support your contribution..."
          />
          <FormErrorMessage>
            {errors.references && errors.references.message}
          </FormErrorMessage>
        </FormControl>

        <Button
          type="submit"
          colorScheme="blue"
          isLoading={isSubmitting}
          loadingText="Submitting..."
        >
          Submit Contribution
        </Button>
      </VStack>
    </Box>
  );
};

export default ContributionForm;
