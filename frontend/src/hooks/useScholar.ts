import { useState, useEffect } from 'react';
import { ScholarProfile } from '../types/scholar';
import { getScholarProfile } from '../services/api';

export const useScholar = () => {
  const [scholar, setScholar] = useState<ScholarProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const loadScholar = async () => {
      try {
        setLoading(true);
        const data = await getScholarProfile();
        setScholar(data);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    loadScholar();
  }, []);

  return { scholar, loading, error };
};
