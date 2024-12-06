import React from 'react';
import { Select, FormControl, FormLabel, Tooltip } from '@chakra-ui/react';

interface DifficultyOption {
  level: string;
  description: string;
}

const difficultyLevels: DifficultyOption[] = [
  {
    level: 'beginner',
    description: 'Basic explanations with simplified terms'
  },
  {
    level: 'intermediate',
    description: 'Moderate detail with some Islamic terminology'
  },
  {
    level: 'advanced',
    description: 'Detailed explanations with scholarly references'
  }
];

interface DifficultyLevelProps {
  onDifficultyChange: (level: string) => void;
  currentDifficulty: string;
}

const DifficultyLevel: React.FC<DifficultyLevelProps> = ({
  onDifficultyChange,
  currentDifficulty,
}) => {
  return (
    <FormControl>
      <FormLabel>Knowledge Level</FormLabel>
      <Tooltip label="Select your preferred level of detail">
        <Select
          value={currentDifficulty}
          onChange={(e) => onDifficultyChange(e.target.value)}
          aria-label="Select knowledge level"
        >
          {difficultyLevels.map((diff) => (
            <option key={diff.level} value={diff.level}>
              {diff.level.charAt(0).toUpperCase() + diff.level.slice(1)} - {diff.description}
            </option>
          ))}
        </Select>
      </Tooltip>
    </FormControl>
  );
};

export default DifficultyLevel;
