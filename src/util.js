export const promptGreetings = 
  `Welcome to BizAI Bank Assistant!       
  I\'m here to guide you through the process of applying for a loan and provide insights on your eligibility based on your analysis.`;

export const DEFAULT_OPTIONS = [
  'Get Started',
  'About MSME\'s Loans',
  'Check Eligibility',
  'More Options'
]

export const BPI_RELATED = [
  'Ka-Negosyo', 'MSME', 'SME', 'Credibility', 'Eligibility', 'Business loans',
  'Personal loans', 'Credit score', 'Credit history', 'Credit report', 'BPI',
  "Tailored loaning plan", "Tailored loan", "Personalized loan", "Personalized loaning plan",
  "Business health check", "Application process", "Eligibility criteria", "Documents required",
  "Tailored", "Personalized", "Yes, proceed with business health check.",
  "Yes, proceed with loaning application.", "loaning application"
]

export const isBPI = sentence => {
  return BPI_RELATED.some(word => new RegExp(`\\b${word}\\b`, 'i').test(sentence));
}

export const isYesOrNo = message => {
  const yesNoPattern = /(?:is|are|can|will|do|did|does|should|would|could)\s.*\?/i;
  return yesNoPattern.test(message);
}

export const specificKeywords = ['Yes, proceed with business health check', 'Would you like to proceed with the application'];
