import React from 'react';
import { Select, FormControl, FormLabel } from '@chakra-ui/react';

interface LanguageOption {
  code: string;
  name: string;
}

const languages: LanguageOption[] = [
  { code: 'en', name: 'English' },
  { code: 'ar', name: 'العربية (Arabic)' },
  { code: 'ur', name: 'اردو (Urdu)' },
  { code: 'ms', name: 'Bahasa Melayu (Malay)' },
  { code: 'tr', name: 'Türkçe (Turkish)' },
];

interface LanguageSelectorProps {
  onLanguageChange: (language: string) => void;
  currentLanguage: string;
}

const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  onLanguageChange,
  currentLanguage,
}) => {
  return (
    <FormControl>
      <FormLabel>Select Language / اختر اللغة</FormLabel>
      <Select
        value={currentLanguage}
        onChange={(e) => onLanguageChange(e.target.value)}
        aria-label="Select language"
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </Select>
    </FormControl>
  );
};

export default LanguageSelector;
